import sys
import os

# ضيف المجلد اللي فوق api عشان يشوف app.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app 
application = app
