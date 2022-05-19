#%% Import packages
import rdflib
import pyshacl
from pyshacl import validate
from rdflib import Graph

#%% Parse the data graph and the shapes graph
graph = Graph()
graph.parse('Data_Graph.ttl', format='ttl')

shapes = Graph()
shapes.parse('Data_Shapes.ttl', format='ttl')


#%% Validate and Print Results
# HERE WE CHECK WHETHER THE RELATIONSHIP SYSTEM-ZONE CONFORMS WITH A REUSABLE STRUCTURE

import pyshacl

results = pyshacl.validate(
    data_graph=graph,
    shacl_graph=shapes,
    data_graph_format="ttl",
    shacl_graph_format="ttl",
    inference="rdfs",
    debug=True,
    serialize_report_graph="ttl",
    )

conforms, report_graph, report_text = results

print("conforms", conforms)

print(report_text)
# %%

report_g = Graph()
report_g.parse(data=report_graph, format="ttl", encoding="utf-8")
nm = report_g.namespace_manager

for s, p, o in sorted(report_g):
    print(s.n3(nm), p.n3(nm), o.n3(nm))
