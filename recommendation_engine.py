class RecommendationEngine:
    def packing_list(self, activity):
        packs = {
            "running": [
                "Water bottle",
                "Running shoes",
                "Fitness tracker",
                "Towel"
            ],
            "farming": [
                "Hat",
                "Gloves",
                "Boots",
                "Sunscreen",
                "Water bottle"
            ],
            "picnic": [
                "Food",
                "Water",
                "Blanket",
                "Napkins",
                "Sunscreen"
            ],
            "travelling": [
                "ID Card",
                "Phone Charger",
                "Water",
                "Passport",
                "Headphones"
            ],
            "outdoor event": [
                "Umbrella",
                "Water",
                "Sunscreen",
                "Folding chair",
                "Sunglasses"
            ]
        }

        return packs.get(activity.lower(), [])