from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

from agents.user_management import user_management_agent
from agents.booking_management import booking_management_agent
from agents.onboarding_agent import onboarding_agent
from configs.agents import (
    triage_agent,
    flight_service,
    baggage_service,
    seat_service,
    meal_service
)
from journal import journal

app = FastAPI(title="Airline Service API")

# Pydantic models for request/response validation
class UserCreate(BaseModel):
    username: str
    email: str
    role: str = "customer"

class UserOnboard(BaseModel):
    username: str
    email: str
    name: str
    phone: str

class BookingCreate(BaseModel):
    customer_id: str
    flight_number: str
    from_airport: str
    to_airport: str
    departure_date: str

class ServiceRequest(BaseModel):
    user_id: str
    message: str
    context: Optional[Dict[str, Any]] = None

# User Management Endpoints
@app.post("/users/")
async def create_user(user: UserCreate):
    user_id = user_management_agent.create_user(user.username, user.email, user.role)
    if user_id is None:
        raise HTTPException(status_code=400, detail="Failed to create user")
    return {"user_id": user_id}

@app.post("/users/onboard/")
async def onboard_user(user: UserOnboard):
    result = onboarding_agent.onboard_new_user(
        username=user.username,
        email=user.email,
        name=user.name,
        phone=user.phone
    )
    if result is None:
        raise HTTPException(status_code=400, detail="Failed to onboard user")
    return result

@app.get("/users/{username}")
async def get_user(username: str):
    user = user_management_agent.read_user(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user[0],
        "username": user[1],
        "email": user[2],
        "role": user[3]
    }

# Booking Management Endpoints
@app.post("/bookings/")
async def create_booking(booking: BookingCreate):
    booking_id = booking_management_agent.create_booking(
        booking.customer_id,
        booking.flight_number,
        booking.from_airport,
        booking.to_airport,
        booking.departure_date
    )
    if booking_id is None:
        raise HTTPException(status_code=400, detail="Failed to create booking")
    return {"booking_id": booking_id}

@app.get("/bookings/{booking_id}")
async def get_booking(booking_id: int):
    booking = booking_management_agent.read_booking(booking_id)
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {
        "id": booking[0],
        "customer_id": booking[1],
        "flight_number": booking[2],
        "from_airport": booking[3],
        "to_airport": booking[4],
        "departure_date": booking[5],
        "booking_date": booking[6],
        "status": booking[7]
    }

# Service Agent Endpoints
@app.post("/services/triage/")
async def triage_service(request: ServiceRequest):
    try:
        response = triage_agent.process_message(request.message, request.context)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/services/flight/")
async def flight_service_endpoint(request: ServiceRequest):
    try:
        response = flight_service.process_message(request.message, request.context)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/services/baggage/")
async def baggage_service_endpoint(request: ServiceRequest):
    try:
        response = baggage_service.process_message(request.message, request.context)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/services/seat/")
async def seat_service_endpoint(request: ServiceRequest):
    try:
        response = seat_service.process_message(request.message, request.context)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/services/meal/")
async def meal_service_endpoint(request: ServiceRequest):
    try:
        response = meal_service.process_message(request.message, request.context)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Journal Endpoints
@app.get("/journal/user/{user_id}")
async def get_user_transactions(user_id: str):
    transactions = journal.get_user_transactions(user_id)
    return {"transactions": transactions}

@app.get("/journal/service/{service_type}")
async def get_service_transactions(service_type: str):
    transactions = journal.get_service_transactions(service_type)
    return {"transactions": transactions}

@app.get("/journal/recent/")
async def get_recent_transactions(limit: int = 50):
    transactions = journal.get_recent_transactions(limit)
    return {"transactions": transactions}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
