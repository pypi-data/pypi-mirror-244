import glob
import json
import json5
import math
import os
import random
import string

import quizgen.constants
import quizgen.parser
import quizgen.util.file
import quizgen.util.git

QUIZ_FILENAME = 'quiz.json'
GROUP_FILENAME = 'group.json'
QUESTION_FILENAME = 'question.json'
PROMPT_FILENAME = 'prompt.md'

class Quiz(object):
    def __init__(self, title = '', description = '',
            practice = True, published = False,
            time_limit = 30, shuffle_answers = True,
            hide_results = None, show_correct_answers = True,
            assignment_group_name = "Quizzes",
            groups = [],
            base_dir = '.',
            version = None,
            **kwargs):
        self.title = title
        self.description = description
        self.practice = practice
        self.published = published
        self.time_limit = time_limit
        self.shuffle_answers = shuffle_answers
        self.hide_results = hide_results
        self.show_correct_answers = show_correct_answers
        self.assignment_group_name = assignment_group_name

        self.groups = groups

        self.version = version
        self.base_dir = base_dir

        try:
            self.validate()
        except Exception as ex:
            raise QuizValidationError(f"Error while validating quiz.") from ex

    def validate(self):
        if ((self.title is None) or (self.title == "")):
            raise QuizValidationError("Title cannot be empty.")

        if ((self.description is None) or (self.description == "")):
            raise QuizValidationError("Description cannot be empty.")

        if (self.version is None):
            self.version = quizgen.util.git.get_version(self.base_dir, throw = True)

    def to_dict(self):
        value = self.__dict__.copy()
        value['groups'] = [group.to_dict() for group in self.groups]
        return value

    @staticmethod
    def from_path(path):
        with open(path, 'r') as file:
            quiz_info = json5.load(file)

        base_dir = os.path.dirname(path)

        quiz_info['groups'] = [Group.from_dict(group_info, base_dir) for group_info in quiz_info.get('groups', [])]

        return Quiz(base_dir = base_dir, **quiz_info)

    def to_json(self, indent = 4):
        return json.dumps(self.to_dict(), indent = indent)

    # TODO
    def to_html(self, **kwargs):
        raise NotImplementedError()

    # TODO
    def to_markdown(self, **kwargs):
        raise NotImplementedError()

    # TODO
    def to_tex(self, **kwargs):
        raise NotImplementedError()

    def to_format(self, format, **kwargs):
        if (format == quizgen.constants.DOC_FORMAT_HTML):
            return self.to_html(**kwargs)
        elif (format == quizgen.constants.DOC_FORMAT_JSON):
            return self.to_json(**kwargs)
        elif (format == quizgen.constants.DOC_FORMAT_MD):
            return self.to_markdown(**kwargs)
        elif (format == quizgen.constants.DOC_FORMAT_TEX):
            return self.to_tex(**kwargs)
        else:
            raise QuizValidationError(f"Unknown format '{format}'.")

class Group(object):
    def __init__(self, name = '',
            pick_count = 1, points = 10,
            questions = [], **kwargs):
        self.name = name
        self.pick_count = pick_count
        self.points = points

        self.questions = questions

        try:
            self.validate()
        except Exception as ex:
            raise QuizValidationError(f"Error while validating group.") from ex

    def validate(self):
        if ((self.name is None) or (self.name == "")):
            raise QuizValidationError("Name cannot be empty.")

    def to_dict(self):
        value = self.__dict__.copy()
        value['questions'] = [question.to_dict() for question in self.questions]
        return value

    def collect_file_paths(self):
        paths = []

        for question in self.questions:
            paths += question.collect_file_paths()

        return paths

    @staticmethod
    def from_dict(group_info, base_dir):
        group_info = group_info.copy()

        questions = []
        for path in group_info.get('questions', []):
            if (not os.path.isabs(path)):
                path = os.path.join(base_dir, path)

            path = os.path.abspath(path)

            questions += _parse_questions(path)

        group_info['questions'] = questions

        return Group(**group_info)

class Question(object):
    def __init__(self, prompt = '', question_type = '', answers = [],
            base_dir = '.',
            **kwargs):
        self.base_dir = base_dir

        self.prompt = prompt

        self.question_type = question_type
        self.answers = answers

        try:
            self.validate()
        except Exception as ex:
            raise QuizValidationError(f"Error while validating question.") from ex

    def validate(self):
        if ((self.prompt is None) or (self.prompt == "")):
            raise QuizValidationError("Prompt cannot be empty.")
        self.prompt_document = quizgen.parser.parse_text(self.prompt, base_dir = self.base_dir)

        if (self.question_type not in quizgen.constants.QUESTION_TYPES):
            raise QuizValidationError(f"Unknown question type: '{self.question_type}'.")

        self._validate_answers()

    def _validate_answers(self):
        if (self.question_type == quizgen.constants.QUESTION_TYPE_ESSAY):
            if (not isinstance(self.answers, list)):
                raise QuizValidationError("Essay questions cannot have answers.")

            if (len(self.answers) != 0):
                raise QuizValidationError("Essay questions cannot have answers.")
        elif (self.question_type == quizgen.constants.QUESTION_TYPE_FILL_IN_MULTIPLE_BLANKS):
            self._validate_fimb_answers()
        elif (self.question_type == quizgen.constants.QUESTION_TYPE_MATCHING):
            self._validate_matching_answers()
        elif (self.question_type == quizgen.constants.QUESTION_TYPE_MULTIPLE_ANSWERS):
            self._validate_answer_list(self.answers)
        elif (self.question_type == quizgen.constants.QUESTION_TYPE_MULTIPLE_CHOICE):
            self._validate_answer_list(self.answers, min_correct = 1, max_correct = 1)
        elif (self.question_type == quizgen.constants.QUESTION_TYPE_MULTIPLE_DROPDOWNS):
            if (len(self.answers) == 0):
                raise QuizValidationError("No answers provided, at least one answer required.")

            for answers in self.answers.values():
                self._validate_answer_list(answers, min_correct = 1, max_correct = 1, parse = False)
        elif (self.question_type == quizgen.constants.QUESTION_TYPE_NUMERICAL):
            self._validate_numerical_answers()
        elif (self.question_type == quizgen.constants.QUESTION_TYPE_SHORT_ANSWER):
            self._validate_fitb_answers()
        elif (self.question_type == quizgen.constants.QUESTION_TYPE_TEXT_ONLY):
            if (not isinstance(self.answers, list)):
                raise QuizValidationError("Text-Only questions cannot have answers.")

            if (len(self.answers) != 0):
                raise QuizValidationError("Text-Only questions cannot have answers.")
        elif (self.question_type == quizgen.constants.QUESTION_TYPE_TF):
            self._validate_tf_answers()
        else:
            raise QuizValidationError(f"Unknown question type: '{self.question_type}'.")

    def _validate_tf_answers(self):
        if (not isinstance(self.answers, bool)):
            raise QuizValidationError(f"'answers' for a T/F question must be a boolean, found '{self.answers}' ({type(self.answers)}).")

        # Change answers to look like multiple choice.
        self.answers = [
            {"correct": self.answers, "text": 'True'},
            {"correct": (not self.answers), "text": 'False'},
        ]

        self._validate_answer_list(self.answers)

    def _validate_numerical_answers(self):
        _check_type(self.answers, list, "'answers' for a numerical question")

        for answer in self.answers:
            label = "values of 'answers' for a numerical question"
            _check_type(answer, dict, label)

            if ('type' not in answer):
                raise QuizValidationError(f"Missing key ('type') for {label}.")

            if (answer['type'] == quizgen.constants.NUMERICAL_ANSWER_TYPE_EXACT):
                required_keys = ['value', 'margin']
            elif (answer['type'] == quizgen.constants.NUMERICAL_ANSWER_TYPE_RANGE):
                required_keys = ['min', 'max']
            elif (answer['type'] == quizgen.constants.NUMERICAL_ANSWER_TYPE_PRECISION):
                required_keys = ['value', 'precision']
            else:
                raise QuizValidationError(f"Unknown numerical answer type: '{answer['type']}'.")

            for key in required_keys:
                if (key not in answer):
                    raise QuizValidationError(f"Missing required key '{key}' for numerical answer type '{answer['type']}'.")

    def _validate_fitb_answers(self):
        """
        "Short Answer" questions are actually fill in the blank questions.
        Just set up the answers to look like fill in multiple blanks with an empty key.
        """

        label = "short answer (fill in the blank)"

        _check_type(self.answers, list, f"{label} answers")

        if (len(self.answers) == 0):
            raise QuizValidationError(f"Expected {label} answers to be non-empty.")

        self.answers = {"": self.answers}

        self._validate_fimb_answers(label = label)

    def _validate_fimb_answers(self, label = 'fill in multiple blanks'):
        if (not isinstance(self.answers, dict)):
            raise QuizValidationError(f"Expected dict for {label} answers, found {type(self.answers)}.")

        if (len(self.answers) == 0):
            raise QuizValidationError(f"Expected {label} answers to be non-empty.")

        for (key, values) in self.answers.items():
            if (not isinstance(values, list)):
                self.answers[key] = [values]

        for (key, values) in self.answers.items():
            _check_type(key, str, f"key for {label} answers")

            if (len(values) == 0):
                raise QuizValidationError(f"Expected {label} possible values to be non-empty.")

            for value in values:
                _check_type(value, str, f"value for {label} answers")

    def _validate_matching_answers(self):
        if (not isinstance(self.answers, dict)):
            raise QuizValidationError(f"Expected dict for matching answers, found {type(self.answers)}.")

        if ('matches' not in self.answers):
            raise QuizValidationError("Matching answer type is missing the 'matches' field.")

        for match in self.answers['matches']:
            if (len(match) != 2):
                raise QuizValidationError(f"Expected exactly two items for a match list, found {len(match)}.")

        if ('distractors' not in self.answers):
            self.answers['distractors'] = []

        for i in range(len(self.answers['distractors'])):
            distractor = self.answers['distractors'][i]
            if (not isinstance(distractor, str)):
                raise QuizValidationError(f"Distractors must be strings, found {type(distractor)}.")

            distractor = distractor.strip()

            if ("\n" in distractor):
                raise QuizValidationError(f"Distractors cannot have newlines, found {type(distractor)}.")

            self.answers['distractors'][i] = distractor

    def _validate_answer_list(self, answers, min_correct = 0, max_correct = math.inf, parse = True):
        if (not isinstance(answers, list)):
            raise QuizValidationError(f"Expected answers to be a list, found {type(answers)} (base_dir: '{self.base_dir}'.")

        if (len(answers) == 0):
            raise QuizValidationError(f"No answers provided, at least one answer required.")

        num_correct = 0
        for answer in answers:
            self._validate_answer(answer, parse = parse)
            if (answer['correct']):
                num_correct += 1

        if (num_correct < min_correct):
            raise QuizValidationError(f"Did not find enough correct answers. Expected at least {min_correct}, found {num_correct} (base_dir: '{self.base_dir}'.")

        if (num_correct > max_correct):
            raise QuizValidationError(f"Found too many correct answers. Expected at most {max_correct}, found {num_correct} (base_dir: '{self.base_dir}'.")

    def _validate_answer(self, answer, parse = True):
        if ('correct' not in answer):
            raise QuizValidationError(f"Answer has no 'correct' field (base_dir: '{self.base_dir}'.")

        if ('text' not in answer):
            raise QuizValidationError(f"Answer has no 'text' field (base_dir: '{self.base_dir}'.")

        if (parse):
            answer['document'] = quizgen.parser.parse_text(answer['text'], base_dir = self.base_dir)

    def to_dict(self):
        value = self.__dict__.copy()

        value['prompt_document'] = self.prompt_document.to_pod()
        value['answers'] = self._answers_to_dict(self.answers)

        return value

    def _answers_to_dict(self, target):
        if (isinstance(target, dict)):
            return {key: self._answers_to_dict(value) for (key, value) in target.items()}
        elif (isinstance(target, list)):
            return [self._answers_to_dict(answer) for answer in target]
        elif (isinstance(target, quizgen.parser.ParseNode)):
            return target.to_pod()
        else:
            return target

    def collect_file_paths(self):
        paths = []

        paths += self.prompt_document.collect_file_paths(self.base_dir)

        for document in self._collect_documents(self.answers):
            paths += document.collect_file_paths(self.base_dir)

        return paths

    def _collect_documents(self, target):
        if (isinstance(target, dict)):
            return self._collect_documents(list(target.values()))
        elif (isinstance(target, list)):
            documents = []
            for value in target:
                documents += self._collect_documents(value)
            return documents
        elif (isinstance(target, quizgen.parser.ParseNode)):
            return [target]
        else:
            return []

    @staticmethod
    def from_path(path):
        with open(path, 'r') as file:
            question_info = json5.load(file)

        # Check for a prompt file.
        prompt_path = os.path.join(os.path.dirname(path), PROMPT_FILENAME)
        if (os.path.exists(prompt_path)):
            question_info['prompt'] = quizgen.util.file.read(prompt_path)

        base_dir = os.path.dirname(path)

        return Question(base_dir = base_dir, **question_info)

def _parse_questions(path):
    if (not os.path.exists(path)):
        raise QuizValidationError(f"Question path does not exist: '{path}'.")

    if (os.path.isfile(path)):
        return [Question.from_path(path)]

    questions = []
    for subpath in sorted(glob.glob(os.path.join(path, '**', QUESTION_FILENAME), recursive = True)):
        questions.append(Question.from_path(subpath))

    return questions

def _check_type(value, expected_type, label):
    if (not isinstance(value, expected_type)):
        raise QuizValidationError(f"{label} must be a {expected_type}, found '{value}' ({type(value)}).")

class QuizValidationError(ValueError):
    pass

LATEX_QUIZ_TEMPLATE = r"""
    \documentclass{exam}

    \title{%%title%%}

    \begin{document}

        \maketitle

        \begin{center}
            \fbox{\fbox{\parbox{5.5in}{\centering
                Answer the questions in the spaces provided.
                If you run out of room for an answer, continue on the back of the page.
            }}}
        \end{center}

        \vspace{5mm}
        \makebox[0.75\textwidth]{Name:\enspace\hrulefill}

        \vspace{5mm}
        \makebox[0.75\textwidth]{CruzID:\enspace\hrulefill}

        \begin{questions}

            %%groups%%

        \end{questions}
    \end{document}
"""

LATEX_GROUP_TEMPLATE = r"""
    \question
    %%name%%

    %%question%%

"""

LATEX_QUESTION_TEMPLATE = r"""
    %%prompt%%
    \\
    %%answers%%
"""
