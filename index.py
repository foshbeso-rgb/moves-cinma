from flask import Flask, render_template, request, jsonify, session, redirect, send_from_directory, Markup
import os
import requests
import config
import tmdb
import sections as s

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'dakhlin_secret_key_123'

BASE_URL = "https://api.themoviedb.org/3"
API_KEY = os.environ.get('API_KEY')

# حط هنا كل الـ routes بتاعتك كلها من اول @app.route("/") لحد اخر واحد
# انسخ كل الكود اللي في app.py بتاعك هنا

# وفي الاخر امسح app.run خالص
app = app