# 📋 Mini CBT Engine

A Flask-powered Computer-Based Test (CBT) application built for **COS 202 — Assignment 4**.  
Students enter their name, answer 10 multiple-choice questions, and receive a timestamped result page with a full answer breakdown.

---

## What the App Does

- Welcomes the student and collects their name
- Presents 10 multiple-choice questions one at a time with a live progress bar and timer
- Tracks the student's score in a session
- Shows a results page with score, percentage, grade remark, submission timestamp, and a per-question answer review

---

## Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Backend    | Python 3 + Flask                    |
| OOP        | `Question` and `TestSession` classes in `models.py` |
| Data Structure | Stack (LIFO list) in `TestSession._answer_stack` |
| Standard API | `datetime` module for timestamping |
| Frontend   | Jinja2 HTML templates + plain CSS/JS |

---

## Project Structure

```
cbt_engine/
├── app.py              # Flask routes
├── models.py           # OOP classes (Question, TestSession)
├── requirements.txt    # Python dependencies
├── README.md
└── templates/
    ├── base.html       # Shared layout + global CSS
    ├── index.html      # Welcome / name entry page
    ├── question.html   # Question display page
    └── results.html    # Results + answer review page
```

---

## How to Run the App Locally

Follow these steps exactly. You only need to do steps 1–3 once.

### Step 1 — Make sure Python is installed

Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux) and type:

```bash
python --version
```

You should see something like `Python 3.10.0`. If not, download Python from [python.org](https://python.org).

---

### Step 2 — Download or clone this project

If you have Git installed:

```bash
git clone https://github.com/YOUR_USERNAME/cbt-engine.git
cd cbt-engine
```

Or just download the ZIP from GitHub and extract it, then open your terminal inside the folder.

---

### Step 3 — Install Flask

In your terminal (inside the project folder), run:

```bash
pip install -r requirements.txt
```

This installs Flask — the only dependency.

---

### Step 4 — Run the app

```bash
python app.py
```

You should see:

```
 * Running on http://127.0.0.1:5000
```

---

### Step 5 — Open it in your browser

Go to: **http://127.0.0.1:5000**

The app will load. Enter your name and start the test!

---

## Routes Summary

| Route       | Method | Description                        |
|-------------|--------|------------------------------------|
| `/`         | GET    | Welcome page (enter name)          |
| `/start`    | POST   | Validates name, starts session     |
| `/question` | GET    | Shows current question             |
| `/submit`   | POST   | Records answer, moves to next      |
| `/results`  | GET    | Shows final results + timestamp    |
| `/restart`  | GET    | Clears session, returns to home    |

---

## Assignment Requirements Checklist

- [x] **OOP** — `Question` class with `is_correct()`, `get_correct_text()`, `to_dict()` methods. `TestSession` class with `record_answer()`, `submit()`, `get_grade()`, `to_result_dict()` methods.
- [x] **Stack (LIFO)** — `TestSession._answer_stack` uses `.append()` and is readable via `.pop()` for potential undo feature.
- [x] **datetime module** — `TestSession.submit()` stamps `datetime.now()` and formats it with `.strftime()`.
- [x] **Flask routes** — 6 working routes covering all app flows.
- [x] **HTML forms** — Name form (`/start`) and answer form (`/submit`) use `request.form`.
- [x] **README** — This file.

---

*Built by Algoni Mohammed — MAAUN, COS 202 — Assignment 4*
   *Due Date: 20th March 2026*
