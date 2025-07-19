party_manual_json = {
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
                    "name": "PartyStart",
                    "key": "b07ba0b01b120aa2",
                    "state": "{{party_start_state}}",
                    "title": "Party starts at",
                    "description": "",
                    "focus": "",
                    "icon": "https://dopniceu5am9m.cloudfront.net/static/planning/new_icon/notes_about.png",
                    "interaction_value": "{{party_start}}",
                    "interaction_template": "",
                    "loading": False,
                    "metadata": {
                        "onPartyStartSave": {
                            "key": "01001",
                            "title": "Save",
                            "description": "",
                            "interactions": [
                                {
                                    "type": "onPartyStartSave",
                                    "title": "Save",
                                    "description": "User clicked Save",
                                    "value": "",
                                    "relation_key": "b07ba0b01b120aa2",
                                }
                            ],
                        }
                    },
                },
                {
                    "name": "PartyAttendant",
                    "key": "b07ba0b01b120aa3",
                    "state": "{{party_attendant_state}}",
                    "title": "Who will attend",
                    "description": "",
                    "focus": "",
                    "icon": "https://dopniceu5am9m.cloudfront.net/static/planning/new_icon/notes_about.png",
                    "interaction_value": "{{party_attendant}}",
                    "interaction_template": "",
                    "loading": False,
                    "metadata": {
                        "onPartyAttendantSave": {
                            "key": "01001",
                            "title": "Save",
                            "description": "",
                            "interactions": [
                                {
                                    "type": "onPartyAttendantSave",
                                    "title": "Save",
                                    "description": "User clicked Save",
                                    "value": "",
                                    "relation_key": "b07ba0b01b120aa3",
                                }
                            ],
                        }
                    },
                },
                {
                    "name": "PartyAllergy",
                    "key": "0536555a9fdc981d",
                    "state": "{{party_allergy_state}}",
                    "title": "Allergies",
                    "description": "",
                    "focus": "",
                    "icon": "https://dopniceu5am9m.cloudfront.net/static/planning/new_icon/notes_about.png",
                    "interaction_value": "{{party_allergy}}",
                    "interaction_template": "",
                    "loading": False,
                    "metadata": {
                        "onPartyAllergySave": {
                            "key": "01001",
                            "title": "Save",
                            "description": "",
                            "interactions": [
                                {
                                    "type": "onPartyAllergySave",
                                    "title": "Save",
                                    "description": "User clicked Save",
                                    "value": "",
                                    "relation_key": "b07ba0b01b120aa4",
                                }
                            ],
                        }
                    },
                },
                {
                    "name": "GroceryList",
                    "key": "LA9B2cX5pQ44",
                    "state": "{{grocery_list_state}}",
                    "title": "Grocery List",
                    "description": "",
                    "focus": "",
                    "icon": "https://dopniceu5am9m.cloudfront.net/static/planning/new_icon/hotel.png",
                    "interaction_value": "{{grocery_list}}",
                    "interaction_template": "",
                    "loading": False,
                    "metadata": {
                        "grocery_list": [
                            {
                                "icon": "https://dopniceu5am9m.cloudfront.net/static/planning/new_icon/hotel.png",
                                "title": "Egg",
                                "subtitle": "1",
                            },
                            {
                                "icon": "https://dopniceu5am9m.cloudfront.net/static/planning/new_icon/hotel.png",
                                "title": "Tomatoes",
                                "subtitle": "80g",
                            },
                        ]
                    },
                },
            ],
        }
    ],
}

party_manual_reload_json = {
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
                    "name": "PartyStart",
                    "key": "b07ba0b01b120aa2",
                    "state": "inactive",
                    "title": "Party starts at",
                    "description": "",
                    "focus": "",
                    "icon": "https://dopniceu5am9m.cloudfront.net/static/planning/new_icon/notes_about.png",
                    "interaction_value": "{{party_start}}",
                    "interaction_template": "",
                    "loading": False,
                    "metadata": {
                        "onPartyStartSave": {
                            "key": "01001",
                            "title": "Save",
                            "description": "",
                            "interactions": [
                                {
                                    "type": "onPartyStartSave",
                                    "title": "Save",
                                    "description": "User clicked Save",
                                    "value": "",
                                    "relation_key": "b07ba0b01b120aa2",
                                }
                            ],
                        }
                    },
                },
                {
                    "name": "PartyAttendant",
                    "key": "b07ba0b01b120aa3",
                    "state": "inactive",
                    "title": "Who will attend",
                    "description": "",
                    "focus": "",
                    "icon": "https://dopniceu5am9m.cloudfront.net/static/planning/new_icon/notes_about.png",
                    "interaction_value": "{{party_attendant}}",
                    "interaction_template": "",
                    "loading": False,
                    "metadata": {
                        "onPartyAttendantSave": {
                            "key": "01001",
                            "title": "Save",
                            "description": "",
                            "interactions": [
                                {
                                    "type": "onPartyAttendantSave",
                                    "title": "Save",
                                    "description": "User clicked Save",
                                    "value": "",
                                    "relation_key": "b07ba0b01b120aa3",
                                }
                            ],
                        }
                    },
                },
                {
                    "name": "PartyAllergy",
                    "key": "0536555a9fdc981d",
                    "state": "inactive",
                    "title": "Allergies",
                    "description": "",
                    "focus": "",
                    "icon": "https://dopniceu5am9m.cloudfront.net/static/planning/new_icon/notes_about.png",
                    "interaction_value": "{{party_allergy}}",
                    "interaction_template": "",
                    "loading": False,
                    "metadata": {
                        "onPartyAllergySave": {
                            "key": "01001",
                            "title": "Save",
                            "description": "",
                            "interactions": [
                                {
                                    "type": "onPartyAllergySave",
                                    "title": "Save",
                                    "description": "User clicked Save",
                                    "value": "",
                                    "relation_key": "b07ba0b01b120aa4",
                                }
                            ],
                        }
                    },
                },
                {
                    "name": "PartyRestaurant",
                    "key": "1ad3ebb8a0fdb912",
                    "state": "active",
                    "title": "Party Restaurant",
                    "description": "Find the perfect restaurant for your party",
                    "focus": "Restaurant Booking",
                    "icon": "https://dopniceu5am9m.cloudfront.net/static/planning/new_icon/notes_about.png",
                    "interaction_value": "",
                    "interaction_template": "",
                    "loading": False,
                    "metadata": {
                        "params": {"keyword": "Pizza", "location": "San Francisco"},
                        "find_restaurants": "https://plan-dev.api.brain.ai/v1.0/invoke/composite-api/method/restaurant/find-restaurants?location={LOCATION}&keyword={KEYWORD}",
                        "get_restaurant_detail": "https://plan-dev.api.brain.ai/v1.0/invoke/composite-api/method/restaurant/get-restaurant-detail?restaurant_id={RESTAURANT_ID}",
                    },
                },
            ],
        }
    ],
}
