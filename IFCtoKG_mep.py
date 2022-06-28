#%% Import packages
import os, sys
import ifcopenshell
import json
import pandas as pd
from rdflib.namespace import NamespaceManager
from rdflib import Graph, RDF, URIRef, Literal

#%% Create a namespace
NS_om = "http://openmetrics.eu/openmetrics#"
NS_bot = "https://w3id.org/bot#"
NS_beo = "https://pi.pauwel.be/voc/buildingelement#"
NS_brick = "https://brickschema.org/schema/Brick#"
NS_rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
NS_rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
NS_owl = "http://www.w3.org/2002/07/owl#"
NS_schema = "http://schema.org#"
NS_mep = "https://pi.pauwel.be/voc/distributioncomponent#"
NS_fso = "http://www.w3id.org/fso#"
NS_props = "https://w3id.org/props#"


graph = Graph()
graph.namespace_manager.bind("om", URIRef(NS_om))
graph.namespace_manager.bind("bot", URIRef(NS_bot))
graph.namespace_manager.bind("beo", URIRef(NS_beo))
graph.namespace_manager.bind("brick", URIRef(NS_brick))
graph.namespace_manager.bind("rdf", URIRef(NS_rdf))
graph.namespace_manager.bind("owl", URIRef(NS_owl))
graph.namespace_manager.bind("schema", URIRef(NS_schema))
graph.namespace_manager.bind("mep", URIRef(NS_mep))
graph.namespace_manager.bind("fso", URIRef(NS_fso))
graph.namespace_manager.bind("props", URIRef(NS_props))


#%% Import IFC file
f = ifcopenshell.open("Basement_East_Plantroom.ifc")

props_guid = URIRef(NS_props + "hasGuid")

#%% Converter 

#####################################################################################
###############     TRANSFORM and LOAD product instances      #######################
#####################################################################################
 

with open('mapping_table.json') as m:
        map = json.load(m)


for element in map:
        components = f.by_type(element)
        if not components:
                print (element + " not found")
        else:
                for component in components:
                        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
                        graph.add((inst, props_guid, Literal(component.GlobalId)))                        
                        if map[component.__dict__["type"]]["bot"] != "":
                                bot = URIRef(NS_bot + map[component.__dict__["type"]]["bot"])
                                graph.add((inst, RDF.type, bot))
                        if map[component.__dict__["type"]]["beo"] != "":
                               beo = URIRef(NS_beo + map[component.__dict__["type"]]["beo"])
                               graph.add((inst, RDF.type, beo))
                        if map[component.__dict__["type"]]["mep"] != "":
                                mep = URIRef(NS_mep + map[component.__dict__["type"]]["mep"])
                                graph.add((inst, RDF.type, mep))
                        if map[component.__dict__["type"]]["fso"] != "":
                                fso = URIRef(NS_fso + map[component.__dict__["type"]]["fso"])
                                graph.add((inst, RDF.type, fso))                              
                        if map[component.__dict__["type"]]["brick"] != "":
                                brick = URIRef(NS_brick + map[component.__dict__["type"]]["brick"])
                                graph.add((inst, RDF.type, brick))
                                                            

#########################################################################################
############################     Create Relationships      ##############################
#########################################################################################

# 1. Distribution component Ports for connecivity of components (using  BOT, FSO)

connections = f.by_type("IFCRELCONNECTSPORTS")

connectedWith = URIRef(NS_fso + "connectedWith")
for connection in connections:
        component_1 = connection.RelatedPort.Nests[0].RelatingObject
        inst_1 = URIRef(NS_om + "inst_" + component_1.GlobalId.replace("$","_"))
        component_2 = connection.RelatingPort.Nests[0].RelatingObject              
        inst_2 = URIRef(NS_om + "inst_" + component_2.GlobalId.replace("$","_"))
        graph.add((inst_1, connectedWith, inst_2))    


# 2. Systems from grouped elements - IfcSystems need to be generated from enrichment processes

systems = f.by_type("IfcSystem")
distributionsystem = URIRef(NS_fso + "DistributionSystem")
#hasConsumerComponent = URIRef(NS_fso + "hasComponent")
#hasSourceComponent = URIRef(NS_fso + "hasComponent")
hascomponent = URIRef(NS_fso + "hasComponent")
hasName = URIRef(NS_props + "hasName")
for system in systems:
        inst_system = URIRef(NS_om + "inst_" + system.GlobalId.replace("$","_"))
        inst_system_name = Literal(str(system.ObjectType))
        graph.add((inst_system, RDF.type, distributionsystem))
        graph.add((inst_system, hasName, inst_system_name))
        # Create relationship: inst_system fso:hascomponent inst_component
        for comp in system.IsGroupedBy[0].RelatedObjects:
                if comp.__dict__["type"] != "IfcDistributionPort":
                        inst_comp = URIRef(NS_om + "inst_" + comp.GlobalId.replace("$","_"))
                        graph.add((inst_system, hascomponent, inst_comp))   


# 3. Spatial Containment of elements/components

containments = f.by_type("IFCRELCONTAINEDINSPATIALSTRUCTURE")
hasElement = URIRef(NS_bot + "hasElement")
for containment in containments: 
        if containment.RelatingStructure.__dict__["type"] == "IfcSpace":
                bot_space = URIRef(NS_bot + "Space")        
                inst_space = URIRef(NS_om + "inst_" + containment.RelatingStructure.GlobalId.replace("$","_"))
                graph.add((inst_space, RDF.type, bot_space))
                for element in containment.RelatedElements: 
                        inst_element = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
                        graph.add((inst_space, hasElement, inst_element))


#%% Export the graph
graph.serialize(destination="Data_Graph.ttl", format="turtle")

