import csv
import random 
import networkx as nx
from models import Node, HealthState
from simulation import initialize_simulation, run_simulation , add_edges
g=nx.Graph()
nodes=[]
output_file_path= "dataset.csv"
def generate_graph():
    g,nodes = initialize_simulation()
    add_edges()
    run_simulation()
    return g, nodes

def save_to_csv(nodes , output_file_path):
    with open(output_file_path , 'w' , newline='') as csvfile:
        csv_writer=csv.writer(csvfile)
        csv_writer.writerow(['Node ID' , 'Health' , 'Positon_X','Postion_Y' , ])
