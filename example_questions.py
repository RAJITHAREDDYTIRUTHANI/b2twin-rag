import json
from simple_interface import ask_question, create_comprehensive_context, load_all_sensor_data

# Load the data
print("Loading sensor data...")
all_data = load_all_sensor_data()
context_summary = create_comprehensive_context(all_data)

# Great example questions that work well with your data
example_questions = [
    "What was the average temperature during the monitoring period?",
    "How many temperature readings were recorded and over what time period?",
    "What's the temperature range in the Biosphere 2 rainforest area?",
    "What's the status of the fan control systems?",
    "How many readings does each sensor type have?",
    "What was the temperature pattern on the first day of monitoring?",
    "Are there any correlations between fan operations and temperature?",
    "What's the overall health of the environmental control system?"
]

print("\n=== EXAMPLE QUESTIONS THAT WORK WELL ===\n")

for i, question in enumerate(example_questions, 1):
    print(f"Question {i}: {question}")
    print("Answer:")
    answer = ask_question(question, context_summary)
    print(answer)
    print("\n" + "="*80 + "\n")
