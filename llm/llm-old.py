from model.persona import Persona
import ollama
from prompts.prompts import prompt_follow_up_contained, prompt_response_to_answer, prompt_persona_system_prompt


def is_follow_up_contained(answer, question, follow_up):
    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt_follow_up_contained(answer, question, follow_up)}])
    return response['message']['content'].lower() == 'yes'


def response_to_answer(answer, question, previous_responses=None):
    try:
        response = ollama.chat(model='llama3', messages=prompt_response_to_answer(answer, question, previous_responses))
        return response['message']['content'].strip("\"")
    except Exception as e:
        print(f"Error calling Ollama API: {str(e)}")

    return None

def get_llm_response(question, conversation_history, responses):
    prompt = question['question']

    if 'info' in question:
        prompt += '\n\nEXTRA INFORMATION:\n' + question['info']
    if 'instruction' in question:
        prompt += '\n\nINSTRUCTION:\n' + question['instruction']


    conversation_history.append({
        'role': 'user',
        'content': prompt
    })

    response = ollama.chat(model='llama3', messages=conversation_history)
    answer = response['message']['content']

    conversation_history.append({
        'role': 'assistant',
        'content': answer
    })

    feedback = response_to_answer(answer, prompt, responses)

    return answer, feedback


def create_interview_data(persona, interview_engine):
    interview = []
    responses = []

    system_prompt = prompt_persona_system_prompt(persona)
    conversation_history = [{'role': 'system', 'content': system_prompt}]

    for key, value in interview_guide.items():
        for question in value:
            answer, response = get_llm_response(question, conversation_history, responses)
            if responses:
                interview.append({'question': f"{str(responses[-1]).capitalize()} {question['question']}", 'answer': answer})
            else:
                interview.append({'question': f"{question['question']}", 'answer': answer})
            responses.append(response)

            if 'follow-up' in question:
                for follow_up in question['follow-up']:
                    contained = is_follow_up_contained(answer=answer, question=question['question'], follow_up=follow_up['question'])

                    if not contained:
                        follow_up_answer, follow_up_response = get_llm_response(follow_up, conversation_history, responses)
                        if responses:
                            interview.append({'question': f"{str(responses[-1]).capitalize()} {follow_up['question']}", 'answer': follow_up_answer})
                        else:
                            interview.append({'question': f"{follow_up['question']}", 'answer': follow_up_answer})
                        responses.append(follow_up_response)

    return interview
