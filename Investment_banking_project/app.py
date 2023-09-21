from flask import Flask, render_template, request, redirect, url_for
import openai

app = Flask(__name__)
openai.api_key = "" # Replace with your OpenAI API key

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        prompt = request.form['prompt']
        return redirect(url_for('form', prompt=prompt))
    return render_template('chatbot.html')

@app.route('/form/<prompt>', methods=['GET', 'POST'])
def form(prompt):
    if request.method == 'POST':
        client_name = request.form['clientName']
        residency = request.form['residency']
        net_worth = float(request.form['netWorth'])
        criminal_background = request.form['criminalBackground']
        restricted_countries = request.form['restrictedCountries']

        # Check eligibility
        eligibility = check_eligibility(net_worth, restricted_countries, criminal_background)

        return render_template('result.html', eligibility=eligibility)

    return render_template('form.html', prompt=prompt)

def check_eligibility(net_worth, restricted_countries, criminal_background):
    if net_worth >= 30000000 and restricted_countries not in ['Syria', 'Pakistan', 'Cuba', 'Iran', 'Afghanistan', 'Bangladesh', 'North Korea', 'Sudan', 'Crimea', 'Zimbabwe', 'Venezuela'] and criminal_background == 'No':
        return "Eligible for investing"
    else:
        return "Not eligible for investing"

if __name__ == '__main__':
    app.run(debug=True)
