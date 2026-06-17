from flask import Flask,render_template
import json

app = Flask(__name__)

@app.route("/")

def dashboard():
    with open("sample_scan_results.json","r") as file:
        devices = json.load(file)

    total_ports = sum(
        len(device["open_ports"])
        for device in devices
    )

    return render_template(
        "index.html",
        devices=devices,
        total_ports = total_ports
    )
    

if __name__ == "__main__":
    app.run(debug=True)