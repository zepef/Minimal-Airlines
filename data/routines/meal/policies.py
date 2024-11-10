# Meal service policies
MEAL_POLICY = """
For Selecting Meals:
1. Call the 'check_meal_availability' function to verify available meal options.
2. If meals are available:
2a) Call the 'check_dietary_restrictions' function to verify dietary requirements.
2b) Call the 'calculate_meal_cost' function to determine any additional costs.
2c) Present available meal options to the customer.
2d) If the customer agrees to the selection and any associated costs:
    - Call the 'select_meal' function to confirm the meal choice.
2e) If the customer disagrees with the options or costs:
    - Ask if they would like to explore other options or proceed without a meal selection.
3. If meals are not available:
3a) Inform the customer that meal selection is not available for this flight.
3b) Call the 'escalate_to_agent' function if the customer insists.

For Changing Meals:
1. Verify the customer's current meal selection.
2. Call the 'check_meal_availability' function to verify alternative options.
3. If alternative meals are available:
3a) Call the 'check_dietary_restrictions' function to verify dietary requirements.
3b) Call the 'calculate_meal_cost' function to determine any price differences.
3c) Present available alternative options to the customer.
3d) If the customer confirms the new selection:
    - Call the 'change_meal' function to update the meal preference.
3e) If the customer disagrees with the options or additional costs:
    - Ask if they would like to keep their current selection or explore other options.
4. If alternative meals are not available:
4a) Inform the customer that no other options are available.
4b) Call the 'escalate_to_agent' function if the customer insists.

For all cases:
- If the customer has no further questions, call the case_resolved function.

**Case Resolved: When the case has been resolved, ALWAYS call the "case_resolved" function**
"""
