from flask import Flask, jsonify, request
import matplotlib.pyplot as plt
import pandas as pd
import json
from get_all_data import get_json

GRAPH_DIR = "./graphs/"
app = Flask(__name__)

# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username

@app.route('/', methods=['GET', 'POST'])
def return_all_json():
    start_date = request.args.get('2018-10-10')
    stop_date = request.args.get('2018-10-17')
    json_str = get_json(start_date, stop_date)

    return json_str


@app.route('/graph')
def get_graph_and_metadata():
    json_str = str(request.args.get('json_obj'))
    graph_name = request.args.get('graph_name')
    df = pd.DataFrame(json.loads(json_str)).reset_index().set_index('index').T
    df.to_csv(GRAPH_DIR + 'example.csv')
    ax = plt.gca()
    df.plot(kind='line', x='index', y='steps', ax=ax)
    plt.savefig(GRAPH_DIR + graph_name + '.png', bbox_inches = 'tight')






# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.run(debug=True)