"""
AI-powered password analysis and categorization using OpenAI
"""

import os
import re
from openai import OpenAI

class AIPasswordAgent:
    def __init__(self):
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("⚠️  Warning: OPENAI_API_KEY not set. AI features will use fallback logic.")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)
    
    def categorize_service(self, service_name):
        """Categorize a service using AI or fallback logic"""
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a password manager assistant. Categorize services into one of these categories: work, personal, shopping, social, financial, entertainment, other. Respond with only the category name."},
                        {"role": "user", "content": f"Categorize this service: {service_name}"}
                    ],
                    max_tokens=10,
                    temperature=0.1
                )
                return response.choices[0].message.content.strip().lower()
            except Exception as e:
                print(f"AI categorization failed: {e}. Using fallback.")
        
        # Fallback categorization logic
        return self._fallback_categorize(service_name)
    
    def _fallback_categorize(self, service_name):
        """Simple rule-based categorization when AI is unavailable"""
        service_lower = service_name.lower()
        
        if any(word in service_lower for word in ['gmail', 'outlook', 'yahoo', 'work', 'office', 'slack', 'teams']):
            return 'work'
        elif any(word in service_lower for word in ['amazon', 'ebay', 'shop', 'store', 'buy']):
            return 'shopping'
        elif any(word in service_lower for word in ['bank', 'paypal', 'venmo', 'credit', 'finance']):
            return 'financial'
        elif any(word in service_lower for word in ['facebook', 'twitter', 'instagram', 'social']):
            return 'social'
        elif any(word in service_lower for word in ['netflix', 'spotify', 'youtube', 'game']):
            return 'entertainment'
        else:
            return 'personal'
    
    def analyze_password_strength(self, password, service_name):
        """Analyze password strength and provide suggestions"""
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a cybersecurity expert. Analyze the password strength and provide specific improvement suggestions. Be concise but helpful."},
                        {"role": "user", "content": f"Analyze this password for {service_name}: '{password}'. Rate its strength and suggest improvements."}
                    ],
                    max_tokens=200,
                    temperature=0.3
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"AI analysis failed: {e}. Using fallback.")
        
        # Fallback analysis
        return self._fallback_analyze_password(password)
    
    def _fallback_analyze_password(self, password):
        """Simple rule-based password analysis"""
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("• Password should be at least 8 characters long")
        
        # Character variety checks
        if re.search(r'[a-z]', password):
            score += 1
        else:
            feedback.append("• Add lowercase letters")
            
        if re.search(r'[A-Z]', password):
            score += 1
        else:
            feedback.append("• Add uppercase letters")
            
        if re.search(r'\d', password):
            score += 1
        else:
            feedback.append("• Add numbers")
            
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
        else:
            feedback.append("• Add special characters")
        
        # Strength rating
        if score >= 5:
            strength = "Strong 💪"
        elif score >= 3:
            strength = "Moderate ⚡"
        else:
            strength = "Weak ⚠️"
        
        result = f"Strength: {strength} (Score: {score}/6)\n"
        if feedback:
            result += "\nSuggestions for improvement:\n" + "\n".join(feedback)
        else:
            result += "\n✓ This password meets basic security requirements!"
            
        return result