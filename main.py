from weather_client import WeatherClient
from analyzer import ActivityRiskAnalyzer, RecommendationEngine

def save_to_favorites(location: str):
    """
    Task: Save favorite locations or previous weather searches locally.
    Must apply: File handling (writing to a text/JSON file).
    """
    print(f"[System] Saving {location} to favorites...")
    # TODO: Implement file writing code here
    pass

def main():
    print("=== Welcome to the Weather Risk & Outdoor Activity Planner ===")
    
    # Get user inputs
    location = input("Enter location (e.g., Abuja): ")
    activity = input("Enter outdoor activity (e.g., football, picnic): ")
    
    print(f"\nLocation: {location}")
    print(f"Activity: {activity}")
    print("[System] Project skeleton is running successfully!")

if __name__ == "__main__":
    main()