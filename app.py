#!/usr/bin/env python3
"""Ponto de entrada.  pip install -r requirements.txt  ->  python app.py  ->  http://localhost:5000"""
from egipcias import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
