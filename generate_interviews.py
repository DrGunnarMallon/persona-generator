from interviews.guide_engine import InterviewGuideEngine
from interviews.formatter import format_interview
from model.persona import Persona
from llm.llm import create_interview_data
from database.mongo import write_interview_to_mongo


for _ in range(300):
    interview_engine = InterviewGuideEngine('prompts/interview_guide.json')
    persona = Persona()

    interview = create_interview_data(persona.to_json(), interview_engine)
    formatted_interview = format_interview(persona.to_json(), interview)

    with open(f'./output/{persona.first_name}_{persona.last_name}', 'w', encoding='utf-8') as file:
        file.write(formatted_interview)

    write_interview_to_mongo(persona.to_json(), formatted_interview)

