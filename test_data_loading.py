import json
from simple_interface import ask_question, create_comprehensive_context, load_all_sensor_data

# Test the data loading and context creation
print("Testing data loading...")
all_data = load_all_sensor_data()
print(f"Loaded {len(all_data)} sensor types")

# Test context creation
print("Creating context...")
context_summary = create_comprehensive_context(all_data)
print(f"Context length: {len(context_summary)} characters")

# Test a question
print("\nTesting question...")
question = "What is the temperature range?"
answer = ask_question(question, context_summary)
print(f"Q: {question}")
print(f"A: {answer}")

print("\nData loading test completed successfully!")