"""PDF scraper module for discovering and downloading PDF files from URLs."""

import os
import hashlib
import logging
import re
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class PDFScraper:
    """Scrapes a webpage to discover and download PDF files."""
    
    def __init__(self, output_dir: str = "data/raw_pdfs"):
        """
        Initialize the PDF scraper.
        
        Args:
            output_dir: Directory to save downloaded PDFs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.downloaded_urls = set()  # Track downloaded URLs to avoid duplicates
        
    def _get_url_hash(self, url: str) -> str:
        """Generate a hash for a URL to use as a unique identifier."""
        return hashlib.md5(url.encode()).hexdigest()
    
    def _is_pdf_url(self, url: str) -> bool:
        """Check if a URL points to a PDF file."""
        parsed = urlparse(url)
        path = parsed.path.lower()
        return path.endswith('.pdf') or 'pdf' in parsed.query.lower()
    
    def _is_arxiv_url(self, url: str) -> bool:
        """Check if a URL is from arXiv."""
        parsed = urlparse(url)
        return 'arxiv.org' in parsed.netloc.lower()
    
    def _extract_arxiv_ids(self, base_url: str) -> List[str]:
        """
        Extract arXiv paper IDs from an arXiv search or listing page.
        
        Args:
            base_url: arXiv search or listing URL
            
        Returns:
            List of arXiv paper IDs (e.g., ['2301.12345', '2302.67890'])
        """
        try:
            response = requests.get(base_url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {base_url}: {e}")
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        arxiv_ids = []
        
        # Pattern for arXiv IDs: YYMM.NNNNN or YYMM.NNNNNvN
        # Also handle old format: YYMM.NNNN
        arxiv_id_pattern = re.compile(r'/(?:abs|pdf)/(\d{4}\.\d{4,5}(?:v\d+)?)')
        
        # Find all links that contain arXiv IDs
        for link in soup.find_all('a', href=True):
            href = link['href']
            match = arxiv_id_pattern.search(href)
            if match:
                paper_id = match.group(1)
                if paper_id not in arxiv_ids:
                    arxiv_ids.append(paper_id)
        
        # Also check for arXiv IDs in text content (some pages list them)
        text_content = soup.get_text()
        text_matches = re.findall(r'\b(\d{4}\.\d{4,5}(?:v\d+)?)\b', text_content)
        for match in text_matches:
            if match not in arxiv_ids:
                arxiv_ids.append(match)
        
        logger.info(f"Extracted {len(arxiv_ids)} arXiv paper IDs from {base_url}")
        return arxiv_ids
    
    def _construct_arxiv_pdf_url(self, paper_id: str) -> str:
        """
        Construct arXiv PDF URL from paper ID.
        
        Args:
            paper_id: arXiv paper ID (e.g., '2301.12345' or '2301.12345v2')
            
        Returns:
            URL to the PDF file
        """
        return f"https://arxiv.org/pdf/{paper_id}.pdf"
    
    def _discover_pdf_urls(self, base_url: str) -> List[str]:
        """
        Discover all PDF URLs on a webpage.
        
        Args:
            base_url: The URL to crawl
            
        Returns:
            List of PDF URLs found on the page
        """
        # Special handling for arXiv
        if self._is_arxiv_url(base_url):
            arxiv_ids = self._extract_arxiv_ids(base_url)
            pdf_urls = [self._construct_arxiv_pdf_url(paper_id) for paper_id in arxiv_ids]
            logger.info(f"Discovered {len(pdf_urls)} arXiv PDF URLs from {base_url}")
            return pdf_urls
        
        # Standard PDF discovery for other sites
        try:
            response = requests.get(base_url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {base_url}: {e}")
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        pdf_urls = []
        
        # Find all anchor tags with href attributes
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(base_url, href)
            
            if self._is_pdf_url(absolute_url):
                pdf_urls.append(absolute_url)
        
        # Also check for direct PDF links in iframes, embeds, etc.
        for tag in soup.find_all(['iframe', 'embed', 'object']):
            src = tag.get('src') or tag.get('data')
            if src:
                absolute_url = urljoin(base_url, src)
                if self._is_pdf_url(absolute_url):
                    pdf_urls.append(absolute_url)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_urls = []
        for url in pdf_urls:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)
        
        logger.info(f"Discovered {len(unique_urls)} PDF URLs from {base_url}")
        return unique_urls
    
    def _download_pdf(self, url: str) -> Optional[Path]:
        """
        Download a PDF file from a URL.
        
        Args:
            url: URL of the PDF to download
            
        Returns:
            Path to downloaded file, or None if download failed
        """
        url_hash = self._get_url_hash(url)
        
        # Check if already downloaded
        if url_hash in self.downloaded_urls:
            logger.debug(f"PDF already downloaded: {url}")
            return None
        
        try:
            response = requests.get(url, timeout=60, stream=True)
            response.raise_for_status()
            
            # Check if response is actually a PDF
            content_type = response.headers.get('content-type', '').lower()
            if 'pdf' not in content_type:
                # Check first bytes for PDF magic number
                first_bytes = response.content[:4]
                if first_bytes != b'%PDF':
                    logger.warning(f"URL {url} does not appear to be a PDF (content-type: {content_type})")
                    return None
            
            # Generate filename from URL
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path)
            
            # Special handling for arXiv: use paper ID as filename
            if 'arxiv.org' in parsed.netloc.lower() and '/pdf/' in parsed.path:
                paper_id = parsed.path.split('/pdf/')[-1].replace('.pdf', '')
                filename = f"arxiv_{paper_id}.pdf"
            elif not filename or not filename.endswith('.pdf'):
                filename = f"{url_hash}.pdf"
            
            filepath = self.output_dir / filename
            
            # Handle filename conflicts
            counter = 1
            original_filepath = filepath
            while filepath.exists():
                stem = original_filepath.stem
                filepath = self.output_dir / f"{stem}_{counter}.pdf"
                counter += 1
            
            # Download file
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            self.downloaded_urls.add(url_hash)
            logger.info(f"Downloaded PDF: {filepath.name} from {url}")
            return filepath
            
        except requests.RequestException as e:
            logger.error(f"Failed to download PDF from {url}: {e}")
            return None
        except IOError as e:
            logger.error(f"Failed to save PDF from {url}: {e}")
            return None
    
    def scrape(self, target_url: str) -> List[Dict[str, str]]:
        """
        Scrape PDFs from a target URL.
        
        Args:
            target_url: URL to crawl for PDFs
            
        Returns:
            List of dictionaries with metadata about downloaded PDFs:
            [{'url': str, 'local_path': str, 'download_timestamp': str}]
        """
        logger.info(f"Starting PDF scraping from {target_url}")
        
        pdf_urls = self._discover_pdf_urls(target_url)
        downloaded_files = []
        
        for url in pdf_urls:
            filepath = self._download_pdf(url)
            if filepath:
                downloaded_files.append({
                    'url': url,
                    'local_path': str(filepath),
                    'download_timestamp': filepath.stat().st_mtime
                })
        
        logger.info(f"Downloaded {len(downloaded_files)} PDF files")
        return downloaded_files
