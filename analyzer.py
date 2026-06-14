import re
from weather_client import Forecast

class ActivityRiskAnalyzer:
    def analyze_risk(self, forecast: Forecast, activity: str) -> dict:
        """
        Uses explicit conditional logic to evaluate base safety metrics.
        """
        condition = forecast.condition.lower()
        temp = forecast.temperature
        
        # Base safety determination rules
        if "thunderstorm" in condition or temp > 40 or temp < 5:
            assessment = "Should be Avoided"
            advice = "Conditions present immediate environmental hazards. It is highly advised to cancel or move indoors."
            best_time = "Not recommended for today"
        elif "rainy" in condition or temp > 33 or temp < 12:
            assessment = "Risky / Manageable with caution"
            advice = "Suboptimal elements present. Dress appropriately, bring protective gear, and monitor changing skies."
            best_time = "Late afternoon if elements calm down"
        else:
            assessment = "Completely Safe"
            advice = "Atmospheric conditions match outdoor recreation requirements perfectly. Have fun!"
            best_time = "Morning or early evening hours"
            
        return {"assessment": assessment, "advice": advice, "best_time": best_time}

class RecommendationEngine:
    def generate_checklist(self, activity: str, assessment: str) -> list:
        """
        Applies Regular Expressions to scrub data and structures a packing inventory.
        """
        # Clean text: remove numbers and special symbols
        clean_act = re.sub(r'[^a-zA-Z\s]', '', activity).strip().lower()
        
        checklist = ["Water bottle", "Charged cell phone", "Identification card"]
        
        if "avoid" in assessment.lower() or "risky" in assessment.lower():
            checklist.append("Emergency umbrella / rain coat")
            checklist.append("Indoor location alternative key")
            
        if any(w in clean_act for w in ["football", "jogging", "sports", "running"]):
            checklist.extend(["Athletic footwear", "Towel", "Electrolytes"])
        elif any(w in clean_act for w in ["farming", "garden"]):
            checklist.extend(["Working gloves", "Sturdy boots", "Sun protective hat"])
        elif any(w in clean_act for w in ["picnic", "travelling", "event"]):
            checklist.extend(["Sitting sheet", "Packed snacks", "Sunscreen cream"])
            
        return checklist