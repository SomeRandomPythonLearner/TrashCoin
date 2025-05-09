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
    value = 1 / session['s'],
    return render_template('index.html', coins=session['coins'], value=value)

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
    session['pending_cost'] = cost
    return render_template(
        'index.html',
        coins=session['coins'],
        value=session['current_cost'],
        confirm_cost=cost,
        mine_count=mine_count
    )
@app.route('/mine', methods=['POST'])
def mine():
    if 'coins' not in session or 'current_cost' not in session:
        return redirect(url_for('index'))

    cost_per_mine = session['current_cost']
    mine_count = int(request.form['mine_count'])
    total_cost = mine_count * cost_per_mine

    # Allow mining even with negative coins
    session['coins'] -= total_cost

    # Perform mining
    gained = 0
    for _ in range(mine_count):
        a, b, c = random.randint(0, 10), random.randint(0, 10), random.randint(0, 10)
        if a == b == c:
            gained += 1
            session['coins'] += 1

    profit = gained - total_cost

    # Store results for confirmation
    session['last_result'] = {
        'gained': gained,
        'cost': total_cost,
        'profit': profit,
        'mine_count': mine_count
    }

    return redirect('/confirm_mining')

@app.route('/confirm_mining', methods=['GET'])
def confirm_mining():
    result = session.pop('last_result', None)
    if not result:
        return redirect(url_for('index'))

    return render_template(
        'result.html',
        gained=result['gained'],
        cost=result['cost'],
        profit=result['profit'],
        coins=session['coins'],
        mine_count=result['mine_count']
    )
