from flask import Flask, session, request, render_template, url_for, redirect, flash
import requests
import json

app = Flask(__name__)
app.secret_key = 'MY SECRET KEY'
AUTH_USERS_COOKIES = {}

@app.route('/')
def books():
    if session.get('email', False):
        result = requests.get(
            'https://mybook.ru/api/bookuserlist/',
            cookies=AUTH_USERS_COOKIES[session['email']],
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
        user = request.form['email']
        result = requests.post(
            'https://mybook.ru/api/auth/',
            json={
                "email": user,
                "password": request.form['password']
            }
        )
        if result.status_code != 200:
            flash('Please enter a valid email or password!')
            return redirect(url_for('login'))
        else:
            global AUTH_USERS_COOKIES
            AUTH_USERS_COOKIES[user] = result.cookies
            session['email'] = user
            return redirect(url_for('books'))


@app.route('/logout')
def logout():
    global AUTH_USERS_COOKIES
    AUTH_USERS_COOKIES.pop(session['email'], None)
    session.pop('email', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run()
