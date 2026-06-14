import re
from weather_client import Forecast

class ActivityRiskAnalyzer:
    def analyze_risk(self, forecast: Forecast, activity: str) -> str:
        """
        Evaluates weather conditions against the planned activity to determine risk level.
        Returns: 'Low Risk', 'Moderate Risk', or 'High Risk / Avoid'
        """
        print(f"[Analyzer] Evaluating conditions for: {activity}...")
        
        condition = forecast.condition.lower()
        temp = forecast.temperature

        # Severe weather rules
        if "thunderstorm" in condition:
            return "High Risk / Avoid (Danger of lightning strikes outdoor)"
        
        if "rainy" in condition:
            # High impact outdoor sports are unsafe in rain
            if any(sport in activity.lower() for sport in ["football", "basketball", "tennis", "cycling"]):
                return "High Risk / Avoid (Slippery surfaces and poor visibility)"
            return "Moderate Risk (Bring protective rain gear)"

        # Temperature rules
        if temp > 38:
            return "High Risk / Avoid (Extreme heatwave warning)"
        elif temp > 30:
            return "Moderate Risk (High temperature, stay hydrated)"
        elif temp < 10:
            return "Moderate Risk (Chilly weather, dress warmly)"
            
        return "Low Risk (Conditions look beautiful for this activity!)"


class RecommendationEngine:
    def generate_checklist(self, activity: str, risk_level: str) -> list:
        """
        Uses Regular Expressions to sanitize the activity string, 
        then builds a customized safety packing list.
        """
        # Use Regex to remove any numbers or symbols from the activity string
        clean_activity = re.sub(r'[^a-zA-Z\s]', '', activity).strip().lower()
        
        # Default packing items
        checklist = ["Water bottle", "Fully charged phone"]
        
        # Add items based on risk level keywords
        if "avoid" in risk_level.lower():
            checklist.append("Indoor backup venue plan")
        elif "moderate" in risk_level.lower():
            checklist.append("First-aid kit copy")
            
        # Add items based on the specific activity type
        if any(word in clean_activity for word in ["football", "basketball", "sports", "run"]):
            checklist.extend(["Athletic shoes", "Towel", "Electrolyte drink"])
        elif any(word in clean_activity for word in ["picnic", "park", "relax"]):
            checklist.extend(["Sitting mat", "Snacks", "Sunscreen"])
            
        return checklist