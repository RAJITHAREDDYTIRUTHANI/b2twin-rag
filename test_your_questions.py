import json
from simple_interface import ask_question, create_comprehensive_context, load_all_sensor_data

# Load the data
print("Loading sensor data...")
all_data = load_all_sensor_data()
context_summary = create_comprehensive_context(all_data)

# Test with your specific questions
your_questions = [
    "Was there super heat on any particular day?",
    "On which day there was a sudden raise or increase and drop or decrease in the temperature and let me know if that affected the moisture level of the soil?"
]

print("\n=== TESTING WITH YOUR SPECIFIC QUESTIONS ===\n")

for i, question in enumerate(your_questions, 1):
    print(f"Question {i}: {question}")
    print("Answer:")
    answer = ask_question(question, context_summary)
    print(answer)
    print("\n" + "="*80 + "\n")
