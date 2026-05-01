import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))
import database
import pdf_generator

cv = database.get_cv(1)
try:
    html = pdf_generator.get_web_html(cv)
    print("SUCCESS")
except Exception as e:
    import traceback
    traceback.print_exc()
