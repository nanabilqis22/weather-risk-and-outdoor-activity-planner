from weather_client import WeatherClient
from analyzer import ActivityRiskAnalyzer, RecommendationEngine

def save_to_history(location: str, activity: str, condition: str, temp: float, risk: str):
    """
    Saves user searches and the live results locally using File Handling.
    """
    try:
        with open("search_history.txt", "a") as file:
            file.write(f"Location: {location} | Activity: {activity} | Weather: {temp}°C, {condition} | Risk: {risk}\n")
        print("[System] Search log successfully saved to 'search_history.txt'.")
    except Exception as e:
        print(f"[Error] Could not save to history: {e}")

def view_history():
    """
    Reads and displays the saved search history file.
    """
    print("\n--- Saved Search History ---")
    try:
        with open("search_history.txt", "r") as file:
            history = file.read()
            if history.strip() == "":
                print("No history found.")
            else:
                print(history)
    except FileNotFoundError:
        print("No history file found yet. Try making a search first!")
    print("----------------------------\n")

def main():
    # Initialize the engine modules you built
    client = WeatherClient()
    analyzer = ActivityRiskAnalyzer()
    engine = RecommendationEngine()
    
    while True:
        print("\n=== Weather Risk & Outdoor Activity Planner ===")
        print("1. Plan an Activity (Live Data)")
        print("2. View Search History")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ")
        
        if choice == "1":
            location = input("Enter location (e.g., Abuja): ").strip()
            activity = input("Enter outdoor activity (e.g., Football): ").strip()
            
            if not location or not activity:
                print("[Warning] Location and Activity cannot be blank!")
                continue
                
            # 1. Fetch live API weather data
            forecast = client.fetch_forecast(location)
            
            if forecast is None:
                print("[System] Could not process planning due to weather service error.")
                continue
                
            # 2. Run the logical rule checks
            risk_level = analyzer.analyze_risk(forecast, activity)
            
            # 3. Clean string with Regex and build the checklist
            checklist = engine.generate_checklist(activity, risk_level)
            
            # 4. Print Results beautifully to user terminal screen
            print("\n==============================================")
            print(f"☀️ LIVE WEATHER REPORT FOR: {location.upper()}")
            print(f"-> Temperature: {forecast.temperature}°C")
            print(f"-> Condition: {forecast.condition}")
            print(f"-> Wind Speed: {forecast.wind_speed} km/h")
            print("==============================================")
            print(f"📋 RISK ASSESSMENT FOR: '{activity}'")
            print(f"-> Result: {risk_level}")
            print("==============================================")
            print("🎒 RECOMMENDED SAFETY PACKING CHECKLIST:")
            for item in checklist:
                print(f" [ ] {item}")
            print("==============================================\n")
            
            # Save all the live details to your local file history
            save_to_history(location, activity, forecast.condition, forecast.temperature, risk_level)
            
        elif choice == "2":
            view_history()
            
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("[Invalid Option] Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()