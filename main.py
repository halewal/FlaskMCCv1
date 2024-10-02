import matplotlib

matplotlib.use('Agg')
from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

menu_data = pd.read_csv("menu.csv")


@app.route('/')
@app.route('/')
def index():
    query = request.args.get("query")
    category = request.args.get("category")

    filtered_data = menu_data

    if query:
        filtered_data = filtered_data[
            filtered_data["Item"].str.contains(query, case=False)
        ]

    if category and category != 'all':
        filtered_data = filtered_data[
            filtered_data["Category"].str.contains(category, case=False)
        ]

    return render_template(
        "index.html",
        pokemon=filtered_data.to_dict(orient="records"),
        categories=menu_data["Category"].unique()  # Pass unique categories to the template
    )


@app.route('/pokemon/<name>')
def pokemon_details(name):
    pokemon = menu_data[menu_data["Item"] == name].iloc[0]
    stats = ["Category", "Calories"]
    values = [pokemon[stat] for stat in stats]

    plt.figure(figsize=(6, 4))
    plt.bar(stats, values, color='blue')
    plt.title(f"Stats for {pokemon['Item']}")

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template(
        "details.html",
        pokemon=pokemon,
        plot_url=plot_url
    )


if __name__ == "__main__":
    app.run(debug=True)
