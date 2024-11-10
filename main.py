import sys
import os
from configs.agents import *
from swarm.repl import run_demo_loop
from agents.user_management import UserManagementAgent
from agents.booking_management import BookingManagementAgent
from agents.onboarding_agent import OnboardingAgent

# ANSI escape codes for colors
GREY = "\033[90m"
RESET = "\033[0m"

# Set the correct working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Note: The airline_bookings.db file is located in the 'instances' directory

try:
    user_management_agent = UserManagementAgent()
    booking_management_agent = BookingManagementAgent()
    onboarding_agent = OnboardingAgent(user_management_agent)
    triage_agent = None  # This should be properly initialized from configs.agents
except Exception as e:
    print(f"Error initializing agents: {e}")
    sys.exit(1)

def get_flight_info():
    print("\nEnter flight information:")
    from_airport = input("Departure Airport: ")
    to_airport = input("Arrival Airport: ")
    flight_number = input("Flight Number: ")
    departure_time = input("Departure Time: ")
    departure_date = input("Departure Date: ")
    
    return {
        "from_airport": from_airport,
        "to_airport": to_airport,
        "flight_number": flight_number,
        "departure_time": departure_time,
        "departure_date": departure_date
    }

def create_booking(user_info, context_variables):
    if not user_info:
        print("Sorry, only registered users can make bookings.")
        return
    
    customer_id = user_info[0]  # Assuming the ID is the first element in the user tuple
    flight_info = get_flight_info()
    
    context_variables["customer_context"] = user_info
    context_variables["flight_context"] = flight_info
    
    print("\nBooking pending. The usable Swarm agents are:")
    print("1. Flight Modification Agent")
    print("2. Flight cancel traversal")
    print("3. Flight change traversal")
    print("4. Lost baggage traversal")
    print("5. Seat Management Agent")
    
    print("\nNow you can:")
    print("1. Add luggage")
    print("2. Request meal preferences")
    print("3. Choose seats")
    print("4. Purchase travel insurance")
    print("5. Arrange airport transfer")
    print("6. Finish booking")
    
    while True:
        choice = input(f"{GREY}User:{RESET} ")
        if choice.lower() == "finish booking" or choice == "6":
            try:
                # Use the Swarm CLI for booking process
                booking_response = run_demo_loop(booking_management_agent, context_variables=context_variables, debug=True)
                print(f"Agent: {booking_response}")
                print("Agent: Your booking is confirmed. Thank you for choosing our airline!")
            except Exception as e:
                print(f"Error creating booking: {e}")
            break
        else:
            try:
                response = run_demo_loop(triage_agent, context_variables={"user_input": choice, **context_variables}, debug=True)
                print(f"Agent: {response}")
            except Exception as e:
                print(f"Error in conversation: {e}")

def is_user_registered(username):
    print(f"Checking if user '{username}' is registered...")  # Debug print
    try:
        user = user_management_agent.read_user(username)
        print(f"User data: {user}")  # Debug print
        return user is not None
    except Exception as e:
        print(f"Error checking user registration: {e}")  # Debug print
        return False

def user_mode():
    print("\nEntering User Mode")
    print("The agent will now ask for your username.")
    
    context_variables = {}
    user_info = None
    initial_prompt = "Hello! Welcome to our airline customer service. Could you please provide your username?"
    
    while True:
        print(f"Agent: {initial_prompt}")
        username = input(f"{GREY}User:{RESET} ")
        if username.lower() == 'exit':
            print("Exiting the program...")
            return 'exit'
        
        if is_user_registered(username):
            context_variables["username"] = username
            user_info = user_management_agent.read_user(username)
            if user_info:
                print(f"Agent: Thank you, {username}. How can I assist you today?")
                break
            else:
                print("Agent: I'm sorry, but there was an error retrieving your information. Please try again.")
        else:
            print("Agent: I'm sorry, but I couldn't find your username in our system.")
            onboard = input("Would you like to register as a new user? (yes/no): ").lower()
            if onboard == 'yes':
                user_info = onboarding_agent.onboard_new_user()
                if user_info:
                    context_variables["username"] = user_info[1]  # Assuming username is the second element in the user tuple
                    print(f"Agent: Thank you for registering, {user_info[1]}. How can I assist you today?")
                    break
                else:
                    print("Agent: I'm sorry, but there was an error during the registration process. Please try again.")
            else:
                print("Agent: I understand. Let me know if you change your mind.")
                initial_prompt = "Please provide a username or type 'exit' to quit:"

    # Main conversation loop
    while True:
        user_input = input(f"{GREY}User:{RESET} ")
        if user_input.lower() == 'exit':
            print("Exiting the program...")
            return 'exit'
        
        context_variables["user_input"] = user_input
        
        if "book" in user_input.lower():
            create_booking(user_info, context_variables)
        else:
            # Run the conversation through the triage agent
            try:
                response = run_demo_loop(triage_agent, context_variables=context_variables, debug=True)
                print(f"Agent: {response}")
            except Exception as e:
                print(f"Error in conversation: {e}")

def choose_mode():
    while True:
        mode = input("Enter mode (admin/user/exit): ").lower()
        if mode in ['admin', 'user', 'exit']:
            return mode
        print("Invalid mode. Please enter 'admin', 'user', or 'exit'.")

if __name__ == "__main__":
    try:
        while True:
            mode = choose_mode()
            if mode == 'admin':
                print("\nEntering Admin Mode")
                print("Admin mode is not implemented yet.")
                # Implement admin_options() function if needed
            elif mode == 'user':
                result = user_mode()
                if result == 'exit':
                    print("Exiting the program. Goodbye!")
                    break
            else:  # mode == 'exit'
                print("Exiting the program. Goodbye!")
                break
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
