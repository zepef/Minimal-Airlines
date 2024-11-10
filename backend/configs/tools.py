from journal import journal

def log_action(func):
    """Decorator to log function calls to the transaction journal"""
    def wrapper(*args, **kwargs):
        # Extract user_id from context if available
        user_id = kwargs.get('context', {}).get('user_id', 'unknown')
        
        # Determine service type and action type from function name
        func_name = func.__name__
        service_type = next((s for s in ['flight', 'baggage', 'seat', 'meal'] if s in func_name), 'general')
        action_type = func_name
        
        try:
            result = func(*args, **kwargs)
            # Log the successful transaction
            journal.log_transaction(
                user_id=user_id,
                service_type=service_type,
                action_type=action_type,
                details=str(result),
                status="completed"
            )
            return result
        except Exception as e:
            # Log the failed transaction
            journal.log_transaction(
                user_id=user_id,
                service_type=service_type,
                action_type=action_type,
                details=str(e),
                status="failed"
            )
            raise
    return wrapper

@log_action
def escalate_to_agent(reason=None):
    return f"Escalating to agent: {reason}" if reason else "Escalating to agent"

@log_action
def check_flight_availability():
    return "Flight is available"

@log_action
def calculate_flight_cost():
    return "Flight cost has been calculated"

@log_action
def create_flight_booking():
    return "Flight has been booked"

@log_action
def calculate_change_fee():
    return "Change fee has been calculated"

@log_action
def calculate_cancellation_fee():
    return "Cancellation fee has been calculated"

@log_action
def valid_to_change_flight():
    return "Customer is eligible to change flight"

@log_action
def change_flight():
    return "Flight was successfully changed!"

@log_action
def initiate_refund():
    status = "Refund initiated"
    return status

@log_action
def initiate_flight_credits():
    status = "Successfully initiated flight credits"
    return status

@log_action
def case_resolved():
    return "Case resolved. No further questions."

@log_action
def initiate_baggage_search():
    return "Baggage was found!"

@log_action
def check_seat_availability():
    return "Seats are available"

@log_action
def attribute_seat():
    return "Seat has been attributed"

@log_action
def change_seat():
    return "Seat has been changed"

@log_action
def add_baggage():
    return "Baggage has been added to the booking"

@log_action
def check_baggage_allowance():
    return "Baggage allowance is available"

@log_action
def calculate_baggage_fee():
    return "Baggage fee has been calculated"

@log_action
def retreat_baggage():
    return "Baggage has been removed from the booking"

@log_action
def calculate_baggage_refund():
    return "Baggage refund has been calculated"

@log_action
def check_meal_availability():
    return "Meal options are available"

@log_action
def select_meal():
    return "Meal has been selected"

@log_action
def change_meal():
    return "Meal preference has been changed"

@log_action
def calculate_meal_cost():
    return "Meal cost has been calculated"

@log_action
def check_dietary_restrictions():
    return "Dietary restrictions have been verified"
