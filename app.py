from flask import Flask, render_template, request, redirect, session, url_for
import random
import time

app = Flask(__name__)
app.secret_key = 'trashcoinkey'  # Needed for session

def get_value():
    return round(100 + random.randint(-10, 10)/10, 6)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'coins' not in session:
        session['coins'] = 10
        session['s'] = get_value()

    message = ""

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'view':
            message = f"You have {session['coins']} TrashCoins."

        elif action == 'value':
            session['s'] = get_value()
            message = f"1 mine costs {1 / session['s']:.6f} TrashCoins."

        elif action == 'load':
            session['coins'] = 10
            session['s'] = get_value()
            message = "Game data reset. (Simulated load)"

        elif action == 'mine':
            try:
                n = int(request.form.get('num_mines'))
                s = session['s']
                spent = n / s
                if spent < 0:
                    raise ValueError()
                session['coins'] -= spent

                gained = 0
                for _ in range(n):
                    a = random.randint(0, 10)
                    b = random.randint(0, 10)
                    c = random.randint(0, 10)
                    if a == b == c:
                        gained += 1
                session['coins'] += gained
                profit = gained - spent
                message = f"You spent {spent:.2f} coins and gained {gained} coins. Total profit: {profit:.2f} coins."

            except:
                message = "Please enter a valid number of minings."

    return render_template("index.html", message=message, coins=round(session['coins'], 2))
from flask import Flask, render_template, request, redirect, url_for, session

@app.route('/start_mining', methods=['POST'])
def start_mining():
    num_mines = int(request.form['num_mines'])
    session['num_mines'] = num_mines
    cost = num_mines / session['s']
    return render_template('confirm.html', cost=round(cost, 2), num_mines=num_mines)

@app.route('/confirm_mining', methods=['POST'])
def confirm_mining():
    num_mines = session.pop('num_mines', 0)
    cost = num_mines / session['s']
    session['coins'] -= cost

    gained = 0
    for _ in range(num_mines):
        if random.randint(0, 10) == random.randint(0, 10) == random.randint(0, 10):
            session['coins'] += 1
            gained += 1

    profit = gained - cost
    return render_template('result.html', gained=gained, cost=round(cost, 2), profit=round(profit, 2))

if __name__ == '__main__':
    app.run(debug=True)
