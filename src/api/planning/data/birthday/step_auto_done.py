auto_done_json = {
    "session_id": "ff8f8f4d-9b13-4632-92c8-643118d60de7",
    "screens": [
        {
            "name": "main",
            "key": "5f5322d01b615a784b1076f8f4e44013",
            "state": "active",
            "title": "Create a party plan",
            "description": "Overview of the party plan creation process.",
            "icon": "",
            "focus": "I want to create a party plan",
            "interaction_value": "",
            "interaction_template": "",
            "cards": [
                {
                    "name": "AgentPerformance",
                    "key": "bfd0489d686d747d",
                    "state": "active",
                    "title": "Coordination Agent",
                    "description": "",
                    "focus": "",
                    "icon": "https://dopniceu5am9m.cloudfront.net/static/planning/new_icon/hotel.png",
                    "interaction_value": "",
                    "interaction_template": "",
                    "loading": False,
                    "metadata": {
                        "completed": True,
                        "subtitle": "Gathering party details",
                        "action_model_screen": {"app_icon": "", "start_time": "345325325"},
                    },
                },
                {
                    "name": "PartyCollectedInfo",
                    "key": "b07ba0b01b120aa8",
                    "state": "active",
                    "title": "Collected Information",
                    "description": "Party details summary",
                    "focus": "",
                    "icon": "https://dopniceu5am9m.cloudfront.net/static/planning/new_icon/hotel.png",
                    "interaction_value": "",
                    "interaction_template": "",
                    "loading": False,
                    "metadata": {
                        "widgets": [
                            {
                                "name": "Address",
                                "metadata": {
                                    "address_detail": "富士山下的小酒馆",
                                    "address_location": "39.983424,116.322987",
                                    "party_name": "Unicorn Adventure",
                                    "start_time": "Sat, July 15th, 2:00 PM - 5:00 PM",
                                },
                            },
                            {
                                "name": "Allergies",
                                "metadata": {"allergies": ["Tommy (nut allergy) ", "Emma (dairy-free)"]},
                            },
                            {"name": "Attendees", "metadata": {"attendees": 8, "ages": "7-9"}},
                        ]
                    },
                },
                {
                    "name": "PartyChooseMeal",
                    "key": "b07ba0b01b120aa4",
                    "state": "inactive",
                    "title": "Choose Your Meal",
                    "description": "",
                    "focus": "",
                    "icon": "https://dopniceu5am9m.cloudfront.net/static/planning/new_icon/hotel.png",
                    "interaction_value": "{{meal}}",
                    "interaction_template": "",
                    "loading": False,
                    "metadata": {
                        "subtitle": "Allergy-safe meal options",
                        "status_text": "Waiting for agent",
                        "recipes": [],
                        "buttons": [
                            {
                                "key": "01c001",
                                "title": "Confirm",
                                "description": "",
                                "interactions": [
                                    {
                                        "type": "onChooseMealConfirm",
                                        "title": "Confirm",
                                        "description": "User clicked Confirm",
                                        "value": "Adfwe01,Bsadf92",
                                        "relation_key": "b07ba0b01b1 20aa2",
                                    }
                                ],
                            }
                        ],
                    },
                },
                {
                    "name": "PartyRestaurant",
                    "key": "1ad3ebb8a0fdb912",
                    "state": "active",
                    "title": "Venue",
                    "description": "",
                    "focus": "",
                    "icon": "https://dopniceu5am9m.cloudfront.net/static/planning/new_icon/hotel.png",
                    "interaction_value": "",
                    "interaction_template": "",
                    "loading": False,
                    "metadata": {
                        "status_text": "Waiting for agent",
                        "params": {"keyword": "焼肉", "location": "東京"},
                        "find_restaurants": "https://plan-dev.api.brain.ai/v1.0/invoke/composite-api/method/restaurant/find-restaurants?location={LOCATION}&keyword={KEYWORD}",
                        "get_restaurant_detail": "https://plan-dev.api.brain.ai/v1.0/invoke/composite-api/method/restaurant/get-restaurant-detail?restaurant_id={RESTAURANT_ID}",
                    },
                },
            ],
        }
    ],
}
