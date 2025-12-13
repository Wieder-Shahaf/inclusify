"""Clustering module for semantic clustering of sentence embeddings."""

import logging
from typing import List, Optional
import numpy as np
import hdbscan
from sklearn.mixture import GaussianMixture

logger = logging.getLogger(__name__)


class SentenceClusterer:
    """Performs semantic clustering on sentence embeddings."""
    
    def __init__(
        self,
        min_cluster_size: int = 10,
        min_samples: int = 5,
        metric: str = 'euclidean',
        method: str = 'hdbscan',
        n_components: Optional[int] = None
    ):
        """
        Initialize the clusterer.
        
        Args:
            min_cluster_size: Minimum size of clusters (for HDBSCAN)
            min_samples: Minimum number of samples in a cluster (for HDBSCAN)
            metric: Distance metric ('euclidean' or 'cosine')
            method: Clustering method ('hdbscan' or 'gmm' for EM/GMM)
            n_components: Number of clusters for GMM (auto-determined if None)
        """
        self.min_cluster_size = min_cluster_size
        self.min_samples = min_samples
        self.metric = metric
        self.method = method.lower()
        self.n_components = n_components
        self.clusterer = None
    
    def _determine_n_components(self, n_samples: int) -> int:
        """
        Automatically determine number of components for GMM.
        
        Uses a heuristic based on sample size.
        
        Args:
            n_samples: Number of samples
            
        Returns:
            Suggested number of components
        """
        if n_samples < 100:
            return max(3, n_samples // 20)
        elif n_samples < 1000:
            return max(5, n_samples // 50)
        elif n_samples < 10000:
            return max(10, n_samples // 200)
        else:
            return max(20, n_samples // 500)
    
    def fit_predict(self, embeddings: np.ndarray) -> np.ndarray:
        """
        Fit the clustering model and predict cluster labels.
        
        Args:
            embeddings: Numpy array of embeddings with shape [n_sentences, embedding_dim]
            
        Returns:
            Array of cluster labels (shape: [n_sentences])
            -1 indicates noise points (outliers) for HDBSCAN, not used for GMM
        """
        if embeddings.size == 0:
            logger.warning("Empty embeddings array provided")
            return np.array([])
        
        if len(embeddings.shape) != 2:
            raise ValueError(f"Expected 2D array, got shape {embeddings.shape}")
        
        try:
            # For cosine metric, normalize embeddings
            if self.metric == 'cosine':
                norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
                data_to_cluster = embeddings / (norms + 1e-8)
                metric_note = " (normalized for cosine similarity)"
            else:
                data_to_cluster = embeddings
                metric_note = ""
            
            if self.method == 'gmm':
                # Gaussian Mixture Model with EM algorithm
                n_components = self.n_components
                if n_components is None:
                    n_components = self._determine_n_components(embeddings.shape[0])
                
                logger.info(
                    f"Clustering {embeddings.shape[0]} embeddings with GMM (EM algorithm), "
                    f"n_components={n_components}{metric_note}"
                )
                
                # Initialize GMM
                self.clusterer = GaussianMixture(
                    n_components=n_components,
                    covariance_type='full',  # Full covariance for better fit
                    max_iter=100,
                    n_init=10,  # Multiple initializations for better results
                    random_state=42,
                    verbose=1 if logger.level <= logging.DEBUG else 0
                )
                
                # Fit and predict
                cluster_labels = self.clusterer.fit_predict(data_to_cluster)
                
                # GMM doesn't produce noise points, all points are assigned
                n_noise = 0
                
            else:  # HDBSCAN
                # For cosine, use euclidean on normalized vectors
                if self.metric == 'cosine':
                    actual_metric = 'euclidean'
                else:
                    actual_metric = self.metric
                
                logger.info(
                    f"Clustering {embeddings.shape[0]} embeddings with HDBSCAN, "
                    f"min_cluster_size={self.min_cluster_size}, "
                    f"min_samples={self.min_samples}, "
                    f"metric={self.metric}{metric_note}"
                )
                
                # Initialize HDBSCAN clusterer
                self.clusterer = hdbscan.HDBSCAN(
                    min_cluster_size=self.min_cluster_size,
                    min_samples=self.min_samples,
                    metric=actual_metric,
                    cluster_selection_method='eom'  # Excess of Mass
                )
                
                # Fit and predict
                cluster_labels = self.clusterer.fit_predict(data_to_cluster)
                n_noise = np.sum(cluster_labels == -1)
            
            # Log clustering statistics
            unique_labels, counts = np.unique(cluster_labels, return_counts=True)
            n_clusters = len(unique_labels[unique_labels != -1])
            
            logger.info(
                f"Clustering complete: {n_clusters} clusters found"
            )
            if n_noise > 0:
                logger.info(f"Noise points (outliers): {n_noise}")
            
            # Log cluster sizes (top 10)
            valid_clusters = [(label, count) for label, count in zip(unique_labels, counts) if label != -1]
            valid_clusters.sort(key=lambda x: x[1], reverse=True)
            logger.info(f"Top 10 largest clusters:")
            for label, count in valid_clusters[:10]:
                logger.info(f"  Cluster {label}: {count} points")
            
            return cluster_labels
            
        except Exception as e:
            logger.error(f"Failed to perform clustering: {e}")
            raise
