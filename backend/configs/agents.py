from configs.tools import *
from data.routines.baggage.policies import *
from data.routines.flight.policies import *
from data.routines.meal.policies import *
from data.routines.prompts import STARTER_PROMPT

from swarm import Agent


def transfer_to_flight():
    return flight_service


def transfer_to_baggage():
    return baggage_service


def transfer_to_seat():
    return seat_service


def transfer_to_meal():
    return meal_service


def transfer_to_triage():
    """Call this function when a user needs to be transferred to a different agent and a different policy.
    For instance, if a user is asking about a topic that is not handled by the current agent, call this function.
    """
    return triage_agent


def triage_instructions(context_variables):
    customer_context = context_variables.get("customer_context", None)
    flight_context = context_variables.get("flight_context", None)
    return f"""You are to triage a users request, and call a tool to transfer to the right intent.
    Once you are ready to transfer to the right intent, call the tool to transfer to the right intent.
    You dont need to know specifics, just the topic of the request.
    When you need more information to triage the request to an agent, ask a direct question without explaining why you're asking it.
    Do not share your thought process with the user! Do not make unreasonable assumptions on behalf of user.
    The customer context is here: {customer_context}, and flight context is here: {flight_context}"""


triage_agent = Agent(
    name="Triage Agent",
    instructions=triage_instructions,
    functions=[transfer_to_flight, transfer_to_baggage, transfer_to_seat, transfer_to_meal],
)

flight_service = Agent(
    name="Flight Service Agent",
    instructions=STARTER_PROMPT + FLIGHT_POLICY,
    functions=[
        escalate_to_agent,
        check_flight_availability,
        calculate_flight_cost,
        create_flight_booking,
        calculate_change_fee,
        calculate_cancellation_fee,
        valid_to_change_flight,
        change_flight,
        initiate_refund,
        initiate_flight_credits,
        transfer_to_triage,
        case_resolved,
    ],
)

baggage_service = Agent(
    name="Baggage Service Agent",
    instructions=STARTER_PROMPT + BAGGAGE_POLICY,
    functions=[
        escalate_to_agent,
        initiate_baggage_search,
        check_baggage_allowance,
        calculate_baggage_fee,
        add_baggage,
        calculate_baggage_refund,
        retreat_baggage,
        transfer_to_triage,
        case_resolved,
    ],
)

seat_service = Agent(
    name="Seat Service Agent",
    instructions=STARTER_PROMPT + SEAT_MANAGEMENT_POLICY,
    functions=[
        escalate_to_agent,
        check_seat_availability,
        attribute_seat,
        change_seat,
        transfer_to_triage,
        case_resolved,
    ],
)

meal_service = Agent(
    name="Meal Service Agent",
    instructions=STARTER_PROMPT + MEAL_POLICY,
    functions=[
        escalate_to_agent,
        check_meal_availability,
        check_dietary_restrictions,
        calculate_meal_cost,
        select_meal,
        change_meal,
        transfer_to_triage,
        case_resolved,
    ],
)
