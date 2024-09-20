from model.persona import Persona
from chatbot.llm import create_interview_data
from Interviews.formatter import format_interview
import json


interview_guide = ""
with open('./prompts/interview_guide.json', 'r', encoding='utf-8') as file:
    interview_guide = json.load(file)

# Create persona
for _ in range(1):
    persona = Persona()

    interview = create_interview_data(persona.to_json(), interview_guide)
    formatted_interview = format_interview(persona.to_json(), interview)

    with open(f'./{persona.first_name}_{persona.last_name}', 'w', encoding='utf-8') as file:
        file.write(formatted_interview)

    # Write to database
    # mongo.write_interview_to_mongo(persona.to_json(), formatted_interview)
