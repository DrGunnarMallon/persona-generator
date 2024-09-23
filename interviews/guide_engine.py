import json


class InterviewGuideEngine:
    def __init__(self, guide_file):
        # Load the interview guide from a JSON file
        with open(guide_file, 'r', encoding='utf-8') as f:
            self.guide = json.load(f)

        # Initialize indices to keep track of the current position in the guide
        self.sections = list(self.guide.keys())
        self.current_section_index = 0
        self.current_question_index = 0
        self.current_followup_index = -1  # -1 indicates no follow-up is currently active

    def get_current_question(self):
        """
        Returns an object with the current question, info, instructions, and a flag indicating if it's a follow-up.
        """
        current_question_data = self._get_current_question_data()
        if current_question_data is None:
            return None  # No more questions

        # Extract the details
        question_text = current_question_data.get('question', '')
        instruction = current_question_data.get('instruction', '')
        info = current_question_data.get('info', '')
        is_follow_up = self.current_followup_index >= 0

        return {
            'question': question_text,
            'instruction': instruction,
            'info': info,
            'is_follow_up': is_follow_up
        }

    def get_next_question(self):
        """
        Advances to the next question and returns the next question's details.
        """
        # Advance to the next question or follow-up
        if not self._advance():
            return None  # No more questions

        # Return the details of the new current question
        return self.get_current_question()

    def has_follow_ups(self):
        """
        Returns True if the current question has follow-up questions, False otherwise.
        """
        current_question_data = self._get_base_question_data()
        if current_question_data is None:
            return False
        followups = current_question_data.get('follow-up', [])
        return len(followups) > 0

    def has_info(self):
        """
        Returns True if the current question contains an 'info' field, False otherwise.
        """
        current_question_data = self._get_current_question_data()
        return current_question_data is not None and 'info' in current_question_data

    def has_instructions(self):
        """
        Returns True if the current question contains an 'instruction' field, False otherwise.
        """
        current_question_data = self._get_current_question_data()
        return current_question_data is not None and 'instruction' in current_question_data

    # Helper methods
    def _get_current_question_data(self):
        """
        Retrieves the data for the current question or follow-up question.
        """
        if self.current_section_index >= len(self.sections):
            return None  # No more questions

        current_section = self.guide[self.sections[self.current_section_index]]
        if self.current_question_index >= len(current_section):
            return None  # No more questions in this section

        current_question_data = current_section[self.current_question_index]

        if self.current_followup_index >= 0:
            # Currently in a follow-up question
            followups = current_question_data.get('follow-up', [])
            if self.current_followup_index < len(followups):
                return followups[self.current_followup_index]
            else:
                return None  # No more follow-ups
        else:
            # Main question
            return current_question_data

    def _get_base_question_data(self):
        """
        Retrieves the data for the base (main) question, regardless of follow-ups.
        """
        if self.current_section_index >= len(self.sections):
            return None

        current_section = self.guide[self.sections[self.current_section_index]]
        if self.current_question_index >= len(current_section):
            return None

        return current_section[self.current_question_index]

    def _advance(self):
        """
        Advances to the next question or follow-up question.
        Returns True if successfully advanced, False if there are no more questions.
        """
        current_question_data = self._get_base_question_data()
        if current_question_data is None:
            return False  # No more questions

        if self.current_followup_index >= 0:
            # Currently in follow-up questions
            followups = current_question_data.get('follow-up', [])
            if self.current_followup_index + 1 < len(followups):
                # Move to the next follow-up question
                self.current_followup_index += 1
            else:
                # No more follow-ups, move to the next main question
                self.current_followup_index = -1
                self.current_question_index += 1
        else:
            # Not currently in a follow-up
            if 'follow-up' in current_question_data and len(current_question_data['follow-up']) > 0:
                # Start the follow-up questions
                self.current_followup_index = 0
            else:
                # Move to the next main question
                self.current_question_index += 1

        # Check if we need to move to the next section
        current_section = self.guide[self.sections[self.current_section_index]]
        if self.current_question_index >= len(current_section):
            # Move to the next section
            self.current_question_index = 0
            self.current_section_index += 1
            self.current_followup_index = -1  # Reset follow-up index

            if self.current_section_index >= len(self.sections):
                return False  # No more sections/questions

        return True
