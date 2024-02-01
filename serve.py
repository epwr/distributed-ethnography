#!/usr/bin/env python3

from app import app, settings

if __name__ == "__main__":
    app.run(host='localhost', port=4000)
