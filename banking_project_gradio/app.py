import gradio as gr
import openai
import re
from flask import Flask, request, render_template

# Set your OpenAI API key here
openai.api_key = ""

app = Flask(__name__)

def investor_form(investor_name):
    # Fetch investor details from the internet using OpenAI API
    prompt = f"Provide detailed information about the investor named {investor_name}. Include the investor's full name, country of residency, estimated net worth, and any information regarding criminal background or connections to restricted countries."
    response = openai.Completion.create(
        engine="text-davinci-003",  
        prompt=prompt,
        max_tokens=150
    )

    bot_response = response.choices[0].text

    # Print the bot's response for debugging
    print("Bot Response:", bot_response)

    
    name_pattern = r"Name:\s*(.+)"
    residency_pattern = r"Residency:\s*(.+)"
    # net_worth_pattern = r"Net Worth:\s*(.+)"
    net_worth_pattern = r"Net Worth: ([^\n]+)"
    criminal_background_pattern = r"Criminal Background:\s*(.+)"
    
    name_match = re.search(name_pattern, bot_response)
    residency_match = re.search(residency_pattern, bot_response)
    net_worth_match = re.search(net_worth_pattern, bot_response)
    criminal_background_match = re.search(criminal_background_pattern, bot_response)

    # Initialize variables with default values
    name = name_match.group(1).strip() if name_match else None
    residency = residency_match.group(1).strip() if residency_match else None
    net_worth = net_worth_match.group(1).strip() if net_worth_match else None
    net_worth = re.sub(r'\(as of [A-Za-z]+\s\d{4}\)', '', net_worth)
    criminal_background = criminal_background_match.group(1).strip() if criminal_background_match else None

    # # Print the extracted values for debugging
    print("Name:", name)
    print("Residency:", residency)
    print("Net Worth:", net_worth)
    print("Criminal Background:", criminal_background)


    # HTML form with the fetched data
    form_html = f"""
    <form method="POST" action="/check_eligibility">
        <input type="hidden" name="investorName" value="{investor_name}">
        <label for="clientName">Client Name:</label>
        <input type="text" id="clientName" name="clientName" value="{name}" required><br><br>
        <label for="residency">Residency:</label>
        <input type="text" id="residency" name="residency" value="{residency}" required><br><br>
        <label for="netWorth">Net Worth (in millions USD):</label>
        <input type="text" id="netWorth" name="netWorth" value="{net_worth}" required><br><br>
        <label for="restrictedCountries">Restricted Countries:</label>
        <select id="restrictedCountries" name="restrictedCountries">
            <option value="None">None</option>
            <option value="Pakistan">Pakistan</option>
            <option value="Syria">Syria</option>
            <option value="Cuba">Pakistan</option>
            <option value="Iran">Syria</option>
            <option value="Afghanistan">Pakistan</option>
            <option value="Bangladesh">Syria</option>
            <option value="North Korea">Pakistan</option>
            <option value="Sudan">Syria</option>
            <option value="Crimea">Syria</option>
            <option value="Zimbabwe">Pakistan</option>
            <option value="Venezuela">Syria</option>
        </select>
        <label for="criminalBackground">Do you have a criminal background?</label>
        <input type="text" id="criminalBackground" name="criminalBackground" value="{criminal_background}" required><br><br>
        <input type="submit" value="Check Eligibility" style="background-color: #FF5733; color: #FFFFFF;">

    </form>
    """
    return form_html

# Define the Gradio interface
gr.Interface(fn=investor_form, inputs="textbox", outputs="html", live=True, title="Investor Eligibility Chatbot", description="Enter the investor's name to check eligibility.").launch()

# # Define the Flask routes
# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/check_eligibility', methods=['POST'])
def check_eligibility():
    investor_name = request.form['investorName']
    client_name = request.form['clientName']
    residency = request.form['residency']
    net_worth = float(request.form['netWorth'])
    criminal_background = request.form['criminalBackground']
    restricted_countries = request.form['restrictedCountries']

    # eligibility check logic
    if net_worth >= 30000000 and restricted_countries not in ['Syria', 'Pakistan', 'Cuba', 'Iran', 'Afghanistan', 'Bangladesh', 'North Korea', 'Sudan', 'Crimea', 'Zimbabwe', 'Venezuela'] and criminal_background == 'No':
        eligibility = "Eligible for investing"
    else:
        eligibility = "Not eligible for investing"

    return render_template('result.html', investor_name=investor_name, client_name=client_name, residency=residency, net_worth=net_worth, criminal_background=criminal_background, restricted_countries=restricted_countries, eligibility=eligibility)

if __name__ == '__main__':
    app.run(share=True)
