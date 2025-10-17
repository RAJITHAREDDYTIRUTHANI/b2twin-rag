import json
from simple_interface import ask_question, create_comprehensive_context, load_all_sensor_data

# Load the data
print("Loading sensor data...")
all_data = load_all_sensor_data()
context_summary = create_comprehensive_context(all_data)

# Test with crisp questions
crisp_questions = [
    "What's the temperature range?",
    "How many readings were recorded?",
    "What's the fan status?",
    "Was there super heat?",
    "What's the monitoring period?",
    "Are there any errors?",
    "What's the highest temperature?",
    "How many sensors are working?"
]

print("\n=== ULTRA-CRISP RESPONSES ===\n")

for i, question in enumerate(crisp_questions, 1):
    print(f"Q{i}: {question}")
    answer = ask_question(question, context_summary)
    print(f"A{i}: {answer}")
    print()
