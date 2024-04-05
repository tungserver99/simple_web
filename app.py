from flask import Flask, request, session, redirect, url_for, render_template
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1",
    database="SimpleAuth"
)
cursor = db_connection.cursor()

# Routes
@app.route('/')
def home():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone_number = request.form['phone_number']
        cursor.execute("INSERT INTO users (username, password, email, phone_number) VALUES (%s, %s, %s, %s)",
                       (username, password, email, phone_number))
        db_connection.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
