from flask import Flask, render_template, request, jsonify, session, redirect, Markup
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')

API_KEY = os.environ.get('TMDB_API_KEY') # عشان انت سميته كده في Vercel
