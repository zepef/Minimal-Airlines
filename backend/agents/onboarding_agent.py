from agents.user_management import user_management_agent

class OnboardingAgent:
    def __init__(self, user_management_agent):
        self.user_management_agent = user_management_agent

    def onboard_new_user(self):
        print("\nWelcome to the onboarding process!")
        username = input("Please choose a username: ")
        email = input("Please enter your email: ")
        name = input("Please enter your full name: ")
        phone = input("Please enter your phone number: ")
        
        # Create the new user
        user_id = self.user_management_agent.create_user(username, email, "customer")
        if user_id:
            print(f"User successfully created with ID: {user_id}")
            # Return a dictionary with user information
            return {
                "user_id": user_id,
                "username": username,
                "email": email,
                "name": name,
                "phone": phone,
                "role": "customer"
            }
        else:
            print("Failed to create user. Please try again later.")
            return None

onboarding_agent = OnboardingAgent(user_management_agent)
