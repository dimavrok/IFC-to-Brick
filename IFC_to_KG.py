#%% Import packages
import os, sys
import ifcopenshell
import json
import uuid
import pandas as pd
from rdflib.namespace import NamespaceManager
from rdflib import Graph, RDF, URIRef, Literal, XSD, Namespace

graph = Graph()

OM = Namespace("https://openmetrics.eu/openmetrics#")
BOT = Namespace("https://w3id.org/bot#")
#BEO = Namespace("https://pi.pauwel.be/voc/buildingelement#")
BRICK = Namespace("https://brickschema.org/schema/Brick#")
FSO = Namespace("https://www.w3id.org/fso#")
PROPS = Namespace("https://w3id.org/props#") # change that with brick value
REF = Namespace("https://w3id.org/brick/ref#")

graph.namespace_manager.bind("om", OM)
graph.namespace_manager.bind("bot", BOT)
graph.namespace_manager.bind("brick", BRICK)
graph.namespace_manager.bind("rdf", RDF)
graph.namespace_manager.bind("ref", REF)
graph.namespace_manager.bind("props", PROPS)
graph.namespace_manager.bind("xsd", XSD)
graph.namespace_manager.bind("fso", FSO)


#%% Import IFC file
print("Importing IFC...")
f = ifcopenshell.open('Basement_East_Plantroom.ifc')
props_guid = PROPS.hasGuid
props_name = PROPS.hasName

# Function that takes as input ifcopenshell.entity_instance and returns RDF instance in the om namespace
def OM_inst(component:ifcopenshell.entity_instance):
        if type(component) != ifcopenshell.entity_instance:
                return str("takes only: ") + ifcopenshell.entity_instance
        else:
                return OM.inst_ + component.GlobalId.replace("$","_")

#%% Converter 

#####################################################################################
###############     TRANSFORM and LOAD product IFC Iinstances      ##################
#####################################################################################
 
if f.wrapped_data.schema == "IFC2X3": 
        print("Version: "+"ifc2x3")
        with open('mapping_IFC2x3.json') as m:
                map = json.load(m)
elif f.wrapped_data.schema == "IFC4":
        print("Version: "+"ifc4")
        with open('mapping_IFC4.json') as m:
                map = json.load(m)    
else:
        print("Not supporting version: " + f.wrapped_data.schema)

print("Mapping IFC entities to Knowledge Graph...")

for element_type in map:
        dot_pos = element_type.find(".")
        if dot_pos > 0:
                IFC_elements = f.by_type(element_type[:dot_pos])
        else:
                IFC_elements = f.by_type(element_type)
        if IFC_elements:
                counter = 0
                for element in IFC_elements:
                        if (dot_pos==-1 and element.__dict__["type"]==element_type) or (dot_pos>0 and element.__dict__["PredefinedType"]==element_type[dot_pos+1:]):
                                graph.add((OM_inst(element), REF.IFCReference, Literal(element.GlobalId, datatype=XSD.string)))
                                if element.Description != None:
                                        graph.add((OM_inst(element), PROPS.hasDescription, Literal(element.Name + " / " + element.Description, datatype=XSD.string)))        
                                else:
                                        graph.add((OM_inst(element), PROPS.hasName, Literal(element.Name, datatype=XSD.string)))   
                                if map[element.__dict__["type"]]["bot"] != "":
                                        bot = URIRef(BOT + map[element.__dict__["type"]]["bot"])
                                        graph.add((OM_inst(element), RDF.type, bot))
                                if map[element.__dict__["type"]]["fso"] != "":
                                        fso = URIRef(FSO + map[element.__dict__["type"]]["fso"])
                                        graph.add((OM_inst(element), RDF.type, fso))                              
                                if map[element.__dict__["type"]]["brick"] != "":
                                        brick = URIRef(BRICK + map[element.__dict__["type"]]["brick"])
                                        graph.add((OM_inst(element), RDF.type, brick))
                                counter += 1
                if counter > 0:
                        print(element_type + " ---> found and loaded... " + str(counter) + " instances") 
                else:
                        print(element_type + "---> not found")
        else:
                print(element_type + " ---> not found")

print ("All IFC entities have been mapped to KG!")
        
#########################################################################################
############################     Create Relationships      ##############################
#########################################################################################

print ("1st step: Distribution Ports processing...")

# 1a. Distribution component Ports for connecivity of components (using  BOT, FSO)

connections = f.by_type("IFCRELCONNECTSPORTS")
for connection in connections:
        component_1 = connection.RelatedPort.Nests[0].RelatingObject
        component_2 = connection.RelatingPort.Nests[0].RelatingObject              
        graph.add((OM_inst(component_1), FSO.connectedWith, OM_inst(component_2)))
        if connection.RelatedPort.FlowDirection == "SINK" or (connection.RelatedPort.FlowDirection == "SOURCEANDSINK" and connection.RelatedPort.Name[0:6] == 'Inport'): # SINK/Inport is inlet
                graph.add((OM_inst(component_1), FSO.feedsFluidTo, OM_inst(component_2)))
        if connection.RelatedPort.FlowDirection == "SOURCE" or (connection.RelatedPort.FlowDirection == "SOURCEANDSINK" and connection.RelatedPort.Name[0:7] == 'Outport'): #SOURCE/Outlet is outlet
                graph.add((OM_inst(component_2), FSO.feedsFluidTo, OM_inst(component_1)))

print ("2nd step: System groups processing...")

## 2. Systems from grouped elements - IfcSystems need to be generated from enrichment processes

systems = f.by_type("IfcSystem")
for system in systems:
        # Create relationship: inst_system fso:hascomponent inst_component
        for comp in system.IsGroupedBy[0].RelatedObjects:
                if comp.__dict__["type"] != "IfcDistributionPort":
                        graph.add((OM_inst(system), FSO.hasComponent, OM_inst(comp)))   
                        graph.add((OM_inst(system), BRICK.hasPart, OM_inst(comp)))   

print ("3rd step: Topology processing...")

# Topological relationships (brick:hasLocation) + properties
spaces = f.by_type("IfcSpace")
for space in spaces:
        storey = space.Decomposes[0].RelatingObject
        building = storey.Decomposes[0].RelatingObject
        # Loading triples in the graph
        graph.add((OM_inst(building), BOT.hasStorey, OM_inst(storey)))
        graph.add((OM_inst(building), BRICK.hasPart, OM_inst(storey)))
        graph.add((OM_inst(storey), BOT.hasSpace, OM_inst(space)))
        graph.add((OM_inst(storey), BRICK.hasPart, OM_inst(space)))
        for prop in space.IsDefinedBy: 
                try: #try and find area and volume properties in spaces (if they exist)
                        for q in prop.RelatingPropertyDefinition.Quantities:
                                if q.__dict__["type"] == "IfcQuantityVolume":
                                        graph.add((OM_inst(space), BRICK.volume, Literal(q.VolumeValue, datatype=XSD.decimal)))
                                if q.__dict__["type"] == "IfcQuantityArea":
                                        graph.add((OM_inst(space), BRICK.area, Literal(q.AreaValue, datatype=XSD.decimal)))
                except:
                        pass

print ("4th step: Spatial containment processing...")

# Spatial Containment of elements/components
for containment in f.by_type("IFCRELCONTAINEDINSPATIALSTRUCTURE"): 
        if containment.RelatingStructure.__dict__["type"] == "IfcSpace":
                space = containment.RelatingStructure
                for element in containment.RelatedElements: 
                        graph.add((OM_inst(space), BOT.hasElement, OM_inst(element)))
                        graph.add((OM_inst(element), BRICK.hasLocation, OM_inst(space)))

print ("DONE")

#%% Export the graph
graph.serialize(destination="Output.ttl", format="turtle")

print ("Results exported in Output.ttl")

# %%
