# Flask creates classes, or website object instances
from flask import Flask, render_template
import pandas as pd

# Website object
# __name__ is a special variable. returns "__{py file name}__" or
# Other file name imported/referenced
app = Flask(__name__)
stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]

# Connect HTML elements to app. use function to render the HTML docs whenever someone
# Accesses our {websiteurl}/home
# Need to have a default "templates" folder, will automatically look for that
# Throw images under a "static folder", make sure the path in HTML file is correct
# can return data to home.html page by declaring variables in return (data=variable)
@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())

# Example of how to ad more pages
# Use tags within this flask String to pass variables
@app.route("/api/v1/<station>/<date>")
def about(station, date):
    # zfill() string method lets you add 0s to string
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    # data in txt files actual starts at row 21 hence skiprows
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    #return render_template("about.html")
    return {"station": station,
            "date": date,
            "temperature": temperature}

# Function/route for user to enter only station and return all info
@app.route("/api/v1/<station>")
def all_data(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    result = df.to_dict(orient="records")
    return result

@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    return result

# See errors on webpage for debugging
# Only run flask app when main.py executed
# Can import main in other py files so we only run certain
# functions when certain pages are accessed
# Can define specific ports if running multiple "apps"
if __name__ == "__main__":
    app.run(debug=True, port=5001)