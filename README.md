# Airline Customer Service API

A FastAPI-based backend service for airline customer service operations.

## Project Structure

```
backend/
├── agents/              # Service agents implementation
│   ├── booking_management.py
│   ├── onboarding_agent.py
│   └── user_management.py
├── configs/            # Configuration files and tools
├── data/              # Data files and routines
│   └── routines/      # Service routines and policies
├── evals/             # Evaluation test cases and utilities
│   ├── eval_cases/    # Test cases for each service
│   └── eval_results/  # Evaluation results
├── instances/         # Database files
├── main.py           # FastAPI application
└── requirements.txt   # Project dependencies
```

## Features

- User Management & Onboarding
- Booking Management
- Service Agents:
  - Triage Agent (request routing)
  - Flight Service (booking, changes, cancellations)
  - Baggage Service (lost baggage, add/remove baggage)
  - Seat Service (selection and changes)
  - Meal Service (selection and dietary requirements)
- Transaction Journal
- Evaluation System

## API Endpoints

### User Management & Onboarding
- POST `/users/` - Create new user
- POST `/users/onboard/` - Onboard new user with additional details
- GET `/users/{username}` - Get user details

### Booking Management
- POST `/bookings/` - Create new booking
- GET `/bookings/{booking_id}` - Get booking details

### Service Endpoints
- POST `/services/triage/` - Triage service requests
- POST `/services/flight/` - Flight service operations
- POST `/services/baggage/` - Baggage service operations
- POST `/services/seat/` - Seat service operations
- POST `/services/meal/` - Meal service operations

### Journal
- GET `/journal/user/{user_id}` - Get user transactions
- GET `/journal/service/{service_type}` - Get service transactions
- GET `/journal/recent/` - Get recent transactions

## Setup

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Start the server:
```bash
uvicorn main:app --reload
```

3. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Structure

All databases are stored in the `backend/instances` directory:
- `airline_users.db` - User management database
- `airline_bookings.db` - Booking management database
- `airline_journal.db` - Transaction journal database

## Testing

The evaluation system includes test cases for all services:
- Triage service tests
- Flight service tests
- Baggage service tests
- Meal service tests
- Seat service tests

To run evaluations:
```bash
cd backend
python -m evals.function_evals
```

## Request Examples

### Onboard New User
```json
POST /users/onboard/
{
    "username": "john_doe",
    "email": "john@example.com",
    "name": "John Doe",
    "phone": "+1234567890"
}
```

### Create Booking
```json
POST /bookings/
{
    "customer_id": "123",
    "flight_number": "FL123",
    "from_airport": "LAX",
    "to_airport": "JFK",
    "departure_date": "2024-01-01"
}
```

### Service Request
```json
POST /services/{service_type}/
{
    "user_id": "123",
    "message": "I need to change my seat",
    "context": {
        "booking_id": "456",
        "flight_number": "FL123"
    }
}
