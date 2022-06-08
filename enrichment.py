# %% Import files and packages
import rdflib
import json
from rdflib import Graph

g = Graph()
g.parse("Data_Graph.ttl")


# dictionary for storing the datapoint ids (Building Management System)
P = {'lights':[], 'spaces':[]}

# dictionary for storing the output 
R = {}
#input

# %% Query the graph to get the 3D vectors for lights and spaces
qres = g.query("""
    PREFIX owl: <http://www.w3.org/2002/07/owl#> 
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    PREFIX bot: <https://w3id.org/bot#> 
    PREFIX brick: <https://brickschema.org/schema/Brick#> 
    PREFIX om: <http://openmetrics.eu/openmetrics#> 
    SELECT DISTINCT ?li ?bbli ?sp ?bbsp WHERE {
        ?li a brick:Lighting . 
        ?sp a brick:Space .
        ?li bot:hasSimple3DModel ?bbli .
        ?sp bot:hasSimple3DModel ?bbsp .
        }""")


# %% Store results of the query in a dictionary
for r in qres:
	P["lights"].append({str(r.li.toPython()):r.bbli.toPython()})

for r in qres:
    P["spaces"].append({str(r.sp.toPython()):r.bbsp.toPython()})

# %% Make the comparison

for i in range(0,len(P["lights"])):    
    for j in P["lights"][i]:
        #print(P["lights"][i][str(j)])
        json.loads(P["lights"][i][str(j)])["bbox"]

    
R = json.loads(P["bb_lights"][0]["inst_bbli"])

# %% Store results into dictionary
for row in qres:
    res_bbli = json.loads(f"{row.bbli}")
    res_bbsp = json.loads(f"{row.bbsp}")
    res_sp = json.loads(f"{row.sp}")
    res_li = json.loads(f"{row.li}")


# %% 

