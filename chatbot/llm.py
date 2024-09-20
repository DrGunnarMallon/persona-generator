from model.persona import Persona
import ollama

responses = []

def is_follow_up_contained(answer, question, follow_up):
    prompt = f"""In one word, either "yes" or "no" answer if the answer to the question '{follow_up}' is contained  in the answer below to the question '{question}'? Do not use more than one word to answer.

Answer: 
{answer}"""

    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])

    return response['message']['content'].lower() == 'yes'


def response_to_answer(answer, question):
    prompt = f"""The answer below was given to the question below in an interview between two university students. 
    Before moving onto the next question the person who asked the question should acknowledge the answer in a very 
    short response. Please provide a very short response that the interviewer should give to the interviewee's 
    answer. Answer with the interviewers response only.
    
    Question:
    {question}
    
    Answer:
    {answer}
    
    Instruction:
    
    Make sure that the answer has not been given before. Here is a list of previous responses:
    {"\n".join(responses)}"""

    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])

    return response['message']['content'].lower()



def get_llm_response(question, conversation_history):
    prompt = question['question']

    if 'info' in question:
        prompt += '\n\nEXTRA INFORMATION:\n' + question['info']
    if 'instruction' in question:
        prompt += '\n\nINSTRUCTION:\n' + question['instruction']

    if len(responses) > 0:
        prompt = responses[-1].title() + prompt

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

    responses.append(response_to_answer(answer, prompt))

    return answer, responses[-1]


def create_interview_data(persona, interview_guide):
    interview = []

    system_prompt = Persona.to_system_prompt(persona)
    conversation_history = [{'role': 'system', 'content': system_prompt}]

    for key, value in interview_guide.items():
        for question in value:
            answer, response = get_llm_response(question, conversation_history)
            interview.append({'question': f"{response}. {question['question']}", 'answer': answer})

            if 'follow-up' in question:
                for follow_up in question['follow-up']:
                    contained = is_follow_up_contained(answer=answer, question=question['question'],
                                                       follow_up=follow_up['question'])

                    if not contained:
                        follow_up_answer, follow_up_response = get_llm_response(follow_up, conversation_history)
                        interview.append({'question': f"{follow_up_response}. {follow_up['question']}", 'answer': follow_up_answer})

    return interview
