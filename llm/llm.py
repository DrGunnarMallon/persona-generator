import ollama
from prompts.prompts import prompt_follow_up_contained, prompt_persona_system_prompt, prompt_formulate_question

model = "llama3.1"


def is_follow_up_contained(answer, question, follow_up):
    response = ollama.chat(model=model, messages=[{'role': 'user', 'content': prompt_follow_up_contained(answer, question, follow_up)}])
    return response['message']['content'].lower() == 'yes'


def get_llm_response(prompt, conversation_history):
    conversation_history.append({
        'role': 'user',
        'content': prompt
    })

    response = ollama.chat(model=model, messages=conversation_history)
    answer = response['message']['content']

    conversation_history.append({
        'role': 'assistant',
        'content': answer
    })

    return answer


def formulate_next_question(previous_question, answer, current_question):
    user_prompt = [
        {
            'role': 'user',
            'content': prompt_formulate_question(previous_question['question'], current_question['question'], answer)
        }
    ]

    current_prompt = ollama.chat(model=model, messages=user_prompt)['message']['content']
    question_only = current_prompt

    if current_question['instruction'] != '':
        current_prompt += f"\n{current_question['instruction']}"
    if current_question['info'] != '':
        current_prompt += f"\n{current_question['info']}"

    return current_prompt.replace("\n", " ").strip("\"").replace("\"", " - "), question_only.replace("\n", " ").replace("\"", "")


def create_interview_data(persona, interview_engine):
    interview = []
    previous_question = None
    answer = ''

    system_prompt = prompt_persona_system_prompt(persona)
    conversation_history = [{'role': 'system', 'content': system_prompt}]

    current_question = interview_engine.get_current_question()
    if current_question:
        prompt = current_question['question']

        if interview_engine.has_instructions():
            prompt += f"\n{current_question['instruction']}"
        if interview_engine.has_info():
            prompt += f"\n{current_question['info']}"

        answer = get_llm_response(prompt, conversation_history)
        previous_question = current_question
        interview.append({'question': f"{current_question['question']}", 'answer': answer})
    else:
        print("No more questions")

    while current_question:
        current_question = interview_engine.get_next_question()
        if not current_question:
            break

        if current_question['is_follow_up']:
            if is_follow_up_contained(answer, previous_question['question'], current_question['question']):
                continue

        next_question, question_only = formulate_next_question(previous_question, answer, current_question)

        answer = get_llm_response(next_question, conversation_history)
        previous_question = current_question
        interview.append({'question': f"{question_only}", 'answer': answer})

    return interview
