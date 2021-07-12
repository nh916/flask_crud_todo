import datetime

from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.static_folder = 'static'
app.config['SECRET_KEY'] = 'MY_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    task = db.Column(db.VARCHAR(100), nullable=False)
    status = db.Column(db.VARCHAR(11), nullable=False, default='Not Started')
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
        try:
            todo_task = request.form.get('todo_task')
            todo_task_status = request.form.get('todo_status')

            todo_for_db = Todo(task=todo_task, status=todo_task_status)

            db.session.add(todo_for_db)
            db.session.commit()

        except Exception:
            print(Exception)
            return 'There was an error'

        return redirect(url_for('view_to_do'))

    return render_template('to_do_app/create.html')


@app.route('/view-to-do')
def view_to_do():
    try:
        all_todos_query = Todo.query.order_by(desc(Todo.date_created)).all()
    except IndexError:
        return 'Please insert data first'

    return render_template('to_do_app/read.html', all_todos_query=all_todos_query)


@app.route('/update-to-do/<id_number>', methods=['GET', 'POST'])
def update_to_do(id_number):
    if request.method == 'POST':
        original_task = db.session.query(Todo).get(id_number)

        original_task.task = request.form.get('todo_task')
        original_task.status = request.form.get('todo_status')
        original_task.date_created = datetime.datetime.utcnow()
        db.session.commit()

        return redirect(url_for('view_to_do'))

    if request.method == 'GET':
        the_todo = db.session.query(Todo).get_or_404(id_number)

        return render_template('to_do_app/update.html', the_todo=the_todo)


@app.route('/delete-to-do/<id_number>', methods=['POST'])
def delete_to_do(id_number):
    if request.method == 'POST':
        try:
            Todo.query.filter_by(id=id_number).delete()
            db.session.commit()

            return 'ok', 200
        except Exception:
            return 'Err', 500


if __name__ == "__main__":
    app.run(debug=True)
