"""Main pipeline for data collection, preprocessing, and weak labeling."""

import logging
import sys
from pathlib import Path
import pandas as pd

from data_collection.pdf_scraper import PDFScraper
from data_collection.text_extractor import TextExtractor
from preprocessing.sentence_splitter import SentenceSplitter
from embeddings.encoder import SentenceEncoder
from clustering.clusterer import SentenceClusterer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class DataPipeline:
    """End-to-end pipeline for collecting and labeling training data."""
    
    def __init__(
        self,
        target_url: str,
        output_dir: str = "data/output",
        pdf_dir: str = "data/raw_pdfs"
    ):
        """
        Initialize the data pipeline.
        
        Args:
            target_url: URL to scrape for PDFs
            output_dir: Directory for output CSV files
            pdf_dir: Directory for downloaded PDFs
        """
        self.target_url = target_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.pdf_scraper = PDFScraper(output_dir=pdf_dir)
        self.text_extractor = TextExtractor()
        self.sentence_splitter = SentenceSplitter(min_tokens=5)
        self.encoder = SentenceEncoder()
        self.clusterer = SentenceClusterer(
            method='gmm',        # Use GMM/EM algorithm
            n_components=None,    # Auto-determine number of clusters
            metric='cosine'       # Better for normalized embeddings
        )
    
    def run(self):
        """Run the complete pipeline."""
        logger.info("=" * 80)
        logger.info("Starting INCLUSIFY Data Collection and Weak Labeling Pipeline")
        logger.info("=" * 80)
        
        # Step 1: Scrape PDFs
        logger.info("\n[Step 1/6] Scraping PDFs from target URL...")
        pdf_metadata = self.pdf_scraper.scrape(self.target_url)
        
        if not pdf_metadata:
            logger.error("No PDFs were downloaded. Exiting.")
            return
        
        logger.info(f"Successfully downloaded {len(pdf_metadata)} PDF files")
        
        # Step 2: Extract text from PDFs
        logger.info("\n[Step 2/6] Extracting text from PDFs...")
        all_sentences = []
        failed_pdfs = []
        
        for pdf_info in pdf_metadata:
            pdf_path = pdf_info['local_path']
            pdf_url = pdf_info['url']
            pdf_name = Path(pdf_path).name
            
            logger.info(f"Processing: {pdf_name}")
            
            text = self.text_extractor.extract_text(pdf_path)
            
            if not text:
                logger.warning(f"Failed to extract text from {pdf_name}")
                failed_pdfs.append(pdf_name)
                continue
            
            # Step 3: Split into sentences
            sentences = self.sentence_splitter.split(
                text,
                source_pdf=pdf_name,
                source_url=pdf_url
            )
            
            all_sentences.extend(sentences)
            logger.info(f"Extracted {len(sentences)} sentences from {pdf_name}")
        
        if not all_sentences:
            logger.error("No sentences were extracted from any PDF. Exiting.")
            return
        
        logger.info(f"\nTotal sentences extracted: {len(all_sentences)}")
        if failed_pdfs:
            logger.warning(f"Failed to process {len(failed_pdfs)} PDFs: {failed_pdfs}")
        
        # Step 4: Create raw sentences CSV
        logger.info("\n[Step 4/6] Creating sentences_raw.csv...")
        sentences_df = pd.DataFrame(all_sentences)
        sentences_df.insert(0, 'sentence_id', range(1, len(sentences_df) + 1))
        
        # Reorder columns: sentence_id, sentence_text, source_pdf, source_url
        sentences_df = sentences_df[['sentence_id', 'sentence_text', 'source_pdf', 'source_url']]
        
        raw_output_path = self.output_dir / "sentences_raw.csv"
        sentences_df.to_csv(raw_output_path, index=False)
        logger.info(f"Saved {len(sentences_df)} sentences to {raw_output_path}")
        
        # Step 5: Generate embeddings
        logger.info("\n[Step 5/6] Generating sentence embeddings...")
        sentence_texts = sentences_df['sentence_text'].tolist()
        embeddings = self.encoder.encode(sentence_texts)
        
        # Step 6: Perform clustering
        logger.info("\n[Step 6/6] Performing semantic clustering...")
        cluster_labels = self.clusterer.fit_predict(embeddings)
        
        # Create clustered sentences CSV
        logger.info("\nCreating sentences_clustered.csv...")
        clustered_df = sentences_df.copy()
        clustered_df['cluster_id'] = cluster_labels
        
        # Reorder columns: sentence_id, sentence_text, cluster_id, source_pdf, source_url
        clustered_df = clustered_df[['sentence_id', 'sentence_text', 'cluster_id', 'source_pdf', 'source_url']]
        
        clustered_output_path = self.output_dir / "sentences_clustered.csv"
        clustered_df.to_csv(clustered_output_path, index=False)
        logger.info(f"Saved {len(clustered_df)} labeled sentences to {clustered_output_path}")
        
        # Summary statistics
        logger.info("\n" + "=" * 80)
        logger.info("Pipeline Summary")
        logger.info("=" * 80)
        logger.info(f"PDFs processed: {len(pdf_metadata) - len(failed_pdfs)}/{len(pdf_metadata)}")
        logger.info(f"Total sentences: {len(all_sentences)}")
        logger.info(f"Unique clusters: {len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)}")
        logger.info(f"Noise points (outliers): {sum(cluster_labels == -1)}")
        logger.info(f"\nOutput files:")
        logger.info(f"  - {raw_output_path}")
        logger.info(f"  - {clustered_output_path}")
        logger.info("=" * 80)


def main():
    """Main entry point for the pipeline."""
    # TODO: Replace with actual target URL
    # For now, using a placeholder - user should update this
    TARGET_URL = "https://arxiv.org/search/?searchtype=all&query=LGBTQ&abstracts=show&size=100&order="
    
    if len(sys.argv) > 1:
        TARGET_URL = sys.argv[1]
        logger.info(f"Using target URL from command line: {TARGET_URL}")
    else:
        logger.warning(
            f"Using default/placeholder URL: {TARGET_URL}\n"
            "Please provide a target URL as a command-line argument or update TARGET_URL in pipeline.py"
        )
    
    pipeline = DataPipeline(target_url=TARGET_URL)
    pipeline.run()


if __name__ == "__main__":
    main()
