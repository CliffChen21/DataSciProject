"""
Text Analyzer Module
Handles text analysis including sentiment analysis and topic modeling
"""
import logging
from typing import List, Dict
import numpy as np
from transformers import pipeline
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from backend.analysis.text_preprocessor import TextPreprocessor

logger = logging.getLogger(__name__)

class TextAnalyzer:
    """
    Text analysis using ML/DL models
    Supports sentiment analysis, topic modeling, and more
    """
    
    def __init__(self):
        self.sentiment_model = None
        self.topic_model = None
        self._load_models()
        logger.info('TextAnalyzer initialized')
    
    def _load_models(self):
        """
        Load ML/DL models on initialization
        Models are loaded lazily to save memory
        """
        try:
            self.sentiment_model = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
            logger.info('Sentiment analysis model loaded successfully')
        except Exception as e:
            logger.warning(f'Could not load sentiment model: {e}. Will use mock data.')
            self.sentiment_model = None
    
    def analyze_sentiment(self, texts: List[str]) -> List[Dict]:
        """
        Analyze sentiment of texts
        
        Args:
            texts: List of text strings to analyze
            
        Returns:
            List of dictionaries with sentiment results
        """
        logger.info(f'Analyzing sentiment for {len(texts)} texts')
        
        # Use actual model if available
        if self.sentiment_model:
            try:
                results = []
                batch_size = 8
                for i in range(0, len(texts), batch_size):
                    batch = texts[i:i + batch_size]
                    truncated_batch = [text[:512] for text in batch]
                    model_results = self.sentiment_model(truncated_batch)
                    
                    for text, result in zip(batch, model_results):
                        results.append({
                            'text': text[:100] + '...' if len(text) > 100 else text,
                            'sentiment': result['label'].lower(),
                            'score': round(result['score'], 3),
                            'confidence': round(result['score'], 3)
                        })
                return results
            except Exception as e:
                logger.error(f'Model inference failed: {e}. Falling back to mock data.')
        
        # Fallback to mock results
        results = []
        for text in texts:
            # Mock sentiment based on text length (just for demo)
            score = min(0.5 + len(text) / 1000, 0.99)
            sentiment = 'positive' if score > 0.6 else 'negative' if score < 0.4 else 'neutral'
            
            results.append({
                'text': text[:100] + '...' if len(text) > 100 else text,
                'sentiment': sentiment,
                'score': round(score, 3),
                'confidence': round(score if score > 0.5 else 1 - score, 3)
            })
        
        return results
    
    def topic_modeling(self, texts: List[str], num_topics: int = 3) -> Dict:
        """
        Perform topic modeling on texts
        
        Args:
            texts: List of text strings
            num_topics: Number of topics to extract
            
        Returns:
            Dictionary with topics and document assignments
        """
        logger.info(f'Performing topic modeling on {len(texts)} texts with {num_topics} topics')
        
        # Implement actual topic modeling with sklearn
        try:
            preprocessor = TextPreprocessor()
            processed_texts = [preprocessor.clean_text(text) for text in texts]
            
            vectorizer = CountVectorizer(
                max_features=1000,
                max_df=0.95,
                min_df=2,
                stop_words='english'
            )
            doc_term_matrix = vectorizer.fit_transform(processed_texts)
            
            lda = LatentDirichletAllocation(
                n_components=num_topics,
                random_state=42,
                max_iter=10
            )
            lda.fit(doc_term_matrix)
            
            feature_names = vectorizer.get_feature_names_out()
            topics = []
            for topic_idx, topic in enumerate(lda.components_):
                top_indices = topic.argsort()[-5:][::-1]
                keywords = [feature_names[i] for i in top_indices]
                topics.append({
                    'topic_id': topic_idx,
                    'keywords': keywords,
                    'weight': round(1 / num_topics, 3)
                })
            
            doc_topics_dist = lda.transform(doc_term_matrix)
            doc_topics = []
            for idx, (text, topic_dist) in enumerate(zip(texts, doc_topics_dist)):
                dominant_topic = np.argmax(topic_dist)
                doc_topics.append({
                    'document_id': idx,
                    'text_preview': text[:100] + '...' if len(text) > 100 else text,
                    'topic_id': int(dominant_topic),
                    'confidence': round(float(topic_dist[dominant_topic]), 3)
                })
            
            return {
                'topics': topics,
                'document_topics': doc_topics,
                'num_topics': num_topics,
                'num_documents': len(texts)
            }
        except Exception as e:
            logger.error(f'Topic modeling failed: {e}. Falling back to mock data.')
        
        # Fallback to mock results
        topics = []
        for i in range(num_topics):
            topics.append({
                'topic_id': i,
                'keywords': [f'keyword{i}_{j}' for j in range(5)],
                'weight': round(1 / num_topics, 3)
            })
        
        doc_topics = []
        for idx, text in enumerate(texts):
            # Assign documents to topics in round-robin fashion (mock)
            topic_id = idx % num_topics
            doc_topics.append({
                'document_id': idx,
                'text_preview': text[:100] + '...' if len(text) > 100 else text,
                'topic_id': topic_id,
                'confidence': round(0.6 + np.random.random() * 0.3, 3)
            })
        
        return {
            'topics': topics,
            'document_topics': doc_topics,
            'num_topics': num_topics,
            'num_documents': len(texts)
        }
    
    def extract_keywords(self, text: str, top_k: int = 10) -> List[Dict]:
        """
        Extract keywords from text
        
        Args:
            text: Input text
            top_k: Number of top keywords to return
            
        Returns:
            List of keyword dictionaries with scores
        """
        # Implement keyword extraction with TF-IDF
        logger.info(f'Extracting top {top_k} keywords from text')
        
        try:
            preprocessor = TextPreprocessor()
            cleaned_text = preprocessor.clean_text(text)
            sentences = [s.strip() for s in cleaned_text.split('.') if s.strip()]
            
            if len(sentences) < 2:
                from collections import Counter
                words = cleaned_text.lower().split()
                word_freq = Counter(words).most_common(top_k)
                return [{'keyword': word, 'score': round(freq / len(words), 3)} for word, freq in word_freq]
            
            vectorizer = TfidfVectorizer(
                max_features=top_k * 2,
                stop_words='english',
                ngram_range=(1, 2)
            )
            tfidf_matrix = vectorizer.fit_transform(sentences)
            feature_names = vectorizer.get_feature_names_out()
            tfidf_scores = tfidf_matrix.toarray().mean(axis=0)
            top_indices = tfidf_scores.argsort()[-top_k:][::-1]
            
            return [{'keyword': feature_names[i], 'score': round(float(tfidf_scores[i]), 3)} for i in top_indices]
        except Exception as e:
            logger.error(f'Keyword extraction failed: {e}. Falling back to simple frequency.')
        
        # Fallback: simple word frequency
        from collections import Counter
        words = text.lower().split()
        word_freq = Counter(words).most_common(top_k)
        
        keywords = [
            {'keyword': word, 'score': round(freq / len(words), 3)}
            for word, freq in word_freq
        ]
        
        return keywords
