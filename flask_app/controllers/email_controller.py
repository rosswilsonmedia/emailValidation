from flask import render_template, redirect, request, session, flash

from flask_app import app
from ..models.email import Email

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if Email.validate_email(request.form):
        Email.save(request.form)
        return redirect('/success')
    else:
        return redirect('/')

@app.route('/success')
def success():
    results=Email.get_all()
    return render_template('success.html', all_emails=results)

@app.route('/delete/<int:id>')
def delete(id):
    data={
        'id':id
    }
    Email.delete(data)
    return redirect('/success')