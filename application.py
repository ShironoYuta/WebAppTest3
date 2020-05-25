from flask import Flask, render_template, request, jsonify, json, make_response
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import os.path
import pandas as pd
import codecs
import MyModules
import definition

app = Flask(__name__)

@app.route('/')
def index():
    return "hello world!"

if __name__ == "__main__":
    app.run(debug=True)