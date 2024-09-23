import random
from model.definitions import *
from model.personality import get_personality_string, get_personality


def get_nationality():
    nationality = random.choices(
        GENERAL["NATIONALITIES"], GENERAL["NATIONALITY_WEIGHTS"]
    )[0]
    return nationality == "Dutch", nationality


def get_degree():
    return random.choice(GENERAL["DEGREE"])


def get_hobbies():
    return random.choices(GENERAL["HOBBIES"], k=2)


def get_interesting_facts():
    return random.choices(GENERAL["FACTS"], k=2)


def get_reason_for_uni():
    return random.choice(GENERAL["REASON_FOR_UNI"])


def generate_personality():
    return get_personality()


class Persona:
    def __init__(
            self,
    ):
        self.is_dutch, self.nationality = get_nationality()
        self.gender = self._get_gender()
        self.sexual_orientation = self._get_sexual_orientation()
        self.age = self._get_age()
        self.degree = get_degree()
        self.speaks_dutch = self._get_speaks_dutch()
        self.first_name, self.last_name = self._get_name()
        self.is_first_gen = self._get_first_gen()
        self.number_siblings = self._get_number_siblings()
        self.birth_order = self._get_birth_order()
        self.father_alive, self.mother_alive = self._get_parents_alive()
        self.is_member, self.student_association = self._get_student_association()
        self.religious_background = self._get_religious_background()
        self.is_working, self.work_hours, self.student_job = self._get_work()
        self.number_of_languages, self.level_of_english = self._get_languages()
        self.housing = self._get_housing()
        self.experiences = self._get_experiences()
        self.reason_for_uni = get_reason_for_uni()
        self.hobbies = get_hobbies()
        self.interesting_facts = get_interesting_facts()
        self.father_profession, self.mother_profession = self._get_parents_professions()
        self.father_income, self.mother_income = self._get_incomes()
        self.personality = generate_personality()

    def _get_gender(self):
        return random.choices(
            GENERAL["GENDER"], INTL[self.nationality]["GENDER_WEIGHTS"]
        )[0]

    def _get_sexual_orientation(self):
        return random.choices(
            GENERAL["SEXUAL_ORIENTATION"],
            INTL[self.nationality]["SEXUAL_ORIENTATION_WEIGHTS"],
        )[0]

    def _get_age(self):
        return random.choices(GENERAL["AGE"], INTL[self.nationality]["AGE_WEIGHTS"])[0]

    def _get_speaks_dutch(self):
        if self.nationality == "Dutch":
            return True
        return random.random() < THRESHOLDS["DUTCH"]

    def _get_name(self):
        first_name, last_name = "", ""

        if self.gender.lower() == "male":
            first_name = random.choices(INTL[self.nationality]["MALE_FIRST_NAME"])[0]
        elif self.gender.lower() == "female":
            first_name = random.choices(INTL[self.nationality]["FEMALE_FIRST_NAME"])[0]
        else:
            first_name = random.choices(INTL[self.nationality]["NONGENDER_FIRST_NAME"])[
                0
            ]

        last_name = random.choices(INTL[self.nationality]["LAST_NAME"])[0]

        return first_name, last_name

    def _get_first_gen(self):
        return random.random() < INTL[self.nationality]["FIRST_GEN_STUDENT_THRESHOLD"]

    def _get_number_siblings(self):
        return random.choices(
            GENERAL["NUMBER_SIBLINGS"],
            INTL[self.nationality]["NUMBER_OF_SIBLINGS_WEIGHTS"],
        )[0]

    def _get_birth_order(self):
        if self.number_siblings == 0:
            return None
        if self.number_siblings == 1:
            return random.choice(["youngest", "oldest"])
        return random.choice(GENERAL["BIRTH_ORDER"])

    def _get_parents_alive(self):
        father_alive = (
                random.random() < INTL[self.nationality]["FATHER_ALIVE_THRESHOLD"]
        )
        mother_alive = (
                random.random() < INTL[self.nationality]["MOTHER_ALIVE_THRESHOLD"]
        )
        return father_alive, mother_alive

    def _get_student_association(self):
        is_member = False
        association = None
        if self.nationality == "Dutch":
            is_member = random.random() < THRESHOLDS["DUTCH_STUDENT_ASSOCIATION"]
        else:
            is_member = random.random() < THRESHOLDS["INTL_STUDENT_ASSOCIATION"]

        if is_member:
            association = random.choice(GENERAL["STUDENT_ASSOCIATIONS"])

        return is_member, association

    def _get_religious_background(self):
        return random.choices(
            INTL[self.nationality]["RELIGION"],
            INTL[self.nationality]["RELIGION_WEIGHTS"],
        )[0]

    def _get_work(self):
        # is working
        is_working = random.random() < INTL[self.nationality]["WORK_THRESHOLD"]

        # work hours
        working_hours = (
            None
            if not is_working
            else random.choices(
                GENERAL["WORK_HOURS"], INTL[self.nationality]["WORK_HOURS_WEIGHTS"]
            )[0]
        )

        # student job
        student_job = None if not is_working else random.choice(GENERAL["STUDENT_JOBS"])

        return is_working, working_hours, student_job

    def _get_languages(self):
        languages_spoken = int(random.random() * 3) + 2
        level_of_english = random.choices(
            GENERAL["ENGLISH_LEVEL"], INTL[self.nationality]["ENGLISH_LEVEL_WEIGHTS"]
        )[0]

        return languages_spoken, level_of_english

    def _get_housing(self):
        if self.nationality == "Dutch":
            return random.choice(DUTCH["HOUSING"])
        else:
            return random.choice(NONDUTCH["HOUSING"])

    def _get_experiences(self):
        if self.nationality == "Dutch":
            return list(random.choices(DUTCH["EXPERIENCE"], k=2))
        else:
            return list(random.choices(NONDUTCH["EXPERIENCE"], k=2))

    def _get_parents_professions(self):
        father_profession = ""
        if self.father_alive:
            father_profession = random.choice(GENERAL["PROFESSIONS"])
        else:
            None

        mother_profession = ""
        if self.mother_alive:
            mother_profession = random.choice(GENERAL["PROFESSIONS"])
        else:
            None

        return father_profession, mother_profession

    def _get_incomes(self):
        # father_income = 0
        # mother_income = 0

        if self.father_alive and self.father_profession != "":
            father_income = GENERAL["INCOME"][
                GENERAL["PROFESSIONS"].index(self.father_profession)
            ]
        else:
            father_income = None

        if self.mother_alive and self.mother_profession != "":
            mother_income = GENERAL["INCOME"][
                GENERAL["PROFESSIONS"].index(self.mother_profession)
            ]
        else:
            mother_income = None

        return father_income, mother_income

    def to_json(self):
        return {
            'is_dutch': self.is_dutch,
            'nationality': self.nationality,
            'gender': self.gender,
            'sexual_orientation': self.sexual_orientation,
            'age': self.age,
            'degree': self.degree,
            'speaks_dutch': self.speaks_dutch,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_first_gen': self.is_first_gen,
            'number_siblings': self.number_siblings,
            'birth_order': self.birth_order,
            'father_alive': self.father_alive,
            'mother_alive': self.mother_alive,
            'is_member': self.is_member,
            'student_association': self.student_association,
            'religious_background': self.religious_background,
            'is_working': self.is_working,
            'work_hours': self.work_hours,
            'student_job': self.student_job,
            'number_of_languages': self.number_of_languages,
            'level_of_english': self.level_of_english,
            'housing': self.housing,
            'experiences': self.experiences,
            'reason_for_uni': self.reason_for_uni,
            'hobbies': self.hobbies,
            'interesting_facts': self.interesting_facts,
            'father_profession': self.father_profession,
            'mother_profession': self.mother_profession,
            'father_income': self.father_income,
            'mother_income': self.mother_income,
            'personality': self.personality,
        }
