"""Sentence splitting module for splitting text into sentences and filtering."""

import logging
import re
from typing import List, Dict
import nltk

logger = logging.getLogger(__name__)


class SentenceSplitter:
    """Splits text into sentences and filters them."""
    
    def __init__(self, min_tokens: int = 5):
        """
        Initialize the sentence splitter.
        
        Args:
            min_tokens: Minimum number of tokens required for a sentence
        """
        self.min_tokens = min_tokens
        self._ensure_nltk_data()
    
    def _ensure_nltk_data(self):
        """Ensure required NLTK data is downloaded."""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            logger.info("Downloading NLTK punkt tokenizer...")
            nltk.download('punkt', quiet=True)
        
        try:
            nltk.data.find('tokenizers/punkt/english')
        except LookupError:
            logger.info("Downloading NLTK English punkt data...")
            nltk.download('punkt_tab', quiet=True)
    
    def _is_english(self, text: str) -> bool:
        """
        Basic check if text is English.
        
        Args:
            text: Text to check
            
        Returns:
            True if text appears to be English
        """
        # Check if text is primarily ASCII or common English Unicode ranges
        ascii_count = sum(1 for c in text if ord(c) < 128)
        total_chars = len([c for c in text if c.isalnum() or c.isspace()])
        
        if total_chars == 0:
            return False
        
        # If more than 90% of characters are ASCII, likely English
        ascii_ratio = ascii_count / total_chars if total_chars > 0 else 0
        
        # Also check for common English words/patterns
        common_english_words = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
        text_lower = text.lower()
        english_word_count = sum(1 for word in common_english_words if word in text_lower)
        
        return ascii_ratio > 0.9 or english_word_count > 0
    
    def _count_tokens(self, sentence: str) -> int:
        """
        Count tokens in a sentence.
        
        Args:
            sentence: Sentence to tokenize
            
        Returns:
            Number of tokens
        """
        try:
            tokens = nltk.word_tokenize(sentence)
            return len(tokens)
        except Exception as e:
            logger.warning(f"Failed to tokenize sentence: {e}")
            # Fallback: split by whitespace
            return len(sentence.split())
    
    def _is_valid_sentence(self, sentence: str) -> bool:
        """
        Check if a sentence is valid (non-empty, long enough, English).
        
        Args:
            sentence: Sentence to validate
            
        Returns:
            True if sentence is valid
        """
        # Check if non-empty
        if not sentence or not sentence.strip():
            return False
        
        # Check minimum token length
        token_count = self._count_tokens(sentence)
        if token_count < self.min_tokens:
            return False
        
        # Check if English
        if not self._is_english(sentence):
            return False
        
        return True
    
    def split(self, text: str, source_pdf: str = "", source_url: str = "") -> List[Dict[str, str]]:
        """
        Split text into sentences and filter them.
        
        Args:
            text: Text to split
            source_pdf: Name of source PDF file
            source_url: URL of source PDF
            
        Returns:
            List of sentence dictionaries with metadata:
            [{'sentence_text': str, 'source_pdf': str, 'source_url': str}]
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for splitting")
            return []
        
        try:
            # Split into sentences using NLTK
            sentences = nltk.sent_tokenize(text)
            logger.debug(f"Split text into {len(sentences)} raw sentences")
            
            # Filter and clean sentences
            valid_sentences = []
            for sentence in sentences:
                # Clean sentence
                sentence = sentence.strip()
                
                # Remove extra whitespace
                sentence = re.sub(r'\s+', ' ', sentence)
                
                if self._is_valid_sentence(sentence):
                    valid_sentences.append({
                        'sentence_text': sentence,
                        'source_pdf': source_pdf,
                        'source_url': source_url
                    })
            
            logger.info(f"Extracted {len(valid_sentences)} valid sentences from {source_pdf}")
            return valid_sentences
            
        except Exception as e:
            logger.error(f"Failed to split text: {e}")
            return []
