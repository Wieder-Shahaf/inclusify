"""Sentence embedding encoder module."""

import logging
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class SentenceEncoder:
    """Generates semantic embeddings for sentences."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-mpnet-base-v2", batch_size: int = 32):
        """
        Initialize the sentence encoder.
        
        Args:
            model_name: Name of the sentence transformer model
            batch_size: Batch size for encoding
        """
        self.model_name = model_name
        self.batch_size = batch_size
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the sentence transformer model."""
        try:
            logger.info(f"Loading sentence transformer model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model {self.model_name}: {e}")
            raise
    
    def encode(self, sentences: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of sentences.
        
        Args:
            sentences: List of sentence strings
            
        Returns:
            Numpy array of embeddings with shape [n_sentences, embedding_dim]
        """
        if not sentences:
            logger.warning("Empty sentence list provided")
            return np.array([])
        
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        try:
            logger.info(f"Encoding {len(sentences)} sentences in batches of {self.batch_size}")
            
            # Encode sentences in batches
            embeddings = self.model.encode(
                sentences,
                batch_size=self.batch_size,
                show_progress_bar=True,
                convert_to_numpy=True,
                normalize_embeddings=True  # Normalize for better clustering
            )
            
            logger.info(f"Generated embeddings with shape {embeddings.shape}")
            return embeddings
            
        except Exception as e:
            logger.error(f"Failed to encode sentences: {e}")
            raise
