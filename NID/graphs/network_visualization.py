from datetime import datetime
from pathlib import Path
import argparse
import igraph as ig
import numpy as np
import pandas as pd
import random
import subprocess

HELP_ADDRESS = "first three numbers of home network address space connected by dots (default = 192.168.0)"
HELP_CSV = "table in csv-format containing sender-ip, receiver-ip, number of packets (assumes a header exists)"
HELP_TCPDUMP = "tcpdump capture file"

file_path = ""
address_space = ""


def get_available_edges(num_vertices):
    return {frozenset([e1, e2]) for e1 in range(0,num_vertices) for e2 in range(0, num_vertices) if e1 < e2}


def random_network(num_vertices, num_edges):
    g = ig.Graph(n=num_vertices)
    g.vs["name"] = ["192.168.0."+str(i) if i > 0 else "Extern" for i in list(range(0, num_vertices))]
    available_edges = get_available_edges(num_vertices)
    if num_edges > len(available_edges):
        raise RuntimeError("Number of edges exceeds maximum number of edges for this graph.")
    g.add_edges([[x,y] for x,y in random.sample(population=available_edges, k=num_edges)])
    count = list(range(1, num_edges+1))
    random.shuffle(count)
    g.es["count"] = count
    return g


def transform_csv():
    df = pd.read_csv(file_path)
    if len(df.columns) >= 3:
        d = {tuple(r.values())[:2]:list(r.values())[2] for r in df.to_dict('records')}
        return create_graph(d)
    else:
        print("Data could not be transformed. Requires three columns (sender-ip, receiver-ip, number of packets).")
        exit(1)

def transform_ip(input):
    first, second = input
    if address_space + "." not in first:
        first = "Extern"
    if address_space + "." not in second:
        second = "Extern"
    return remove_port(first), remove_port(second)


def remove_port(ip):
    s = ip.split(".")
    return ".".join(s[:4]) if len(s) > 4 else ip


def transform_tcpdump():
    d = {}
    x = subprocess.Popen(f"tcpdump -r {file_path} | cut -d \" \" -f3,5 | cut -d: -f1", shell=True,
                         stdout=subprocess.PIPE)
    for l in x.stdout:
        line = l.decode('utf-8')
        key = tuple(line.strip().split(' '))
        if len(key) > 1:
            key = transform_ip(key)
            d.setdefault(key, 0)
            d[key] = d[key] + 1
    return create_graph(d)


def create_graph(d):
    vertex_set = set([item for sublist in d.keys() for item in sublist])
    vertex_list = list(vertex_set)
    edge_set_dictionary = {}
    for item in [(key[0], key[1], value) for key, value in d.items()]:
        key = frozenset([item[0], item[1]])
        value = item[2]
        if len(key) > 1:
            edge_set_dictionary.setdefault(key, 0)
            edge_set_dictionary[key] = edge_set_dictionary[key] + value
    edges = list(edge_set_dictionary)
    count = [edge_set_dictionary.get(edge) for edge in edges]

    g = ig.Graph(n=len(vertex_list))
    g.vs["name"] = vertex_list
    g.add_edges([[x, y] for x, y in edges])
    g.es["count"] = count
    return g


def scale_edges(input):
    count = input.copy()
    for x, y in enumerate(np.array(count).argsort()):
        count[y] = (x + 1)
    max_value = len(count)
    if max_value <= 10:
        return count
    factor = 10/max_value
    return [round((x + 1) * factor) for x in count]


def plot_network(graph, output_path=None):
    visual_style = dict()
    visual_style["edge_color"] = "silver"
    visual_style["vertex_color"] = ["deepskyblue" if x == "Extern" else "aquamarine" for x in graph.vs["name"]]
    visual_style["vertex_label_size"] = 20
    visual_style["vertex_size"] = 60
    visual_style["vertex_label"] = graph.vs["name"]
    visual_style["edge_width"] = scale_edges(graph.es["count"])
    visual_style["layout"] = graph.layout("kk")
    visual_style["bbox"] = (800, 800)
    visual_style["margin"] = 70
    if output_path:
        return ig.plot(graph, output_path, **visual_style)
    return ig.plot(graph, target=None, **visual_style)


def main(is_csv):
    g = transform_csv() if is_csv else transform_tcpdump()
    if g:
        plot_network(g)
    else:
        print("Data could not be transformed to a network graph.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--csv", action="store_true", help=HELP_CSV)
    group.add_argument("-t", "--tcpdump", action="store_true", help=HELP_TCPDUMP)
    parser.add_argument("file_path", type=Path, help="path of file containing data")
    parser.add_argument("-a", "--address_space", type=str, default="192.168.0", help=HELP_ADDRESS)

    p = parser.parse_args()

    if p.file_path.exists():
        file_path = str(p.file_path)
        print(f"Reading from: {file_path}")
        address_space = p.address_space
        timestamp = datetime.now().strftime('%Y-%m-%dT%H%M%S')
        output_path = f"network_{timestamp}.png"
        main(p.csv)
        print(f"Visualization complete! See file: {output_path}")
    else:
        print("No data provided! Please refer to help:\n")
        parser.print_help()