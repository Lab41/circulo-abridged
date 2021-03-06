import igraph
from igraph import VertexCover
import os
import sys
import urllib.request
from circulo.download_utils import download_with_notes, multigraph_to_weights

GRAPH_NAME = "football"
DOWNLOAD_URL = "http://www-personal.umich.edu/~mejn/netdata/football.zip"
GRAPH_TYPE = ".gml"

def __download__(data_dir):
    """
    downloads the graph from DOWNLOAD_URL into data_dir/GRAPH_NAME
    """
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    download_with_notes(DOWNLOAD_URL, GRAPH_NAME, data_dir)


def __prepare__(data_dir):
    """
    """
    pass


def get_graph():
    """
    Downloads and prepares the graph from DOWNLOAD_URL
    """
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    graph_path = os.path.join(data_dir, GRAPH_NAME + GRAPH_TYPE)

    if not os.path.exists(graph_path):
        __download__(data_dir)
        __prepare__(data_dir)

    G = igraph.load(graph_path)
    multigraph_to_weights(G)
    return G

def get_ground_truth(G=None):
    """
    Returns a VertexClustering object of the
    ground truth of the graph G. The ground truth for this
    football data is the conference to which each team belongs.
    """
    if G is None:
        G = get_graph()

    if G is None:
        print("Unable to get graph")
        sys.exit(0)

    #by default conferences are identified by a float number
    float_membership = G.vs['value']

    conf_map = {}
    for vertex_id, conference_id in enumerate(G.vs['value']):
        if conference_id not in conf_map:
            conf_map[conference_id] = []
        conf_map[conference_id].append(vertex_id)

    cluster_list = [v for k,v in conf_map.items()]

    return VertexCover(G, cluster_list)


def main():
    G = get_graph()
    get_ground_truth(G)

if __name__ == "__main__":
    main()
