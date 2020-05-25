from flask import Flask, render_template, request, jsonify, json, make_response
from io import BytesIO
import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import csv
import definition

app = Flask(__name__)

@app.route('/')
def index():
    return "hello world!"

if __name__ == "__main__":
    app.run(debug=True)