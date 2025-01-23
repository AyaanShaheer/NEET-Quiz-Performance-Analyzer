import pandas as pd
import numpy as np
from typing import Dict, List, Any
from collections import defaultdict

class StudentPerformanceAnalyzer:
    def __init__(self, current_quiz_data: Dict, historical_quiz_data: List[Dict]):
        """
        Initialize the analyzer with current and historical quiz data
        
        :param current_quiz_data: Dict containing latest quiz submission details
        :param historical_quiz_data: List of dictionaries with past quiz performances
        """
        self.current_quiz = pd.DataFrame(current_quiz_data.get('questions', []))
        self.historical_quizzes = historical_quiz_data
        
        # Performance tracking
        self.topic_performance = defaultdict(list)
        self.difficulty_performance = defaultdict(list)
        
    def analyze_performance(self) -> Dict[str, Any]:
        """
        Comprehensive performance analysis
        
        :return: Dictionary with detailed performance insights
        """
        # Topic-wise performance analysis
        self._calculate_topic_performance()
        
        # Difficulty level analysis
        self._analyze_difficulty_levels()
        
        # Identify weak areas
        weak_topics = self._identify_weak_topics()
        
        # Student persona classification
        persona = self._classify_student_persona()
        
        return {
            'topic_performance': dict(self.topic_performance),
            'difficulty_performance': self.difficulty_performance,
            'weak_topics': weak_topics,
            'student_persona': persona,
            'improvement_recommendations': self._generate_recommendations()
        }
    
    def _calculate_topic_performance(self):
        """
        Calculate performance metrics for each topic
        """
        for quiz in self.historical_quizzes:
            for topic, accuracy in quiz.get('topic_accuracies', {}).items():
                self.topic_performance[topic].append(accuracy)
    
    def _analyze_difficulty_levels(self):
        """
        Analyze performance across different difficulty levels
        """
        difficulty_scores = defaultdict(list)
        for quiz in self.historical_quizzes:
            for diff, score in quiz.get('difficulty_scores', {}).items():
                difficulty_scores[diff].append(score)
        
        self.difficulty_performance = {
            diff: {
                'avg_score': np.mean(scores) if scores else 0,
                'improvement_trend': np.polyfit(range(len(scores)), scores, 1)[0] if len(scores) > 1 else 0
            }
            for diff, scores in difficulty_scores.items()
        }
    
    def _identify_weak_topics(self) -> List[str]:
        """
        Identify topics with consistently low performance
        
        :return: List of weak topics
        """
        weak_topics = []
        for topic, performances in self.topic_performance.items():
            avg_performance = np.mean(performances) if performances else 0
            if avg_performance < 0.5:  # Below 50% accuracy
                weak_topics.append(topic)
        
        return weak_topics
    
    def _classify_student_persona(self) -> str:
        """
        Classify student's learning persona based on performance patterns
        
        :return: Student persona description
        """
        # Analyze overall performance and learning characteristics
        topic_means = [np.mean(perf) for perf in self.topic_performance.values() if perf]
        overall_avg = np.mean(topic_means) if topic_means else 0
        performance_variability = np.std(topic_means) if topic_means else 0
        
        if overall_avg > 0.8:
            return "High Achiever: Consistently strong performer"
        elif 0.6 < overall_avg <= 0.8:
            if performance_variability > 0.2:
                return "Inconsistent Learner: Potential for improvement with focused study"
            else:
                return "Steady Performer: Reliable across topics"
        else:
            return "Emerging Learner: Needs comprehensive support and targeted interventions"
    
    def _generate_recommendations(self) -> Dict[str, Any]:
        """
        Generate personalized study recommendations
        
        :return: Dictionary of recommendations
        """
        recommendations = {
            'focus_topics': self._identify_weak_topics(),
            'suggested_difficulty': self._recommend_difficulty_level(),
            'study_strategies': self._develop_study_strategies()
        }
        return recommendations
    
    def _recommend_difficulty_level(self) -> str:
        """
        Recommend appropriate difficulty level
        
        :return: Recommended difficulty level
        """
        # Find the difficulty level with lowest performance
        if not self.difficulty_performance:
            return "Medium"
        
        lowest_perf_diff = min(
            self.difficulty_performance.items(), 
            key=lambda x: x[1]['avg_score']
        )[0]
        
        return lowest_perf_diff
    
    def _develop_study_strategies(self) -> List[str]:
        """
        Develop personalized study strategies
        
        :return: List of study recommendations
        """
        strategies = []
        
        # Weak topics strategy
        weak_topics = self._identify_weak_topics()
        if weak_topics:
            strategies.append(f"Focus on mastering weak topics: {', '.join(weak_topics)}")
        
        # Difficulty level strategy
        recommended_diff = self._recommend_difficulty_level()
        strategies.append(f"Practice {recommended_diff} level questions to build confidence")
        
        # Additional personalized strategies
        if self._classify_student_persona() == "Inconsistent Learner":
            strategies.append("Develop a consistent study routine with regular mock tests")
        
        return strategies