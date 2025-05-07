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
    session['s'] += random.uniform(-0.01, 0.01)
    cost = 1 / session['s']
    session['current_cost'] = cost  # store this value for later mining
    return {'value': cost}
    
@app.route('/calculate_cost', methods=['POST'])
def calculate_cost():
    mine_count = int(request.form['mine_count'])
    cost = mine_count * session.get('current_cost', 0.01)
    session['pending_mines'] = mine_count
    return render_template(
        'index.html',
        coins=round(session['coins'], 2),
        value=round(session['current_cost'], 6),
        confirm_cost=round(cost, 4),
        mine_count=mine_count
    )

@app.route('/mine', methods=['POST'])
def mine():
    if 'coins' not in session or 'current_cost' not in session:
        return redirect(url_for('index'))

    cost = session['current_cost']  # use frozen cost value
    n = int(request.form['mine_count'])
    total_cost = n * cost

    if session['coins'] < total_cost:
        message = "Not enough coins."
    else:
        session['coins'] -= total_cost
        gained = sum(
            1 for _ in range(n)
            if random.randint(0, 10) == random.randint(0, 10) == random.randint(0, 10)
        )
        session['coins'] += gained
        message = f"You spent {total_cost:.4f} coins and gained {gained} coins. Profit: {gained - total_cost:.4f} coins."

    return render_template("index.html", message=message, coins=round(session['coins'], 2), value=session['current_cost'])

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
