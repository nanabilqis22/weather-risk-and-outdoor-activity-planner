class RecommendationEngine:
    
    def get_advice(self, activity, risk):

        advice = {
            "Safe": "Weather conditions are suitable.",
            "Manageable": "Proceed with caution.",
            "Risky": "Be careful and monitor conditions.",
            "Avoid": "Postpone the activity."
        }

        return advice.get(risk)

    def packing_list(self, activity):

        packs = {
            "Football": [
                "Water",
                "Boots",
                "Sportswear"
            ],
            "Jogging": [
                "Water bottle",
                "Running shoes"
            ],
            "Farming": [
                "Hat",
                "Gloves",
                "Boots"
            ],
            "Picnic": [
                "Food",
                "Water",
                "Blanket"
            ],
            "Travelling": [
                "ID Card",
                "Phone Charger",
                "Water"
            ],
            "Outdoor Event": [
                "Umbrella",
                "Water",
                "Sunscreen"
            ]
        }

        return packs.get(activity, [])