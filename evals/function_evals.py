import json

from configs.agents import *
from evals.eval_utils import run_function_evals

# Test case file paths
triage_test_cases = "eval_cases/triage_cases.json"
flight_modification_cases = "eval_cases/flight_modification_cases.json"
baggage_service_cases = "eval_cases/baggage_service_cases.json"
meal_service_cases = "eval_cases/meal_service_cases.json"
seat_service_cases = "eval_cases/seat_service_cases.json"

# Number of iterations for each test
n = 5

if __name__ == "__main__":
    # Run triage_agent evals
    print("\nRunning Triage Agent Evaluations...")
    with open(triage_test_cases, "r") as file:
        triage_test_cases = json.load(file)
    run_function_evals(
        triage_agent,
        triage_test_cases,
        n,
        eval_path="eval_results/triage_evals.json",
    )

    # Run flight modification evals
    print("\nRunning Flight Modification Evaluations...")
    with open(flight_modification_cases, "r") as file:
        flight_modification_cases = json.load(file)
    run_function_evals(
        flight_modification,
        flight_modification_cases,
        n,
        eval_path="eval_results/flight_modification_evals.json",
    )

    # Run baggage service evals
    print("\nRunning Baggage Service Evaluations...")
    with open(baggage_service_cases, "r") as file:
        baggage_service_cases = json.load(file)
    run_function_evals(
        baggage_service,
        baggage_service_cases,
        n,
        eval_path="eval_results/baggage_service_evals.json",
    )

    # Run meal service evals
    print("\nRunning Meal Service Evaluations...")
    with open(meal_service_cases, "r") as file:
        meal_service_cases = json.load(file)
    run_function_evals(
        meal_service,
        meal_service_cases,
        n,
        eval_path="eval_results/meal_service_evals.json",
    )

    # Run seat service evals
    print("\nRunning Seat Service Evaluations...")
    with open(seat_service_cases, "r") as file:
        seat_service_cases = json.load(file)
    run_function_evals(
        seat_service,
        seat_service_cases,
        n,
        eval_path="eval_results/seat_service_evals.json",
    )
