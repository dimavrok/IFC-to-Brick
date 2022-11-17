#%% Import packages
import pyshacl
from rdflib import Graph

# Parse the data graph and the shapes graph
data_graph = Graph()
data_graph.parse("output.ttl", format="ttl")

shapes = Graph()
shapes.parse("shapes.ttl", format="ttl")

#%% Validate and Print Results

results = pyshacl.validate(
    data_graph,
    shacl_graph=shapes,
    data_graph_format="ttl",
    shacl_graph_format="ttl",
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

report_g.serialize(destination="Validation_Report.ttl", format="turtle")

# %%
