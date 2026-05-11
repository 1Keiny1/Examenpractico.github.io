from flask import Flask, render_template
import pandas as pd
import matplotlib
import os

matplotlib.use("Agg")

import matplotlib.pyplot as plt

app = Flask(__name__, template_folder="front")


@app.route("/")
def inicio():
    datos = pd.read_csv("data/datos.csv", na_values=["NA"])

    columnas = datos.columns.tolist()
    registros = datos.head(10).to_dict(orient="records")

    variables_numericas = ["peso", "altura", "velocidad"]

    estadisticas = {}

    for variable in variables_numericas:
        serie = datos[variable].dropna()

        estadisticas[variable] = {
            "media": round(serie.mean(), 2),
            "mediana": round(serie.median(), 2),
            "moda": round(serie.mode().iloc[0], 2)
        }

    frecuencia_absoluta = datos["color"].value_counts(dropna=False).sort_index()
    frecuencia_relativa = frecuencia_absoluta / frecuencia_absoluta.sum()
    frecuencia_acumulada = frecuencia_absoluta.cumsum()

    tabla_frecuencias = []

    for categoria in frecuencia_absoluta.index:
        nombre = "NA" if pd.isna(categoria) else str(categoria)

        tabla_frecuencias.append({
            "categoria": nombre,
            "frecuencia_absoluta": int(frecuencia_absoluta[categoria]),
            "frecuencia_relativa": round(float(frecuencia_relativa[categoria]) * 100, 2),
            "frecuencia_acumulada": int(frecuencia_acumulada[categoria])
        })

    categorias = ["NA" if pd.isna(c) else str(c) for c in frecuencia_absoluta.index]
    valores = frecuencia_absoluta.values

    os.makedirs("static/graficas", exist_ok=True)

    plt.figure(figsize=(8, 4))
    plt.bar(categorias, valores)
    plt.title("Frecuencia Absoluta de Colores")
    plt.xlabel("Color")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.savefig("static/graficas/barras.png")
    plt.close()

    plt.figure(figsize=(6, 6))
    plt.pie(
        valores,
        labels=categorias,
        autopct="%1.1f%%"
    )
    plt.title("Frecuencia Relativa de Colores")
    plt.tight_layout()
    plt.savefig("static/graficas/pastel.png")
    plt.close()

    plt.figure(figsize=(8, 4))
    plt.plot(categorias, valores, marker="o")
    plt.title("Polígono de Frecuencias")
    plt.xlabel("Color")
    plt.ylabel("Frecuencia")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("static/graficas/poligono.png")
    plt.close()

    return render_template(
        "index.html",
        columnas=columnas,
        registros=registros,
        estadisticas=estadisticas,
        tabla_frecuencias=tabla_frecuencias
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)