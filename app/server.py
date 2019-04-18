from flask import Flask, session, request, render_template, url_for, redirect, flash
import requests
import json

app = Flask(__name__)
app.secret_key = 'MY SECRET KEY'

@app.route('/')
def books():
    if session.get('email', False):
        result = requests.get(
            'https://mybook.ru/api/bookuserlist/',
            cookies=AUTH_COOKIES,
            headers={
                'Accept': 'application/json; version=5'
                }
        ).json()
        data = result['objects']
        return render_template('books.html', data=data, name=session['email'], len=len(data))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        result = requests.post(
            'https://mybook.ru/api/auth/',
            json={
                "email": request.form['email'],
                "password": request.form['password']
            }
        )
        if result.status_code != 200:
            flash('Please enter a valid email or password!')
            return redirect(url_for('login'))
        else:
            global AUTH_COOKIES
            AUTH_COOKIES = result.cookies
            session['email'] = request.form['email']
            return redirect(url_for('books'))


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run()
