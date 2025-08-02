from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
# Developed by https://www.linkedin.com/in/navdeepd2
app = Flask(__name__)
RESULTS_FILE = 'results.txt'
MAX_RESULTS = 25

def load_results():
    if not os.path.exists(RESULTS_FILE):
        return []
    with open(RESULTS_FILE, 'r') as f:
        lines = f.readlines()
    results = [json.loads(line.strip()) for line in lines[-MAX_RESULTS:]]
    return results[::-1]

def save_result(entry):
    with open(RESULTS_FILE, 'a') as f:
        f.write(json.dumps(entry) + '\n')

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    survival_data = None

    if request.method == 'POST':
        try:
            name = request.form.get('name').strip()
            savings = float(request.form.get('savings') or 0)
            mutual = float(request.form.get('mutual') or 0)
            ppf = float(request.form.get('ppf') or 0)
            others = float(request.form.get('others') or 0)

            rent = float(request.form.get('rent') or 0)
            food = float(request.form.get('food') or 0)
            car = float(request.form.get('car') or 0)
            subs = float(request.form.get('subs') or 0)

            total_assets = savings + mutual + ppf + others
            total_expenses = rent + food + car + subs

            if total_expenses <= 0:
                raise ValueError("Total expenses must be greater than 0.")

            survival_months = round(total_assets / total_expenses, 1)
            survival_years = round(survival_months / 12, 2)

            survival_data = {
                'months': survival_months,
                'years': survival_years
            }

            if name:
                entry = {
                    'name': name,
                    'months': survival_months,
                    'years': survival_years,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                save_result(entry)

        except ValueError:
            message = "Please enter valid numeric values."

    return render_template('index.html', message=message, survival_data=survival_data, total_assets=total_assets if survival_data else None, total_expenses=total_expenses if survival_data else None)

@app.route('/results')
def results():
    return jsonify(load_results())

if __name__ == '__main__':
    app.run(debug=True, port=4630)

