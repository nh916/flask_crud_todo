from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
app.static_folder = 'static'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add-to-do', methods=["GET", "POST"])
def add_to_do():
    if request.method == 'POST':
        todo_task = request.form.get('todo_task')
        print('task', todo_task)
        return redirect(url_for('add_to_do'))

    return render_template('to_do_app/create.html')


@app.route('/view-todo')
def view_to_do():
    # context = {
    #     'to_dos':
    # }
    return render_template('to_do_app/read.html')


if __name__ == "__main__":
    app.run(debug=True)
