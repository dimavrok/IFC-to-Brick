#%% import graphs

"""Why I am using SHACL rules: It is more powerful that SPARQL Construct because
we can specify a shape in the graph and then enrich only this shape. 
So, perhaps, SPARQL Construct rules would work but we would need multiple SPARQL(?) """

import pyshacl
from rdflib import Graph

g = Graph()
g.parse("Data_Graph.ttl")




# %% Export the graph
g.serialize(destination="Data_Graph_INFERRED.ttl", format="turtle")

