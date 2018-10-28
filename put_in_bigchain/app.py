from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)

@app.route('/put_in', methods=['GET', 'POST'])
def put_in_blockstack():
    url = 'https://jasonjconci.localtunnel.me/'
    req = requests.get(url)
    content = str(req.content)
    #ref = request.headers.get('oref')
    url2 = "http://10.177.0.17:9191/storage"
    payload = {"content": "nothing"}
    headers = {"accept": "application/json", "Originator-Ref":"jason", "Content-Type": "application/json"}
    response = requests.post(url, data=payload, headers=headers)
    return "<p1>jason</pa>"

@app.route('/get_from', methods=['GET', 'POST'])
def get_from_blockstack():
    ref = request.headers.get('oref')
    payload = {}
    headers = {"accept":"application/json", "Originator-Ref":ref}
    url2 = "http://10.177.0.17:9191/storage"
    response = requests.get(url, data=payload, headers=headers)
    return response.text

if __name__ == "__main__":
    app.run(debug=True)
