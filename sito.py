from flask import Flask, render_template, request
app = Flask(__name__)

import pandas as pd
import geopandas as gpd
import contextily as ctx
import os

comuni = gpd.read_file("Comuni/Com01012022_g_WGS84.dbf")
province = gpd.read_file("Province/ProvCM01012022_g_WGS84.dbf")


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/es1', methods = ["GET"])
def es1():
    nome = request.args.get("provincia")
    provincia_selezionata = province[province["DEN_UTS"] == nome.capitalize()].to_crs(3857)
    ax = provincia_selezionata.plot(figsize = (12, 8), edgecolor = "k", facecolor = "none", linewidth = 2)
    ctx.add_basemap(ax)

    
    return render_template('grafico1.html')

@app.route('/es2')
def es2():
    return render_template('')

@app.route('/es3')
def es3():
    return render_template('')

@app.route('/es4')
def es4():
    return render_template('')

@app.route('/')
def home():
    return render_template('')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)