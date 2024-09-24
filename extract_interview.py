from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json


uri = "mongodb+srv://personas:Iloveourcatsverymuch1975@persona-creator.7zs64.mongodb.net/?retryWrites=true&w=majority&appName=personcreator"


def load_interviews_from_mongo(uri):
    """
    Connects to MongoDB, fetches interviews along with associated persona data, and returns them.

    Args:
        uri (str): MongoDB connection URI.

    Returns:
        List[dict]: A list of dictionaries where each dictionary contains persona and their associated interviews.
    """
    try:
        # Connect to MongoDB
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client["personas_project"]

        # Fetch interviews and associated persona data
        interviews_collection = db["interviews"]
        personas_collection = db["personas"]

        # Fetch all interviews
        interviews_cursor = interviews_collection.find()

        interviews_data = []

        for interview in interviews_cursor:
            # Fetch the associated persona
            persona_id = interview.get('persona_id')
            if not persona_id:
                continue  # Skip if persona_id is missing

            try:
                persona = personas_collection.find_one({"_id": persona_id})
            except Exception as e:
                print(f"Error fetching persona with ID {persona_id}: {e}")
                persona = None

            # Append interview and associated persona data
            interviews_data.append({
                'interview': interview,
                'persona': persona
            })

        return interviews_data

    except Exception as e:
        print(f"Error connecting to MongoDB or fetching data: {e}")
        return []


def process_interview(interview):

    interview_data = []

    try:
        questions = interview.split("---")

        for question in questions:
            question = question.strip()
            if not question:
                continue

            parts = question.split("[Student]:")
            if len(parts) != 2:
                print(f"Skipping malformed question:\n{question}\n")
                continue

            question_part = parts[0].strip()
            answer_part = parts[1].strip()

            if '[Interviewer]:' in question_part:
                question = question_part.split('[Interviewer]:', 1)[1].strip()
            else:
                print(f"Skipping malformed question:\n{question_part}")
                continue

            interview_data.append(
                {"question": question, "answer": answer_part}
            )

    except Exception as e:
        print(f"Error: {e}")

    return interview_data


def format_persona(persona):
    """
    Formats persona details into a readable string format.

    Args:
        persona (dict): Dictionary containing persona details.

    Returns:
        str: Formatted string with persona details.
    """
    details = []
    details.append(f"Name: {persona.get('first_name', '')} {persona.get('last_name', '')}")
    details.append(f"Nationality: {persona.get('nationality', '')}")
    details.append(f"Gender: {persona.get('gender', '')}")
    details.append(f"Sexual Orientation: {persona.get('sexual_orientation', '')}")
    details.append(f"Age: {persona.get('age', '')}")
    details.append(f"Degree: {persona.get('degree', '')}")
    details.append(f"Speaks Dutch: {'Yes' if persona.get('speaks_dutch') else 'No'}")
    details.append(f"First Generation Student: {'Yes' if persona.get('is_first_gen') else 'No'}")
    details.append(f"Number of Siblings: {persona.get('number_siblings', '')}")
    details.append(f"Birth Order: {persona.get('birth_order', '')}")
    details.append(f"Driver's License: {'Yes' if persona.get('has_drivers_license') else 'No'}")
    details.append(f"Has Car: {'Yes' if persona.get('has_car') else 'No'}")
    details.append(f"Political Views: {persona.get('political_views', '')}")
    details.append(f"Student Association: {persona.get('student_association', '')}")
    details.append(f"Religious Background: {persona.get('religious_background', '')}")
    details.append(f"Number of Languages: {persona.get('number_of_languages', '')}")
    details.append(f"Level of English: {persona.get('level_of_english', '')}")
    details.append(f"Reason for going to University: {persona.get('reason_for_uni', '')}")
    details.append(f"Housing: {persona.get('housing', '')}")
    details.append(f"Has job: {'Yes' if persona.get('is_working') else 'No'}")
    details.append(f"Working hours: {persona.get('work_hours', '') if persona.get('is_working') else 'None'}")
    details.append(f"Student job: {persona.get('student_job', '') if persona.get('is_working') else "None"}")
    details.append(f"Hobbies: {'// '.join(persona.get('hobbies', []))}")
    details.append(f"Interesting Facts: {'// '.join(persona.get('interesting_facts', []))}")
    details.append(f"Memorable experiences: {'// '.join(persona.get('experiences', []))}")
    details.append(f"Father Alive: {'Yes' if persona.get('father_alive') else 'No'}")
    details.append(f"Father's Political Views: {persona.get('father_political', '') if persona.get('father_alive') else 'None'}")
    details.append(f"Father's Profession: {persona.get('father_profession', '') if persona.get('father_alive') else 'None'}")
    details.append(f"Father's Income: {persona.get('father_income', '')}")
    details.append(f"Mother Alive: {'Yes' if persona.get('mother_alive') else 'No'}")
    details.append(f"Mother's Political Views: {persona.get('mother_political', '') if persona.get('mother_alive') else 'None'}")
    details.append(f"Mother's Profession: {persona.get('mother_profession', '') if persona.get('mother_alive') else 'None'}")
    details.append(f"Mother's Income: {persona.get('mother_income', '') if persona.get('mother_alive') else 'None'}")

    details.append(f"\nPersonality Characteristics:")
    for key, value in persona.get('personality','').items():
        details.append(f"{key}: {value}")

    return "\n".join(details)


def format_interview(interview):
    """
    Formats the interview details into a readable string format.

    Args:
        interview (list): List of interview questions and answers.

    Returns:
        str: Formatted string with interview Q&A.
    """
    q_and_a = []
    for entry in interview:
        question = entry.get('question', '')
        answer = entry.get('answer', '')
        q_and_a.append(f"Interviewer:\n{question}\n\nStudents:\n{answer}\n\n")
    return "\n".join(q_and_a)


def format_json_to_text(json_data):
    """
    Formats the entire JSON data into a human-readable text format.

    Args:
        json_data (dict): The JSON data containing persona and interview.

    Returns:
        str: Formatted string with persona details and interview Q&A.
    """
    persona = json_data.get('persona', {})
    interview = json_data.get('interview', [])

    formatted_persona = format_persona(persona)
    formatted_interview = format_interview(interview)

    return f"=== Persona Details ===\n{formatted_persona}\n\n=== Interview ===\n{formatted_interview}"


def save_to_text_file(output_path, content):
    """
    Saves formatted content to a text file.

    Args:
        output_path (str): The file path where the formatted content should be saved.
        content (str): The formatted content to save.
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)


def save_interviews_to_files():
    interviews_data = load_interviews_from_mongo(uri)

    for interview in interviews_data:
        output_file = (f"{interview['persona']['first_name']}_{interview['persona']['last_name']}_interview.txt")

        processed_interview = process_interview(interview['interview']['interview'])
        formatted_content = format_json_to_text({
            "persona": interview['persona'],
            "interview": processed_interview,
        })

        # Save the formatted content to a text file
        save_to_text_file(f"output/{output_file}", formatted_content)

        print(f"Formatted content has been saved to {output_file}")


if __name__ == "__main__":
    save_interviews_to_files()