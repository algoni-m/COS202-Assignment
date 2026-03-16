# models.py
# ============================================================
# OOP Models for the Mini CBT Engine
# Defines Question and TestSession classes with state + behavior
# ============================================================

from datetime import datetime


class Question:
    """
    Represents a single multiple-choice question.
    State: question text, options list, correct answer index
    Behavior: check if a given answer is correct, serialize to dict
    """

    def __init__(self, text, options, correct_index):
        self.text          = text          # The question string
        self.options       = options       # List of 4 option strings
        self.correct_index = correct_index # Index (0-3) of the correct option

    def is_correct(self, chosen_index):
        """Return True if the chosen index matches the correct answer."""
        return int(chosen_index) == self.correct_index

    def get_correct_text(self):
        """Return the text of the correct answer."""
        return self.options[self.correct_index]

    def to_dict(self):
        """Serialize the question to a plain dictionary for Jinja templates."""
        return {
            "text"          : self.text,
            "options"       : self.options,
            "correct_index" : self.correct_index,
        }


class TestSession:
    """
    Represents a user's active test session.
    State: student name, score, answer history (stack), timestamp
    Behavior: record answers, compute grade, build result summary
    """

    # --- Grade thresholds ---
    GRADE_MAP = [
        (90, "Outstanding",  "🏆"),
        (75, "Excellent",    "🎉"),
        (60, "Good Pass",    "👍"),
        (50, "Pass",         "✅"),
        (0,  "Needs Review", "📚"),
    ]

    def __init__(self, student_name, total_questions):
        self.student_name    = student_name
        self.total_questions = total_questions
        self.score           = 0
        self.submitted_at    = None   # set when test is submitted

        # DATA STRUCTURE — Stack (LIFO)
        # We use a list as a stack to record each answer in order.
        # .append() pushes onto the stack; we can .pop() to undo the last
        # answer if we ever add an "undo" feature. This satisfies the
        # assignment's Stack (LIFO) requirement.
        self._answer_stack = []

    def record_answer(self, question, chosen_index):
        """
        Push an answer record onto the stack.
        Each record stores the question, chosen option, correct option,
        and whether the answer was correct.
        """
        correct = question.is_correct(chosen_index)
        if correct:
            self.score += 1

        self._answer_stack.append({
            "question"     : question.text,
            "chosen"       : question.options[int(chosen_index)],
            "correct_ans"  : question.get_correct_text(),
            "is_correct"   : correct,
        })

    def submit(self):
        """Stamp the submission time using Python's datetime module."""
        self.submitted_at = datetime.now()

    def get_percentage(self):
        """Calculate percentage score."""
        return round((self.score / self.total_questions) * 100)

    def get_grade(self):
        """Return (grade label, emoji) based on percentage."""
        pct = self.get_percentage()
        for threshold, label, emoji in self.GRADE_MAP:
            if pct >= threshold:
                return label, emoji
        return "Needs Review", "📚"

    def get_timestamp(self):
        """Return a human-readable timestamp string."""
        if self.submitted_at:
            return self.submitted_at.strftime("%A, %d %B %Y — %I:%M:%S %p")
        return "Not submitted"

    def get_answers(self):
        """Return the full answer history list (from the stack)."""
        return list(self._answer_stack)

    def to_result_dict(self):
        """Build the complete result payload sent to the results template."""
        grade_label, grade_emoji = self.get_grade()
        return {
            "student_name"   : self.student_name,
            "score"          : self.score,
            "total"          : self.total_questions,
            "percentage"     : self.get_percentage(),
            "grade"          : grade_label,
            "emoji"          : grade_emoji,
            "timestamp"      : self.get_timestamp(),
            "answers"        : self.get_answers(),
        }
