from flask import Flask, request, render_template, redirect, url_for
import requests

app = Flask(__name__)

def process(result_text):
    parts = result_text.split(':')
    if len(parts) == 1:
        final=[]
        return final
    part = parts[1]
    print(part)
    if part.count('\n') >= 3:
        final = part.split('\n')
        # Using list comprehension to apply changes to all items in list:
        print(final)
        final = final[2:]
        for i in range(len(final)):
            final[i] = final[i][2:]

        print(final)
    else:
        final = part.split(',')
        final = [item.strip().capitalize() for item in final]  # Apply strip and capitalize to all items
        print(final)
    return final


@app.route('/')
def start():
    return render_template('start.html')



@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form['user_input']
        return redirect(url_for('answer', prompt=user_input))
    return render_template('home.html')

@app.route('/process_answer', methods=['POST'])
def process_answer():
    response_text = request.form['response']  # This gets the value of the clicked button
    prompt = "Generate 4 words related to " + response_text + ", separated with commas"
    data = {
        "prompt": prompt,
        "max_tokens": 50,
        "temperature": 0.5
    }
    headers = {"Content-Type": "application/json"}
    try:
        api_response = requests.post("http://localhost:1234/v1/completions", json=data, headers=headers)
        if api_response.status_code == 200:
            response_data = api_response.json()
            if response_data.get('choices'):
                result_text = response_data['choices'][0]['text'].strip()
                final = process(result_text)
                print(final)
                return render_template('answer.html', result0=final[0] if len(final) > 0 else "model error",
                       result1=final[1] if len(final) > 1 else "model error",
                       result2=final[2] if len(final) > 2 else "model error",
                       result3=final[3] if len(final) > 3 else "model error",res=response_text)
            else:
                error_message = "No results found."
                return render_template('answer.html', error=error_message, res=response_text)
        else:
            return render_template('answer.html', error="Failed to fetch response from the model", res=response_text)
    except requests.exceptions.RequestException as e:
        return render_template('answer.html', error=str(e), res=response_text)


@app.route('/answer')
def answer():
    prompt = request.args.get('prompt', default='', type=str)
    if prompt:
        url = "http://localhost:1234/v1/completions"
        headers = {"Content-Type": "application/json"}
        data = {
            "prompt": "Generate 4 words related to " + prompt + ", separated with commas",
            "max_tokens": 50,
            "temperature": 0.5
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('choices'):
                result_text = response_data['choices'][0]['text'].strip()
                final = process(result_text)
                return render_template('answer.html', result0=final[0], result1=final[1], result2=final[2], result3=final[3], res=prompt)
            else:
                error_message = "No result was found in the response."
                return render_template('answer.html', result={"error": error_message})
        else:
            error_message = "Failed to fetch response from the model"
            return render_template('answer.html', result={"error": error_message})
    else:
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
