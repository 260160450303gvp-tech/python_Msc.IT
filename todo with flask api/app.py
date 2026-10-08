from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Todo Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(300))
    priority = db.Column(db.String(20), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date, nullable=False)


# Create database
with app.app_context():
    db.create_all()


# Home Page
@app.route("/")
def index():
    pending = Todo.query.filter_by(is_completed=False).all()
    completed = Todo.query.filter_by(is_completed=True).all()

    return render_template(
        "home.html",
        pending=pending,
        completed=completed
    )


# Add Task
@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    description = request.form["description"]
    priority = request.form["priority"]
    due_date = datetime.strptime(
        request.form["due_date"], "%Y-%m-%d"
    ).date()

    task = Todo(
        title=title,
        description=description,
        priority=priority,
        due_date=due_date
    )

    db.session.add(task)
    db.session.commit()

    return redirect("/")


# Toggle Complete / Pending
@app.route("/toggle/<int:id>")
def toggle(id):
    task = Todo.query.get_or_404(id)

    task.is_completed = not task.is_completed

    db.session.commit()

    return redirect("/")


# Update Task
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    task = Todo.query.get_or_404(id)

    task.title = request.form["title"]
    task.description = request.form["description"]
    task.priority = request.form["priority"]

    task.due_date = datetime.strptime(
        request.form["due_date"], "%Y-%m-%d"
    ).date()

    db.session.commit()

    return redirect("/")


# Delete Task
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    task = Todo.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return redirect("/")


# API - Get Tasks
@app.route("/api/tasks")
def api_tasks():

    tasks = Todo.query.all()

    data = []

    for task in tasks:
        data.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "is_completed": task.is_completed,
            "due_date": str(task.due_date)
        })

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)