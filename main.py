from weather_client import WeatherClient
from analyzer import ActivityRiskAnalyzer, RecommendationEngine

def save_to_history(location: str, activity: str):
    """
    Task: Save user searches locally using File Handling.
    Appends the location and activity to 'search_history.txt'.
    """
    try:
        # 'a' means append mode, so it keeps old data and adds new data to the end
        with open("search_history.txt", "a") as file:
            file.write(f"Location: {location} | Activity: {activity}\n")
        print("[System] Search saved successfully to 'search_history.txt'.")
    except Exception as e:
        print(f"[Error] Could not save to history: {e}")

def view_history():
    """
    Task: Read and display the saved search history file.
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
    while True:
        print("\n=== Weather Risk & Outdoor Activity Planner ===")
        print("1. Plan an Activity")
        print("2. View Search History")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ")
        
        if choice == "1":
            location = input("Enter location (e.g., Abuja): ").strip()
            activity = input("Enter outdoor activity (e.g., Football): ").strip()
            
            if not location or not activity:
                print("[Warning] Location and Activity cannot be blank!")
                continue
                
            print(f"\n[Processing] Location: {location}")
            print(f"[Processing] Activity: {activity}")
            
            # Save this data to your local text file
            save_to_history(location, activity)
            
            print("\n[System] (Note: Weather analysis will display once your teammates complete their files!)")
            
        elif choice == "2":
            view_history()
            
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("[Invalid Option] Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()