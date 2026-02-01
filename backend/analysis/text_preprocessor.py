"""
Text Preprocessor Module
Handles text cleaning, tokenization, and preprocessing
"""
import logging
import re
from typing import List
from collections import Counter

logger = logging.getLogger(__name__)

class TextPreprocessor:
    """
    Text preprocessing utilities
    Supports both English and Chinese text
    """
    
    def __init__(self):
        # English stop words (basic set)
        self.english_stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'should', 'could', 'can', 'may', 'might', 'must', 'this',
            'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
        
        # Load Chinese stop words and jieba
        self.chinese_stopwords = set()
        self.jieba_available = False
        try:
            import jieba
            self.jieba = jieba
            self.jieba_available = True
            self.chinese_stopwords = {
                '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
                '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
                '你', '会', '着', '没有', '看', '好', '自己', '这', '那'
            }
            logger.info('Jieba loaded successfully for Chinese text processing')
        except ImportError:
            logger.warning('Jieba not available. Chinese tokenization will be limited.')
    
    def clean_text(self, text: str, remove_urls: bool = True, 
                   remove_special_chars: bool = True) -> str:
        """
        Clean text by removing unwanted elements
        
        Args:
            text: Input text
            remove_urls: Whether to remove URLs
            remove_special_chars: Whether to remove special characters
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove URLs
        if remove_urls:
            text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters (keep alphanumeric, spaces, and Chinese characters)
        if remove_special_chars:
            text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def remove_stopwords(self, text: str, language: str = 'english') -> str:
        """
        Remove stop words from text
        
        Args:
            text: Input text
            language: Language of the text ('english' or 'chinese')
            
        Returns:
            Text with stop words removed
        """
        words = text.lower().split()
        
        if language == 'english':
            filtered_words = [w for w in words if w not in self.english_stopwords]
        elif language == 'chinese':
            # Use jieba for Chinese word segmentation if available
            if self.jieba_available:
                words = list(self.jieba.cut(text.lower()))
                filtered_words = [w for w in words if w not in self.chinese_stopwords and w.strip()]
            else:
                filtered_words = words
        else:
            filtered_words = words
        
        return ' '.join(filtered_words)
    
    def tokenize(self, text: str, language: str = 'english') -> List[str]:
        """
        Tokenize text into words
        
        Args:
            text: Input text
            language: Language of the text
            
        Returns:
            List of tokens
        """
        if language == 'english':
            # Simple whitespace tokenization for English
            return text.lower().split()
        elif language == 'chinese':
            # Use jieba for Chinese tokenization
            if self.jieba_available:
                return list(self.jieba.cut(text))
            else:
                # Fallback: character-level tokenization
                return list(text)
        else:
            return text.split()
    
    def preprocess_batch(self, texts: List[str], language: str = 'english') -> List[str]:
        """
        Preprocess a batch of texts
        
        Args:
            texts: List of input texts
            language: Language of the texts
            
        Returns:
            List of preprocessed texts
        """
        logger.info(f'Preprocessing {len(texts)} texts in {language}')
        
        processed = []
        for text in texts:
            cleaned = self.clean_text(text)
            no_stopwords = self.remove_stopwords(cleaned, language)
            processed.append(no_stopwords)
        
        return processed
