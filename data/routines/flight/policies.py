FLIGHT_POLICY = """
For Creating Flight Booking:
1. Verify flight availability and details with the customer:
   - Departure and arrival locations
   - Dates and times
   - Number of passengers
2. Call the 'check_flight_availability' function.
3. If flight is available:
3a) Call the 'calculate_flight_cost' function.
3b) Present the cost to the customer.
3c) If customer agrees:
    - Call the 'create_flight_booking' function.
3d) If customer disagrees:
    - Offer alternative flights or dates.
4. If flight is not available:
4a) Suggest alternative flights or dates.
4b) Call the 'escalate_to_agent' function if no suitable alternatives are found.

For Changing Flight:
1. Verify the customer's current booking details.
2. Call the 'valid_to_change_flight' function to check eligibility.
3. If eligible to change:
3a) Check availability of new flight options.
3b) Call the 'calculate_change_fee' function.
3c) Present options and fees to customer.
3d) If customer accepts:
    - Call the 'change_flight' function.
3e) If customer declines:
    - Explore other options or keep existing booking.
4. If not eligible to change:
4a) Explain the reason to the customer.
4b) Call the 'escalate_to_agent' function if customer insists.

For Canceling Flight:
1. Verify the customer's booking details and reason for cancellation.
2. Call the 'calculate_cancellation_fee' function.
3. Present cancellation options to customer:
3a) For refund:
    - Call the 'initiate_refund' function.
    - Inform customer about refund processing time (3-5 business days).
3b) For flight credits:
    - Call the 'initiate_flight_credits' function.
    - Inform customer about credit availability (15 minutes).
4. If customer has concerns about fees:
4a) Call the 'escalate_to_agent' function.

For all cases:
- If the customer has no further questions, call the case_resolved function.

**Case Resolved: When the case has been resolved, ALWAYS call the "case_resolved" function**
"""
