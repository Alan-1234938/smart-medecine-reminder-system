from flask import Flask, render_template, request, redirect
import csv
import datetime
import os

app = Flask(__name__)
FILENAME = "medication.csv"

# Ensure the CSV file exists
if not os.path.exists(FILENAME):
    with open(FILENAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Dosage", "Frequency", "Schedule Times", "Days", "Start Date"])

def read_data():
    with open(FILENAME, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        return list(reader)

def write_data(data):
    with open(FILENAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Dosage", "Frequency", "Schedule Times", "Days", "Start Date"])
        writer.writerows(data)

@app.route("/")
def index():
    medications = read_data()
    medications.sort(key=lambda x: x[3]) # sort by time
    return render_template("index.html", medications=medications)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    dosage = request.form["dosage"]
    freq = request.form["frequency"]
    times = request.form["times"]
    days = request.form["days"]
    today = datetime.date.today().isoformat()

    with open(FILENAME, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, dosage, freq, times, days, today])
    
    return redirect("/")

@app.route("/edit/<int:index>")
def edit(index):
    data = read_data()
    if index < len(data):
        return render_template("edit.html", index=index, med=data[index])
    return redirect("/")

@app.route("/update/<int:index>", methods=["POST"])
def update(index):
    data = read_data()
    if index < len(data):
        name = request.form["name"]
        dosage = request.form["dosage"]
        freq = request.form["frequency"]
        times = request.form["times"]
        days = request.form["days"]
        start = data[index][5] # preserve original start date
        data[index] = [name, dosage, freq, times, days, start]
        write_data(data)
    return redirect("/")

@app.route("/delete/<int:index>")
def delete(index):
    data = read_data()
    if 0 <= index < len(data):
        del data[index]
        write_data(data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
import os

port = int(os.environ.get("PORT",5000))
app.run(host="0.0.0.0", port=port)    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port)
