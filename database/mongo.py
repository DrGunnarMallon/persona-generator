from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

uri = "mongodb+srv://personas:Iloveourcatsverymuch1975@persona-creator.7zs64.mongodb.net/?retryWrites=true&w=majority&appName=persona-creator"

def write_interview_to_mongo(persona, interview):
    client = MongoClient(uri, server_api=ServerApi('1'))

    interview_data = {
        "interview": interview
    }

    def print_with_time(message):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] {message}")

    try:
        mydb = client['personas_project']
        mycol = mydb['personas']

        print_with_time("Inserting self into 'personas' collection")
        result = mycol.insert_one(persona)
        interview_data["persona_id"] = result.inserted_id
    except Exception as e:
        print(f"Error inserting self: {e}")
        return None

    try:
        mycol = mydb['interviews']
        print_with_time("Inserting interview into 'interviews' collection")
        return mycol.insert_one(interview_data)
    except Exception as e:
        print(f"Error inserting interview: {e}")
        return None
