from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(_name_)

# Fetch the database URL from Render's environment, fallback to local MySQL for local testing
db_url = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:Hetm189@localhost/Notes_App')

# Render's Postgres URLs start with "postgres://", but SQLAlchemy requires "postgresql://"
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    notes = Note.query.all()
    return render_template('index.html', notes=notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_note = Note(title=title, content=content)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_note.html')

@app.route('/edit_note/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    note = Note.query.get_or_404(id)

    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit_note.html', note=note)

@app.route('/delete_note/<int:id>')
def delete_note(id):
    note = Note.query.get_or_404(id)

    db.session.delete(note)
    db.session.commit()

    return redirect(url_for('home'))

if _name_ == "_main_":
    app.run(host='0.0.0.0', port=5000, debug=True)