"""
Health Chatbot - Semantic Similarity Based Question Answering System
Implements TF-IDF and cosine similarity for intelligent health query matching
"""

import json
import numpy as np
from typing import Dict, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from datetime import datetime


class HealthChatbot:
    """
    Health Chatbot using TF-IDF and cosine similarity for semantic matching.
    Provides answers with confidence scores and explanations.
    """
    
    def __init__(self, dataset_path: str, confidence_threshold: float = 0.3):
        """
        Initialize the chatbot with dataset.
        
        Args:
            dataset_path: Path to JSON dataset with Q&A pairs
            confidence_threshold: Minimum similarity score for valid answers (0-1)
        """
        self.confidence_threshold = confidence_threshold
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            max_features=500,
            ngram_range=(1, 2)
        )
        
        # Load dataset
        self.qa_pairs = self._load_dataset(dataset_path)
        self.questions = [qa['question'].lower() for qa in self.qa_pairs]
        
        # Build TF-IDF matrix for questions
        self.tfidf_matrix = self.vectorizer.fit_transform(self.questions)
        
        # Store conversation history
        self.conversation_history = []
        
        print(f"✓ Chatbot initialized with {len(self.qa_pairs)} Q&A pairs")
        print(f"✓ Confidence threshold: {self.confidence_threshold}")
        print(f"✓ TF-IDF vocabulary size: {len(self.vectorizer.get_feature_names_out())}\n")
    
    def _load_dataset(self, dataset_path: str) -> List[Dict]:
        """Load Q&A dataset from JSON file."""
        try:
            with open(dataset_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data['qa_pairs']
        except FileNotFoundError:
            raise FileNotFoundError(f"Dataset not found: {dataset_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in dataset: {dataset_path}")
    
    def _extract_keywords_from_query(self, query: str) -> List[str]:
        """Extract important keywords from query for explanation."""
        # Remove common words and extract meaningful keywords
        stop_words = {'what', 'is', 'the', 'a', 'an', 'how', 'to', 'for', 'can', 'do', 'about', 'are', 'symptoms', 'treatment', 'prevent', 'prevention'}
        words = re.findall(r'\b\w+\b', query.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return keywords
    
    def _get_matched_keywords(self, query_keywords: List[str], qa_id: int) -> List[str]:
        """Find which keywords matched from the Q&A pair."""
        qa_keywords = set(self.qa_pairs[qa_id]['keywords'])
        matched = [kw for kw in query_keywords if kw in qa_keywords]
        return matched
    
    def answer_query(self, query: str, return_top_n: int = 3) -> Dict:
        """
        Answer a health query with similarity scores and explanations.
        
        Args:
            query: User's health question
            return_top_n: Number of top results to consider (default: 3)
            
        Returns:
            Dictionary with answer, confidence, explanation, and alternatives
        """
        query_lower = query.lower().strip()
        
        if not query_lower:
            return self._get_fallback_response("Please enter a valid question.")
        
        # Vectorize the query using same TF-IDF
        query_vector = self.vectorizer.transform([query_lower])
        
        # Calculate cosine similarity with all questions
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)[0]
        
        # Get top matches
        top_indices = np.argsort(similarities)[::-1][:return_top_n]
        top_scores = similarities[top_indices]
        
        # Extract keywords for explanation
        query_keywords = self._extract_keywords_from_query(query)
        
        # Main result
        best_idx = top_indices[0]
        best_score = top_scores[0]
        
        # Create response
        if best_score >= self.confidence_threshold:
            best_qa = self.qa_pairs[best_idx]
            matched_keywords = self._get_matched_keywords(query_keywords, best_idx)
            
            response = {
                'success': True,
                'answer': best_qa['answer'],
                'confidence': float(best_score),
                'question_id': best_qa['id'],
                'category': best_qa['category'],
                'matched_question': best_qa['question'],
                'explanation': self._generate_explanation(
                    best_score, 
                    best_qa, 
                    query_keywords,
                    matched_keywords
                ),
                'alternatives': self._get_alternatives(top_indices[1:], top_scores[1:]),
                'similarity_scores': {
                    'best_match': float(best_score),
                    'all_top_3': [float(s) for s in top_scores]
                }
            }
        else:
            response = self._get_fallback_response(
                f"Confidence too low (score: {best_score:.2%}). Please rephrase or consult a medical professional."
            )
            response['similarity_scores'] = {
                'best_match': float(best_score),
                'all_top_3': [float(s) for s in top_scores]
            }
        
        # Store in history
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response
        })
        
        return response
    
    def _generate_explanation(self, 
                             similarity_score: float, 
                             qa_pair: Dict, 
                             query_keywords: List[str],
                             matched_keywords: List[str]) -> str:
        """Generate human-readable explanation for the answer."""
        explanation = f"Similarity Score: {similarity_score:.1%}\n"
        explanation += f"Category: {qa_pair['category'].replace('-', ' ').title()}\n"
        
        if matched_keywords:
            explanation += f"Matched Keywords: {', '.join(matched_keywords)}\n"
        
        explanation += f"Original Question: {qa_pair['question']}\n"
        explanation += f"Why This Match: High textual similarity between your query and this Q&A pair."
        
        return explanation
    
    def _get_alternatives(self, alt_indices: np.ndarray, alt_scores: np.ndarray) -> List[Dict]:
        """Get alternative answers if confidence is low."""
        alternatives = []
        for idx, score in zip(alt_indices, alt_scores):
            if score > 0.1:  # Show alternatives with minimal relevance
                qa = self.qa_pairs[idx]
                alternatives.append({
                    'answer': qa['answer'],
                    'confidence': float(score),
                    'question': qa['question'],
                    'category': qa['category']
                })
        return alternatives
    
    def _get_fallback_response(self, message: str = None) -> Dict:
        """Return a safe fallback response."""
        if message is None:
            message = "I'm not confident about this answer. Please consult a qualified medical professional for accurate health advice."
        
        return {
            'success': False,
            'answer': message,
            'confidence': 0.0,
            'question_id': -1,
            'category': 'fallback',
            'matched_question': None,
            'explanation': "Low confidence match - using fallback response.",
            'alternatives': []
        }
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the conversation history."""
        return self.conversation_history
    
    def get_similarity_scores_for_testing(self, test_queries: List[str]) -> List[float]:
        """
        Get similarity scores for multiple test queries (for visualization).
        
        Args:
            test_queries: List of test queries
            
        Returns:
            List of best similarity scores for each query
        """
        scores = []
        for query in test_queries:
            query_vector = self.vectorizer.transform([query.lower()])
            similarities = cosine_similarity(query_vector, self.tfidf_matrix)[0]
            best_score = np.max(similarities)
            scores.append(float(best_score))
        return scores
    
    def batch_answer(self, queries: List[str]) -> List[Dict]:
        """Answer multiple queries at once."""
        return [self.answer_query(q) for q in queries]
    
    def print_response(self, response: Dict) -> str:
        """Pretty print a chatbot response."""
        output = "\n" + "="*70 + "\n"
        
        if response['success']:
            output += f"✓ ANSWER\n"
            output += f"{response['answer']}\n\n"
            output += f"📊 EXPLANATION\n"
            output += f"{response['explanation']}\n"
        else:
            output += f"⚠ FALLBACK RESPONSE\n"
            output += f"{response['answer']}\n"
        
        output += "\n" + "="*70 + "\n"
        return output


def main():
    """Demo of the chatbot."""
    # Initialize chatbot
    chatbot = HealthChatbot(
        dataset_path='data/health_qa_dataset.json',
        confidence_threshold=0.3
    )
    
    # Test queries
    test_queries = [
        "What causes dengue fever?",
        "How can I prevent malaria?",
        "Tell me about COVID-19 symptoms",
        "I have a fever and body aches",
        "What is the treatment for diabetes?",
        "xyz abc random text",  # Low confidence test
    ]
    
    print("\n" + "="*70)
    print("HEALTH CHATBOT - DEMO")
    print("="*70 + "\n")
    
    for query in test_queries:
        print(f"USER: {query}")
        response = chatbot.answer_query(query)
        print(chatbot.print_response(response))


if __name__ == "__main__":
    main()
