import os
import json
import re
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

uri = "mongodb+srv://personas:Iloveourcatsverymuch1975@persona-creator.7zs64.mongodb.net/?retryWrites=true&w=majority&appName=personcreator"


def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z_\-]', '_', name)


def convert_objectids(obj):
    if isinstance(obj, list):
        return [convert_objectids(item) for item in obj]
    elif isinstance(obj, dict):
        new_obj = {}
        for key, value in obj.items():
            if isinstance(value, ObjectId):
                new_obj[key] = str(value)
            elif isinstance(value, dict) or isinstance(value, list):
                new_obj[key] = convert_objectids(value)
            else:
                new_obj[key] = value
        return new_obj
    else:
        return obj


def load_interviews_from_mongo(uri):
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client["personas_project"]

        interviews_collection = db["interviews"]
        personas_collection = db["personas"]

        interviews_cursor = interviews_collection.find()

        interviews_data = []

        for interview in interviews_cursor:
            persona_id = interview.get('persona_id')
            if not persona_id:
                print("persona_id missing in interview. Skipping.")
                continue  # Skip if persona_id is missing

            try:
                persona = personas_collection.find_one({"_id": persona_id})
            except Exception as e:
                print(f"Error fetching persona with ID {persona_id}: {e}")
                persona = None

            # Convert ObjectIds to strings
            interview_converted = convert_objectids(interview)
            persona_converted = convert_objectids(persona) if persona else None

            interviews_data.append({
                'interview': interview_converted,
                'persona': persona_converted
            })

        return interviews_data

    except Exception as e:
        print(f"Error connecting to MongoDB or fetching data: {e}")
        return []


def save_interviews_to_json():
    if not uri:
        print("MongoDB URI not found in environment variables.")
        return

    interviews_data = load_interviews_from_mongo(uri)

    output_dir = os.path.join("..", "output")
    os.makedirs(output_dir, exist_ok=True)

    for interview in interviews_data:
        persona = interview.get('persona')
        if not persona:
            print("Persona data is missing. Skipping this interview.")
            continue

        first_name = sanitize_filename(persona.get('first_name', 'Unknown'))
        last_name = sanitize_filename(persona.get('last_name', 'Unknown'))

        output_file = os.path.join(output_dir, f"{first_name}_{last_name}_interview.json")

        try:
            with open(output_file, 'w') as file:
                json.dump(interview, file, indent=4)
            print(f"Successfully saved {output_file}")
        except IOError as e:
            print(f"Failed to write to {output_file}: {e}")


if __name__ == "__main__":
    save_interviews_to_json()