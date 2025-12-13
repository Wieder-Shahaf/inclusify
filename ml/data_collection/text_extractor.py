"""Text extraction module for extracting and cleaning text from PDF files."""

import logging
import re
from pathlib import Path
from typing import Optional
import pdfplumber

logger = logging.getLogger(__name__)


class TextExtractor:
    """Extracts and cleans text from PDF files."""
    
    def __init__(self):
        """Initialize the text extractor."""
        self.reference_patterns = [
            r'^references\s*$',
            r'^bibliography\s*$',
            r'^works\s+cited\s*$',
            r'^literature\s+cited\s*$',
        ]
    
    def _remove_headers_footers(self, text: str) -> str:
        """
        Remove headers and footers from text using heuristics.
        
        Args:
            text: Raw text from PDF
            
        Returns:
            Text with headers and footers removed
        """
        lines = text.split('\n')
        cleaned_lines = []
        
        # Track lines that appear frequently (likely headers/footers)
        line_counts = {}
        for line in lines:
            stripped = line.strip()
            if stripped:
                line_counts[stripped] = line_counts.get(stripped, 0) + 1
        
        # Identify common headers/footers (appear more than 3 times)
        common_lines = {line for line, count in line_counts.items() if count > 3}
        
        # Filter out common lines and page numbers
        for line in lines:
            stripped = line.strip()
            # Skip empty lines
            if not stripped:
                cleaned_lines.append('')
                continue
            
            # Skip if it's a common header/footer
            if stripped in common_lines:
                continue
            
            # Skip lines that are just page numbers
            if re.match(r'^\d+$', stripped):
                continue
            
            # Skip lines that are very short and appear frequently (likely headers)
            if len(stripped) < 20 and line_counts.get(stripped, 0) > 2:
                continue
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _remove_references(self, text: str) -> str:
        """
        Remove references section from text.
        
        Args:
            text: Text that may contain references
            
        Returns:
            Text with references section removed
        """
        lines = text.split('\n')
        cleaned_lines = []
        in_references = False
        
        for line in lines:
            stripped = line.strip().lower()
            
            # Check if we've hit a references section
            if not in_references:
                for pattern in self.reference_patterns:
                    if re.match(pattern, stripped):
                        in_references = True
                        logger.debug(f"Found references section at: {line}")
                        break
                
                if not in_references:
                    cleaned_lines.append(line)
            else:
                # Skip lines in references section
                # Stop if we hit a new major section (all caps, likely a heading)
                if len(stripped) > 0 and stripped.isupper() and len(stripped) < 50:
                    # Might be a new section, but be conservative
                    pass
                # Continue skipping reference content
                continue
        
        return '\n'.join(cleaned_lines)
    
    def _normalize_whitespace(self, text: str) -> str:
        """
        Normalize whitespace in text.
        
        Args:
            text: Text with potentially irregular whitespace
            
        Returns:
            Text with normalized whitespace
        """
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        # Replace multiple newlines with double newline (paragraph break)
        text = re.sub(r'\n{3,}', '\n\n', text)
        # Remove trailing whitespace from lines
        lines = [line.rstrip() for line in text.split('\n')]
        return '\n'.join(lines)
    
    def extract_text(self, pdf_path: str) -> Optional[str]:
        """
        Extract and clean text from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Cleaned text, or None if extraction failed
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            logger.error(f"PDF file not found: {pdf_path}")
            return None
        
        try:
            text_parts = []
            
            with pdfplumber.open(pdf_path) as pdf:
                logger.debug(f"Extracting text from {pdf_path.name} ({len(pdf.pages)} pages)")
                
                for page_num, page in enumerate(pdf.pages, 1):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text_parts.append(page_text)
                    except Exception as e:
                        logger.warning(f"Failed to extract text from page {page_num} of {pdf_path.name}: {e}")
                        continue
            
            if not text_parts:
                logger.warning(f"No text extracted from {pdf_path.name}")
                return None
            
            raw_text = '\n'.join(text_parts)
            
            # Clean the text
            cleaned_text = self._remove_headers_footers(raw_text)
            cleaned_text = self._remove_references(cleaned_text)
            cleaned_text = self._normalize_whitespace(cleaned_text)
            
            logger.info(f"Extracted {len(cleaned_text)} characters from {pdf_path.name}")
            return cleaned_text
            
        except Exception as e:
            logger.error(f"Failed to extract text from {pdf_path}: {e}")
            return None
