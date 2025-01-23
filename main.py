import os
from dotenv import load_dotenv
from api_client import NEETTestlineAPIClient
from performance_analyzer import StudentPerformanceAnalyzer
from ml_recommender import MLRecommendationEngine
from visualizer import PerformanceVisualizer
from logger import NEETAnalyticsLogger

def main():
    # Setup logging
    logger = NEETAnalyticsLogger.setup_logging()
    
    # Load environment variables
    load_dotenv()
    
    try:
        # API integration
        user_id = os.getenv('NEET_USER_ID')
        if not user_id:
            raise ValueError("No user ID found in environment variables")
        
        api_client = NEETTestlineAPIClient()
        current_quiz = api_client.get_current_quiz_data(user_id)
        historical_data = api_client.get_historical_quiz_data(user_id)
        
        # Performance analysis
        analyzer = StudentPerformanceAnalyzer(current_quiz, historical_data)
        insights = analyzer.analyze_performance()
        logger.info("Performance analysis completed")
        
        # Visualization
        PerformanceVisualizer.plot_topic_performance(insights['topic_performance'])
        PerformanceVisualizer.plot_difficulty_progression({
            diff: {'scores': data['avg_score']} 
            for diff, data in insights['difficulty_performance'].items()
        })
        
        # ML Recommendations
        ml_engine = MLRecommendationEngine(historical_data)
        clustering = ml_engine.cluster_learning_patterns()
        
        # Print insights
        print("\n--- Student Performance Insights ---")
        print(f"Student Persona: {insights['student_persona']}")
        print("\nWeak Topics:", insights['weak_topics'])
        print("\nRecommendations:")
        for strategy in insights['improvement_recommendations']['study_strategies']:
            print(f"- {strategy}")
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise

if __name__ == "__main__":
    main()