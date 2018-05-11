import flask
import graph_operations

def create_app():
    app = flask.Flask(__name__)
    return app

app = create_app()

@app.route('/my-endpoint', methods=['GET'])
def get_corpus():
    return flask.jsonify({'foo': 42})

@app.route('/tree', methods=['GET'])
def get_tree_by_root():
    root = flask.request.args.get('root')
    return flask.jsonify(graph_operations.get_tree_by_root(root))

@app.route('/delete_some_node', methods=['POST'])
def delete_some_node():
    graph_operations.delete_node('fox');
    return ('', 204);


@app.route('/clear_all_nodes', methods=['POST'])
def clear_all_nodes():
    graph_operations.clear_entire_graph()
    return ('', 204);


@app.route('/all_roots', methods=['GET'])
def get_all_roots():
    return flask.jsonify(graph_operations.get_all_roots())

