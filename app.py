from flask import Flask, render_template, make_response
import pandas as pd
import io
import numpy as np

from helper import get_recipes_and_ingredients


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/download_recipes')
def download_recipes():
    #Create DF
    recipes = get_recipes_and_ingredients()
    df = pd.DataFrame(np.array(recipes), columns=['recipe name', 'ingredient', 'quanitity'])
    
    # Creating output and writer (pandas excel writer)
    out = io.BytesIO()
    writer = pd.ExcelWriter(out, engine='xlsxwriter')

    # Export data frame to excel
    df.to_excel(excel_writer=writer, index=False, sheet_name='Sheet1')
    writer.close()

    # Flask create response 
    r = make_response(out.getvalue())

    # Defining correct excel headers
    r.headers["Content-Disposition"] = "attachment; filename=stardew-scrape.xlsx"
    r.headers["Content-type"] = "application/x-xls"

    # Finally return response
    return r