from flask import Flask, request, render_template
from agents import check_hiking_conditions
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        city = request.form['city']
        result = check_hiking_conditions(city)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
