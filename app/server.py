#!/usr/bin/env python3

from flask import Flask, render_template

from app.config import settings

app = Flask(__name__)

@app.route('/')
def get_index_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host=settings.host, port=settings.port)
