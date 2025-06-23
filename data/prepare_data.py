import json
import random

# Load JSON data
with open('../backend/app/colleges.json', 'r') as f:
    colleges = json.load(f)

# Define question templates
question_templates = {
    'No of courses available in the college': [
        "What are the courses at {name}?",
        "Which courses are offered by {name}?",
        "List the courses available at {name}."
    ],
    'Annual Fee (Convener Quota)': [
        "What is the convener quota fee at {name}?",
        "How much is the annual fee for convener quota at {name}?",
        "Tell me the convener quota fees for {name}."
    ],
    'Annual Fee (Management Quota)': [
        "What is the management quota fee at {name}?",
        "How much is the management quota fee at {name}?",
        "Tell me the management quota fees for {name}."
    ],
    'Percentage of Placement': [
        "What is the placement percentage at {name}?",
        "How good are placements at {name}?",
        "Tell me about {name} placements."
    ],
    'Phone No. of Head of Instt.': [
        "What is the contact number for {name}?",
        "How can I contact {name}?",
        "Give me the phone number of {name}."
    ],
    'general': [
        "Tell me about {name}.",
        "What are the details of {name}?",
        "Give me information about {name}."
    ]
}

# Generate training data
training_data = []

for college in colleges:
    name = college['Name of the Institution']
    code = college['Institution_code']
    
    for field, templates in question_templates.items():
        for template in templates:
            question = template.format(name=name)
            if field == 'general':
                # General info response
                answer = (f"Details for {name}:\n"
                    f"Address: {college['Address1']}, {college['Address2']}, {college['District']}, {college['State']}, Pin: {college['Pin Code']}\n"
                    f"Courses: {', '.join(college['No of courses available in the college'])}\n"
                    f"Affiliated to: {college.get('Affiliated to', 'N/A')}\n"
                    f"Rating: {college['Rating']}")
            else:
                answer = f"{field} at {name}: {college[field] if field in college else 'Information not available.'}"
            training_data.append({'question': question, 'answer': answer})
            
            # Add code-based variation
            code_question = template.format(name=code)
            training_data.append({'question': code_question, 'answer': answer})
    
    # Add variations with synonyms
    for field, templates in question_templates.items():
        for template in templates:
            if 'courses' in template.lower():
                question = template.replace('courses', 'programs').format(name=name)
                answer = f"No of courses available in the college at {name}: {', '.join(college['No of courses available in the college'])}"
                training_data.append({'question': question, 'answer': answer})

# Save training data
with open('training_data.json', 'w') as f:
    json.dump(training_data, f, indent=2)

print(f"Generated {len(training_data)} question-answer pairs.")