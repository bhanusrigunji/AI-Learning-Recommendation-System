from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
import random
app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'

db = SQLAlchemy(app)


# Student Table
class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    email = db.Column(db.String(100))

    password = db.Column(db.String(100))


# Load Questions from JSON File
with open('data/questions.json', 'r') as file:
    quiz_data = json.load(file)


# Home Page
@app.route('/')
def home():
    return render_template('index.html')


# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_student = Student(
            name=name,
            email=email,
            password=password
        )

        db.session.add(new_student)
        db.session.commit()

        return "Registration Successful"

    return render_template('register.html')


# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        student = Student.query.filter_by(
            email=email,
            password=password
        ).first()

        if student:
            return render_template('dashboard.html')

        else:
            return "Invalid Email or Password"

    return render_template('login.html')


# Subjects Page
@app.route('/subjects')
def subjects():
    return render_template('subjects.html')


# Quiz Page
@app.route('/quiz/<subject>', methods=['GET', 'POST'])
def quiz(subject):

    questions = random.sample(
    quiz_data[subject],
    min(3, len(quiz_data[subject]))
)

    score = 0

    weak_topics = []

    # Video Recommendations
    video_recommendations = {
        "Introduction": "https://www.youtube.com/watch?v=rfscVS0vtbw",
        "Functions": "https://www.youtube.com/watch?v=9Os0o3wzS_I",
        "Loops": "https://www.youtube.com/watch?v=6iF8Xb7Z3wQ",
        "SQL": "https://www.youtube.com/watch?v=HXV3zeQKqGY"
    }

    if request.method == 'POST':

        for i, question in enumerate(questions):

            selected_answer = request.form.get(f'q{i+1}')

            correct_answer = question['answer']

            if selected_answer == correct_answer:
                score += 1

            else:
                weak_topics.append(question['topic'])

        recommended_videos = []

        for topic in weak_topics:

            if topic in video_recommendations:
                recommended_videos.append(
                    video_recommendations[topic]
                )

        return render_template(
            'result.html',
            score=score,
            total=len(questions),
            weak_topics=weak_topics,
            recommended_videos=recommended_videos,
            subject=subject
        )

    return render_template(
        'quiz.html',
        questions=questions,
        subject=subject
    )


# Run Application
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)