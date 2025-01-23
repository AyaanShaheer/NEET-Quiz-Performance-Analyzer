from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np

class MLRecommendationEngine:
    def __init__(self, historical_data):
        self.historical_data = historical_data
        self.scaler = StandardScaler()
    
    def cluster_learning_patterns(self):
        """Cluster students based on learning characteristics"""
        features = self._extract_learning_features()
        
        if len(features) == 0:
            return {
                'clusters': [],
                'cluster_centroids': None
            }
        
        scaled_features = self.scaler.fit_transform(features)
        
        # Determine optimal number of clusters
        n_clusters = min(3, len(scaled_features))
        
        # Use K-means for clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(scaled_features)
        
        return {
            'clusters': clusters,
            'cluster_centroids': kmeans.cluster_centers_
        }
    
    def _extract_learning_features(self):
        """Extract key learning pattern features"""
        features = []
        for quiz in self.historical_data:
            topic_accuracies = quiz.get('topic_accuracies', {})
            difficulty_scores = quiz.get('difficulty_scores', {})
            
            if not topic_accuracies or not difficulty_scores:
                continue
            
            feature_vector = [
                np.mean(list(topic_accuracies.values())),
                np.std(list(topic_accuracies.values())),
                np.mean(list(difficulty_scores.values()))
            ]
            features.append(feature_vector)
        
        return np.array(features)
    
    def generate_advanced_recommendations(self, cluster):
        """Generate cluster-specific recommendations"""
        recommendation_map = {
            0: "Focus on consistent study across topics",
            1: "Targeted practice on weak subject areas",
            2: "Advanced problem-solving strategies"
        }
        return recommendation_map.get(cluster, "General study guidance")