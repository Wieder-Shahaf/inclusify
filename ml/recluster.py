"""Re-cluster existing sentences with updated parameters.

This script loads sentences from sentences_raw.csv, regenerates embeddings,
and performs clustering with the current parameters, then outputs
sentences_clustered.csv. Useful for experimenting with different clustering
parameters without re-running the entire pipeline.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
import pandas as pd

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


def recluster(
    input_csv: str = "data/output/sentences_raw.csv",
    output_csv: str = "data/output/sentences_clustered.csv",
    method: str = 'gmm',
    min_cluster_size: int = 5,
    min_samples: int = 3,
    n_components: Optional[int] = None,
    metric: str = 'cosine'
):
    """
    Re-cluster sentences from an existing CSV file.
    
    Args:
        input_csv: Path to sentences_raw.csv
        output_csv: Path to output sentences_clustered.csv
        method: Clustering method ('hdbscan' or 'gmm' for EM/GMM)
        min_cluster_size: Minimum cluster size for HDBSCAN
        min_samples: Minimum samples for HDBSCAN
        n_components: Number of clusters for GMM (auto if None)
        metric: Distance metric ('euclidean' or 'cosine')
    """
    logger.info("=" * 80)
    logger.info("Re-clustering Sentences")
    logger.info("=" * 80)
    
    # Load sentences
    logger.info(f"\n[Step 1/3] Loading sentences from {input_csv}...")
    input_path = Path(input_csv)
    if not input_path.exists():
        logger.error(f"Input file not found: {input_csv}")
        return
    
    sentences_df = pd.read_csv(input_csv)
    logger.info(f"Loaded {len(sentences_df)} sentences")
    
    # Generate embeddings
    logger.info("\n[Step 2/3] Generating sentence embeddings...")
    encoder = SentenceEncoder()
    sentence_texts = sentences_df['sentence_text'].tolist()
    embeddings = encoder.encode(sentence_texts)
    
    # Perform clustering
    logger.info("\n[Step 3/3] Performing semantic clustering...")
    clusterer = SentenceClusterer(
        method=method,
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        n_components=n_components,
        metric=metric
    )
    cluster_labels = clusterer.fit_predict(embeddings)
    
    # Create clustered sentences CSV
    logger.info("\nCreating clustered sentences CSV...")
    clustered_df = sentences_df.copy()
    clustered_df['cluster_id'] = cluster_labels
    
    # Reorder columns: sentence_id, sentence_text, cluster_id, source_pdf, source_url
    clustered_df = clustered_df[['sentence_id', 'sentence_text', 'cluster_id', 'source_pdf', 'source_url']]
    
    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    clustered_df.to_csv(output_path, index=False)
    logger.info(f"Saved {len(clustered_df)} labeled sentences to {output_path}")
    
    # Summary statistics
    logger.info("\n" + "=" * 80)
    logger.info("Clustering Summary")
    logger.info("=" * 80)
    logger.info(f"Total sentences: {len(clustered_df)}")
    logger.info(f"Unique clusters: {len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)}")
    logger.info(f"Noise points (outliers): {sum(cluster_labels == -1)}")
    
    # Cluster size distribution
    cluster_counts = pd.Series(cluster_labels).value_counts().sort_index()
    logger.info(f"\nCluster distribution:")
    for cluster_id, count in cluster_counts.items():
        if cluster_id == -1:
            logger.info(f"  Noise (cluster_id=-1): {count} sentences")
        else:
            logger.info(f"  Cluster {cluster_id}: {count} sentences")
    
    logger.info(f"\nOutput file: {output_path}")
    logger.info("=" * 80)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Re-cluster sentences with updated parameters"
    )
    parser.add_argument(
        '--input',
        type=str,
        default='data/output/sentences_raw.csv',
        help='Input CSV file (default: data/output/sentences_raw.csv)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='data/output/sentences_clustered.csv',
        help='Output CSV file (default: data/output/sentences_clustered.csv)'
    )
    parser.add_argument(
        '--method',
        type=str,
        choices=['hdbscan', 'gmm'],
        default='gmm',
        help='Clustering method: hdbscan or gmm (EM algorithm) (default: gmm)'
    )
    parser.add_argument(
        '--n-components',
        type=int,
        default=None,
        help='Number of clusters for GMM (auto-determined if not specified)'
    )
    parser.add_argument(
        '--min-cluster-size',
        type=int,
        default=5,
        help='Minimum cluster size for HDBSCAN (default: 5)'
    )
    parser.add_argument(
        '--min-samples',
        type=int,
        default=3,
        help='Minimum samples for HDBSCAN (default: 3)'
    )
    parser.add_argument(
        '--metric',
        type=str,
        choices=['euclidean', 'cosine'],
        default='cosine',
        help='Distance metric (default: cosine)'
    )
    
    args = parser.parse_args()
    
    recluster(
        input_csv=args.input,
        output_csv=args.output,
        method=args.method,
        min_cluster_size=args.min_cluster_size,
        min_samples=args.min_samples,
        n_components=args.n_components,
        metric=args.metric
    )


if __name__ == "__main__":
    main()
