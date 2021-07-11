import datetime

from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime

app = Flask(__name__)
app.static_folder = 'static'
app.config['SECRET_KEY'] = 'MY_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    task = db.Column(db.VARCHAR(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'id: {self.id} task: {self.task} date_created: {self.date_created}'


db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add-to-do', methods=["GET", "POST"])
def add_to_do():
    if request.method == 'POST':
        todo_task = request.form.get('todo_task')
        todo_for_db = Todo(task=todo_task)
        db.session.add(todo_for_db)
        db.session.commit()

        return redirect(url_for('view_to_do'))

    return render_template('to_do_app/create.html')


@app.route('/view-to-do')
def view_to_do():
    context = {
        'task': 1,
        'date': 1,
        'id': 1
    }
    return render_template('to_do_app/read.html')


@app.route('/update-to-do')
def update_to_do():
    pass


@app.route('/delete-to-do')
def delete_to_do():
    pass


if __name__ == "__main__":
    app.run(debug=True)
