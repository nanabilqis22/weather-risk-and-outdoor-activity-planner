from weather_client import Forecast

class ActivityRiskAnalyzer:
    def analyze_risk(self, forecast: Forecast, activity: str) -> str:
        """
        Task: Explain whether the activity is safe, manageable, risky, or should be avoided.
        """
        print(f"[System] Analyzing risk for activity: {activity}...")
        # TODO: Add risk analysis logic rules here
        return "Safe"


class RecommendationEngine:
    def generate_checklist(self, activity: str, risk_level: str) -> list:
        """
        Task: Generate a packing checklist, best time of day, and safety advice.
        Must apply: Regular expressions to clean text or validate inputs.
        """
        # TODO: Add packing list and regex validation logic here
        return []