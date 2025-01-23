import requests
import os
from dotenv import load_dotenv

class NEETTestlineAPIClient:
    def __init__(self):
        load_dotenv()
        self.base_url = os.getenv('NEET_API_BASE_URL')
        self.api_key = os.getenv('NEET_API_KEY')
    
    def get_current_quiz_data(self, user_id):
        # Mock data for current quiz
        return {
            'questions': [
                {'topic': 'Physics', 'difficulty': 'Medium'},
                {'topic': 'Chemistry', 'difficulty': 'Hard'},
                {'topic': 'Biology', 'difficulty': 'Easy'}
            ]
        }

    def get_historical_quiz_data(self, user_id, num_quizzes=5):
        return [
        {
            'topic_accuracies': {
                'Physics': 0.4, 
                'Chemistry': 0.3, 
                'Biology': 0.5,
                'Mathematics': 0.6
            },
            'difficulty_scores': {
                'Easy': 0.7, 
                'Medium': 0.5, 
                'Hard': 0.3
            }
        },
        {
            'topic_accuracies': {
                'Physics': 0.5, 
                'Chemistry': 0.4, 
                'Biology': 0.6,
                'Mathematics': 0.7
            },
            'difficulty_scores': {
                'Easy': 0.8, 
                'Medium': 0.6, 
                'Hard': 0.4
            }
        }
    ]
    
    def _get_headers(self):
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }