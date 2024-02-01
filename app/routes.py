from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def get_index_page():
    return render_template('index.html')


@app.route('/test')
def get_test_values():
    return "test return value"
