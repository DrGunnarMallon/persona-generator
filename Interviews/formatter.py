def format_interview(persona, interview):
    output = ""

    for item in interview:
        output += f"[Interviewer]: {item['question']}\n"
        output += f"[Student]: \n{item['answer']}\n"
        output += f"---\n"

    return output
