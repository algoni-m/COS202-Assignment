# app.py
# ============================================================
# Mini CBT Engine — Flask Application Entry Point
# Routes: /  /start  /question  /submit  /results  /restart
# ============================================================

from flask import Flask, render_template, request, session, redirect, url_for
from models import Question, TestSession

app = Flask(__name__)

# Secret key required for Flask's client-side session (cookie)
app.secret_key = "cbt_engine_secret_2026"  # Required for Flask session cookies


# ============================================================
   # QUESTION BANK — 10 hardcoded multiple-choice questions
   # Topics: HTML, Python, OOP, Data Structures, General Knowledge
   # ============================================================
QUESTIONS = [
    Question("What does HTML stand for?",
             ["HyperText Markup Language", "HighText Machine Language",
              "Hyperloop Markup Logic", "HyperTransfer Markup Language"], 0),

    Question("Which data structure operates on a Last-In, First-Out (LIFO) principle?",
             ["Queue", "Linked List", "Stack", "Heap"], 2),

    Question("What is the capital city of Nigeria?",
             ["Lagos", "Kano", "Abuja", "Port Harcourt"], 2),

    Question("In Python, which keyword is used to define a function?",
             ["func", "define", "function", "def"], 3),

    Question("What does CSS stand for?",
             ["Creative Style Sheets", "Cascading Style Sheets",
              "Computer Style Syntax", "Coded Style Sheets"], 1),

    Question("Which planet is known as the Red Planet?",
             ["Venus", "Jupiter", "Saturn", "Mars"], 3),

    Question("In OOP, what best describes 'encapsulation'?",
             ["Hiding internal state and exposing only necessary methods",
              "Creating multiple objects from a class",
              "Inheriting properties from a parent class",
              "Overriding a parent method"], 0),

    Question("What symbol is used to start a comment in Python?",
             ["//", "/*", "#", "--"], 2),

    Question("Which of these is NOT a programming language?",
             ["Swift", "Kotlin", "Photoshop", "Rust"], 2),

    Question("What does 'HTTP' stand for?",
             ["HyperText Transfer Protocol", "High Transfer Text Program",
              "HyperTransfer Text Packet", "Hybrid Text Transfer Process"], 0),
]


# ============================================================
# ROUTE 1 — Home / Welcome page
# ============================================================
@app.route("/")
def index():
    """Render the welcome screen where the student enters their name."""
    return render_template("index.html")


# ============================================================
# ROUTE 2 — Start test (POST from welcome form)
# ============================================================
@app.route("/start", methods=["POST"])
def start():
    """
    Receive the student's name, initialise a fresh TestSession,
    store it in the Flask session (cookie), redirect to first question.
    """
    name = request.form.get("student_name", "").strip()
    if not name:
        return render_template("index.html", error="Please enter your name before starting.")

    # Serialise the new TestSession into the cookie
    session["student_name"]  = name
    session["current_q"]     = 0
    session["score"]         = 0
    session["answer_stack"]  = []   # Stack stored in session

    return redirect(url_for("question"))


# ============================================================
# ROUTE 3 — Display current question (GET)
# ============================================================
@app.route("/question")
def question():
    """
    Show the current question. If the test is complete, go to results.
    """
    if "student_name" not in session:
        return redirect(url_for("index"))

    idx = session.get("current_q", 0)

    if idx >= len(QUESTIONS):
        return redirect(url_for("results"))

    q        = QUESTIONS[idx]
    progress = round((idx / len(QUESTIONS)) * 100)
    letters  = ["A", "B", "C", "D"]

    return render_template(
        "question.html",
        question     = q.to_dict(),
        q_number     = idx + 1,
        total        = len(QUESTIONS),
        progress     = progress,
        letters      = letters,
        student_name = session["student_name"],
    )


# ============================================================
# ROUTE 4 — Submit answer for current question (POST)
# ============================================================
@app.route("/submit", methods=["POST"])
def submit_answer():
    """
    Receive the chosen option, record it via TestSession.record_answer(),
    advance to next question or show results.
    """
    if "student_name" not in session:
        return redirect(url_for("index"))

    chosen = request.form.get("chosen_index")
    if chosen is None:
        return redirect(url_for("question"))

    idx = session.get("current_q", 0)
    q   = QUESTIONS[idx]

    # Build a temporary TestSession just to use its record_answer logic
    ts = _load_session()
    ts.record_answer(q, int(chosen))
    _save_session(ts, idx + 1)

    return redirect(url_for("question"))


# ============================================================
# ROUTE 5 — Results page
# ============================================================
@app.route("/results")
def results():
    """
    Finalise the TestSession, stamp the submission time,
    and render the results page with full breakdown.
    """
    if "student_name" not in session:
        return redirect(url_for("index"))

    ts = _load_session()
    ts.submit()   # stamps datetime.now() via the datetime module

    result = ts.to_result_dict()
    return render_template("results.html", result=result)


# ============================================================
# ROUTE 6 — Restart (clear session, go home)
# ============================================================
@app.route("/restart")
def restart():
    """Clear the session and redirect to the welcome page."""
    session.clear()
    return redirect(url_for("index"))


# ============================================================
# HELPERS — load/save TestSession from Flask session cookie
# ============================================================
def _load_session():
    """
    Reconstruct a TestSession object from the Flask cookie data.
    We store primitives in the cookie and rebuild the object on each request.
    """
    ts = TestSession(session["student_name"], len(QUESTIONS))
    ts.score         = session.get("score", 0)
    ts._answer_stack = session.get("answer_stack", [])
    return ts


def _save_session(ts, next_q_index):
    """Persist TestSession state back into the Flask cookie."""
    session["student_name"] = ts.student_name
    session["score"]        = ts.score
    session["answer_stack"] = ts._answer_stack
    session["current_q"]    = next_q_index


# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)
