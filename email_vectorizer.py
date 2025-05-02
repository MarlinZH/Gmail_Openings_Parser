from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import numpy as np
from datetime import datetime

class EmailVectorizer:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the email vectorizer
        Args:
            model_name: Name of the sentence transformer model to use
        """
        self.model = SentenceTransformer(model_name)
        
    def vectorize_email(self, email_data: Dict) -> Dict:
        """
        Vectorize email content and metadata
        Args:
            email_data: Dictionary containing email information
        Returns:
            Dictionary with added vector field
        """
        # Combine relevant fields for vectorization
        text_to_vectorize = f"{email_data.get('subject', '')} {email_data.get('content', '')}"
        
        # Generate vector embedding
        vector = self.model.encode(text_to_vectorize)
        
        # Add vector to email data
        email_data['vector'] = vector.tolist()
        email_data['vector_timestamp'] = datetime.now().isoformat()
        
        return email_data
    
    def find_similar_emails(self, email_data: Dict, existing_emails: List[Dict], 
                          threshold: float = 0.7) -> List[Dict]:
        """
        Find similar emails based on vector similarity
        Args:
            email_data: Current email data
            existing_emails: List of existing emails with vectors
            threshold: Similarity threshold (0-1)
        Returns:
            List of similar emails
        """
        if 'vector' not in email_data:
            email_data = self.vectorize_email(email_data)
            
        current_vector = np.array(email_data['vector'])
        similar_emails = []
        
        for existing_email in existing_emails:
            if 'vector' not in existing_email:
                continue
                
            existing_vector = np.array(existing_email['vector'])
            similarity = np.dot(current_vector, existing_vector) / (
                np.linalg.norm(current_vector) * np.linalg.norm(existing_vector)
            )
            
            if similarity >= threshold:
                similar_emails.append({
                    'email': existing_email,
                    'similarity': float(similarity)
                })
        
        # Sort by similarity score
        similar_emails.sort(key=lambda x: x['similarity'], reverse=True)
        return similar_emails 