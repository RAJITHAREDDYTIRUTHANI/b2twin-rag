import json
from simple_interface import ask_question, create_comprehensive_context, load_all_sensor_data

# Load the data
print("Loading sensor data...")
all_data = load_all_sensor_data()
context_summary = create_comprehensive_context(all_data)

# Test with sample questions
sample_questions = [
    "What was the temperature trend over the monitoring period?",
    "How many temperature readings were recorded?",
    "What is the temperature range in the Biosphere 2 rainforest area?"
]

print("\n=== TESTING WITH SAMPLE QUESTIONS ===\n")

for i, question in enumerate(sample_questions, 1):
    print(f"Question {i}: {question}")
    print("Answer:")
    answer = ask_question(question, context_summary)
    print(answer)
    print("\n" + "="*80 + "\n")
