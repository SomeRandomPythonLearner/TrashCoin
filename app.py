from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = 'trashcoin-key'  # Required for session to work

@app.route('/')
def index():
    if 'coins' not in session:
        session['coins'] = 10
    if 's' not in session:
        session['s'] = 100
    value = round(1 / session['s'], 4)
    return render_template('index.html', coins=round(session['coins'], 2), value=value)

@app.route('/get_value')
def get_value():
    session['s'] += random.randint(-10, 10) / 1000000
    value = 1 / session['s']
    return {'value': value}

@app.route('/start_mining', methods=['POST'])
def start_mining():
    try:
        num_mines = int(request.form['num_mines'])
        session['num_mines'] = num_mines
        cost = num_mines / session['s']
        return render_template('confirm.html', cost=round(cost, 2), num_mines=num_mines)
    except Exception as e:
        return f"Error: {e}"

@app.route('/confirm_mining', methods=['POST'])
def confirm_mining():
    num_mines = session.pop('num_mines', 0)
    cost = num_mines / session['s']
    session['coins'] -= cost

    gained = 0
    for _ in range(num_mines):
        a = random.randint(0, 10)
        b = random.randint(0, 10)
        c = random.randint(0, 10)
        if a == b == c:
            session['coins'] += 1
            gained += 1

    profit = gained - cost
    return render_template('result.html', gained=gained, cost=round(cost, 2), profit=round(profit, 2), coins=round(session['coins'], 2))

if __name__ == '__main__':
    app.run(debug=True)
