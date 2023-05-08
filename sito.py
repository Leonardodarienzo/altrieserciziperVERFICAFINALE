from flask import Flask, render_template, request
app = Flask(__name__)

import pandas as pd
import geopandas as gpd
import contextily as ctx
import os
import matplotlib.pyplot as plt

comuni = gpd.read_file("Comuni/Com01012022_g_WGS84.dbf")
province = gpd.read_file("Province/ProvCM01012022_g_WGS84.dbf")


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/es1', methods = ["GET"])
def es1():
    global nome
    nome = request.args.get("provincia")
    provincia_selezionata = province[province["DEN_UTS"] == nome.capitalize()].to_crs(3857)
    ax = provincia_selezionata.plot(figsize = (12, 8), edgecolor = "k", facecolor = "none", linewidth = 2)
    ctx.add_basemap(ax)

    dir = "static/images"
    file_name = "graf1.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template('grafico1.html')

@app.route('/es2')
def es2():
    provincia_selezionata = province[province["DEN_UTS"] == nome.capitalize()].to_crs(3857)
    comuni_provincia_selezionata = comuni.to_crs(3857)[comuni.to_crs(3857).within(provincia_selezionata.geometry.item())].to_html()
    return render_template('tabella.html', tabella = comuni_provincia_selezionata)

@app.route('/es3')
def es3():
    provincia_selezionata = province[province["DEN_UTS"] == nome.capitalize()].to_crs(3857)
    comuni_provincia_selezionata = comuni.to_crs(3857)[comuni.to_crs(3857).within(provincia_selezionata.geometry.item())]
    df3 = comuni_provincia_selezionata.sort_values(by="COMUNE")[["COMUNE", "Shape_Area"]].to_html()
    return render_template('tabella.html', tabella = df3)

@app.route('/es4')
def es4():
    provincia_selezionata = province[province["DEN_UTS"] == nome.capitalize()].to_crs(3857)
    comuni_provincia_selezionata = comuni.to_crs(3857)[comuni.to_crs(3857).within(provincia_selezionata.geometry.item())]
    dizionario = dict(zip(comuni_provincia_selezionata["COMUNE"], comuni_provincia_selezionata["Shape_Area"]))
    return render_template('tabella.html', tabella = dizionario)

@app.route('/es5')
def es5():
    def conversione(kmq):
        return kmq * 0.386102
    valore5 = conversione(37)
    return render_template('tabella.html', tabella = valore5)

@app.route('/es6')
def es6():
    def conversione(kmq):
        return kmq * 0.386102
    provincia_selezionata = province[province["DEN_UTS"] == nome.capitalize()].to_crs(3857)
    comuni_provincia_selezionata = comuni.to_crs(3857)[comuni.to_crs(3857).within(provincia_selezionata.geometry.item())]
    comuni_provincia_selezionata["superficieInMigliaQuadrate"] = conversione(comuni_provincia_selezionata["Shape_Area"])
    df6 = comuni_provincia_selezionata.to_html()
    return render_template('tabella.html', tabella = df6)

@app.route('/es7')
def es7():
    provincia_selezionata = province[province["DEN_UTS"] == nome.capitalize()].to_crs(3857)
    comuni_confinanti_provinciaSelezionata = comuni.to_crs(3857)[comuni.to_crs(3857).touches(provincia_selezionata.geometry.item())].to_html()
    return render_template('tabella.html', tabella = comuni_confinanti_provinciaSelezionata)

@app.route('/es8')
def es8():
    def conversione(kmq):
        return kmq * 0.386102
    provincia_selezionata = province[province["DEN_UTS"] == nome.capitalize()].to_crs(3857)
    comuni_confinanti_provinciaSelezionata = comuni.to_crs(3857)[comuni.to_crs(3857).touches(provincia_selezionata.geometry.item())]
    comuni_confinanti_provinciaSelezionata["superficieInMigliaQuadrate"] = conversione(comuni_confinanti_provinciaSelezionata["Shape_Area"])
    valore8 = int(comuni_confinanti_provinciaSelezionata["superficieInMigliaQuadrate"].sum())
    return render_template('tabella.html', tabella = valore8)

@app.route('/es9')
def es9():
    provincia_selezionata = province[province["DEN_UTS"] == nome.capitalize()].to_crs(3857)
    comuni_confinanti_provinciaSelezionata = comuni.to_crs(3857)[comuni.to_crs(3857).touches(provincia_selezionata.geometry.item())]
    comune_confinate_maxEsteso = comuni_confinanti_provinciaSelezionata[comuni_confinanti_provinciaSelezionata["Shape_Area"] == comuni_confinanti_provinciaSelezionata["Shape_Area"].max()].to_html()
    return render_template('tabella.html', tabella = comune_confinate_maxEsteso)

@app.route('/es10')
def es10():
    provincia_selezionata = province[province["DEN_UTS"] == nome.capitalize()].to_crs(3857)
    d = int(provincia_selezionata.geometry.item().distance(province[province["DEN_UTS"] == "Milano"].to_crs(3857).geometry.item()))
    return render_template('tabella.html', tabella = d)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)