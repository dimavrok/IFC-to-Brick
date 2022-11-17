#%% 
import brickschema # 

g = brickschema.Graph(load_brick=True)

g.load_file("Inputs.ttl") #add your ttl here
g.expand(profile="owlrl")
print(f"Inferred graph has {len(g)} triples")

# %%
g.serialize("Output.ttl") #export the enriched ttl here

# %%
