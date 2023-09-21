from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

openai.api_key = ""
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    prompt = request.form['prompt']

    # Call the OpenAI API with the prompt
    response = openai.Completion.create(
        engine="",
        prompt=prompt,
        max_tokens=150  
    )

    # Extract and return the OpenAI response
    reply = response.choices[0].text.strip()
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)