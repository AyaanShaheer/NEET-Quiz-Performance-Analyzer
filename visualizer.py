import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

class PerformanceVisualizer:
    @staticmethod
    def plot_topic_performance(topic_performances):
        """Create a bar chart of topic performances"""
        # Ensure output directory exists
        os.makedirs('reports', exist_ok=True)
        
        # Convert topic performances to a DataFrame
        df = pd.DataFrame.from_dict({
            topic: {'average_score': sum(scores) / len(scores)} 
            for topic, scores in topic_performances.items()
        }, orient='index')
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x=df.index, y='average_score', data=df)
        plt.title('Topic Performance Analysis')
        plt.xlabel('Topics')
        plt.ylabel('Average Score')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('reports/topic_performance.png')
        plt.close()
    
    @staticmethod
    def plot_difficulty_progression(difficulty_data):
        """Visualize performance across difficulty levels"""
        # Ensure output directory exists
        os.makedirs('reports', exist_ok=True)
        
        plt.figure(figsize=(10, 6))
        for difficulty, data in difficulty_data.items():
            plt.plot(data['scores'], label=difficulty)
        
        plt.title('Performance Across Difficulty Levels')
        plt.xlabel('Quiz Attempts')
        plt.ylabel('Score')
        plt.legend()
        plt.tight_layout()
        plt.savefig('reports/difficulty_progression.png')
        plt.close()