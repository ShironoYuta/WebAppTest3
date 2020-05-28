from flask import Flask, render_template, request, jsonify, json, make_response
import definition
app = Flask(__name__)

@app.route('/')
def index():
    return "hello world!"

if __name__ == "__main__":
    app.run(debug=True)