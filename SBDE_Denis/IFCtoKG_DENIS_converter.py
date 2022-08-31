#%% Import packages
import os, sys
import ifcopenshell
import json
import pandas as pd
from rdflib.namespace import NamespaceManager
from rdflib import Graph, RDF, URIRef, Literal, XSD

#%% Create a namespace
NS_om = "https://openmetrics.eu/openmetrics#"
NS_bot = "https://w3id.org/bot#"
NS_beo = "https://pi.pauwel.be/voc/buildingelement#"
NS_brick = "https://brickschema.org/schema/Brick#"
NS_rdf = "https://www.w3.org/1999/02/22-rdf-syntax-ns#"
NS_owl = "https://www.w3.org/2002/07/owl#"
NS_schema = "https://schema.org#"
NS_mep = "https://pi.pauwel.be/voc/distributioncomponent#"
NS_fso = "https://www.w3id.org/fso#"
NS_props = "https://w3id.org/props#"
NS_xsd = "https://www.w3.org/2001/XMLSchema#"


graph = Graph()
graph.namespace_manager.bind("om", URIRef(NS_om))
graph.namespace_manager.bind("bot", URIRef(NS_bot))
graph.namespace_manager.bind("brick", URIRef(NS_brick))
graph.namespace_manager.bind("rdf", URIRef(NS_rdf))
graph.namespace_manager.bind("owl", URIRef(NS_owl))
graph.namespace_manager.bind("schema", URIRef(NS_schema))
graph.namespace_manager.bind("props", URIRef(NS_props))
graph.namespace_manager.bind("xsd", URIRef(NS_xsd))


#%% Import IFC file
print("Importing IFC...")
f = ifcopenshell.open('SCNew.ifc')
props_guid = URIRef(NS_props + "hasGuid")
props_name = URIRef(NS_props + "hasName")

#%% Converter 

#####################################################################################
###############     TRANSFORM and LOAD product instances      #######################
#####################################################################################
 
if f.wrapped_data.schema == "IFC2X3": 
        print("Version: "+"ifc2x3")
        with open('mapping_table_IFC2x3.json') as m:
                map = json.load(m)
elif f.wrapped_data.schema == "IFC4":
        print("Version: "+"ifc4")
        with open('mapping_DENIS.json') as m:
                map = json.load(m)    
else:
        print("Not supporting version: " + f.wrapped_data.schema)

print("Mapping IFC entities to Knowledge Graph...")

for element in map:
        components = f.by_type(element)
        if not components:
                print (element + "--> not found")
        else:
                print("Loading..." + element)
                for component in components:
                        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
                        graph.add((inst, props_guid, Literal(component.GlobalId, datatype=XSD.string)))        
                        if component.Description != None:
                                graph.add((inst, props_name, Literal(component.Name + " / " + component.Description, datatype=XSD.string)))        
                        else:
                                graph.add((inst, props_name, Literal(component.Name, datatype=XSD.string)))   
                        if map[component.__dict__["type"]]["bot"] != "":
                                bot = URIRef(NS_bot + map[component.__dict__["type"]]["bot"])
                                graph.add((inst, RDF.type, bot))
#                        if map[component.__dict__["type"]]["beo"] != "":
#                                beo = URIRef(NS_beo + map[component.__dict__["type"]]["beo"])
#                                graph.add((inst, RDF.type, beo))
#                        if map[component.__dict__["type"]]["mep"] != "":
#                                mep = URIRef(NS_mep + map[component.__dict__["type"]]["mep"])
#                                graph.add((inst, RDF.type, mep))
#                        if map[component.__dict__["type"]]["fso"] != "":
#                                fso = URIRef(NS_fso + map[component.__dict__["type"]]["fso"])
#                                graph.add((inst, RDF.type, fso))                              
                        if map[component.__dict__["type"]]["brick"] != "":
                                brick = URIRef(NS_brick + map[component.__dict__["type"]]["brick"])
                                graph.add((inst, RDF.type, brick))

print ("All IFC entities have been mapped to KG!")


#########################################################################################
############################     Create Relationships      ##############################
#########################################################################################

#print ("Parsing distribution ports...")

# 1a. Distribution component Ports for connecivity of components (using  BOT, FSO)

#connections = f.by_type("IFCRELCONNECTSPORTS")
#connectedWith = URIRef(NS_fso + "connectedWith")
#feedsFluidTo = URIRef(NS_fso + "feedsFluidTo") # only between fso components (every distribution element in IFC)
#
#for connection in connections:
#        component_1 = connection.RelatedPort.Nests[0].RelatingObject
#        inst_1 = URIRef(NS_om + "inst_" + component_1.GlobalId.replace("$","_"))
#        component_2 = connection.RelatingPort.Nests[0].RelatingObject              
#        inst_2 = URIRef(NS_om + "inst_" + component_2.GlobalId.replace("$","_"))
#        graph.add((inst_1, connectedWith, inst_2))
#        if connection.RelatedPort.FlowDirection == "SINK" or (connection.RelatedPort.FlowDirection == "SOURCEANDSINK" and connection.RelatedPort.Name[0:6] == 'Inport'): # SINK/Inport is inlet
#                graph.add((inst_1, feedsFluidTo, inst_2))
#        if connection.RelatedPort.FlowDirection == "SOURCE" or (connection.RelatedPort.FlowDirection == "SOURCEANDSINK" and connection.RelatedPort.Name[0:7] == 'Outport'): #SOURCE/Outlet is outlet
#                graph.add((inst_2, feedsFluidTo, inst_1))


#print("1st step... ports processed!")
#
#
## 2. Systems from grouped elements - IfcSystems need to be generated from enrichment processes
#
#systems = f.by_type("IfcSystem")
#distributionsystem = URIRef(NS_fso + "DistributionSystem")
##hasConsumerComponent = URIRef(NS_fso + "hasComponent")
##hasSourceComponent = URIRef(NS_fso + "hasComponent")
#hascomponent = URIRef(NS_fso + "hasComponent")
#hasName = URIRef(NS_props + "hasName")
#for system in systems:
#        inst_system = URIRef(NS_om + "inst_" + system.GlobalId.replace("$","_"))
#        inst_system_name = Literal(str(system.ObjectType))
#        graph.add((inst_system, RDF.type, distributionsystem))
#        graph.add((inst_system, hasName, inst_system_name))
#        # Create relationship: inst_system fso:hascomponent inst_component
#        for comp in system.IsGroupedBy[0].RelatedObjects:
#                if comp.__dict__["type"] != "IfcDistributionPort":
#                        inst_comp = URIRef(NS_om + "inst_" + comp.GlobalId.replace("$","_"))
#                        graph.add((inst_system, hascomponent, inst_comp))   


# Topological relationships (brick:hasLocation) + properties

hasPart = URIRef(NS_brick + "hasPart")
hasStorey = URIRef(NS_bot + "hasStorey")
hasSpace = URIRef(NS_bot + "hasSpace")
spaces = f.by_type("IfcSpace")
for space in spaces:
        inst_space = URIRef(NS_om + "inst_" + space.GlobalId.replace("$","_"))
        storey = space.Decomposes[0].RelatingObject
        inst_storey = URIRef(NS_om + "inst_" + storey.GlobalId.replace("$","_"))
        building = storey.Decomposes[0].RelatingObject
        inst_building = URIRef(NS_om + "inst_" + building.GlobalId.replace("$","_"))
        # Loading triples in the graph
        graph.add((inst_building, hasStorey, inst_storey))
        graph.add((inst_building, hasPart, inst_storey))
        graph.add((inst_storey, hasSpace, inst_space))
        graph.add((inst_storey, hasPart, inst_space))
        for prop in space.IsDefinedBy: 
                try: #try and find area and volume properties in spaces (if they exist)
                        for q in prop.RelatingPropertyDefinition.Quantities:
                                if q.__dict__["type"] == "IfcQuantityVolume":
                                        brick_volume = URIRef(NS_brick + "volume")
                                        graph.add((inst_space, brick_volume, Literal(q.VolumeValue, datatype=XSD.decimal)))
                                if q.__dict__["type"] == "IfcQuantityArea":
                                        brick_volume = URIRef(NS_brick + "area")
                                        graph.add((inst_space, brick_volume, Literal(q.AreaValue, datatype=XSD.decimal)))
                except:
                        pass

# Spatial Containment of elements/components
hasLocation = URIRef(NS_brick + "hasLocation")
containments = f.by_type("IFCRELCONTAINEDINSPATIALSTRUCTURE")
hasElement = URIRef(NS_bot + "hasElement")
for containment in containments: 
        if containment.RelatingStructure.__dict__["type"] == "IfcSpace":
                inst_space = URIRef(NS_om + "inst_" + containment.RelatingStructure.GlobalId.replace("$","_"))
                for element in containment.RelatedElements: 
                        inst_element = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
                        graph.add((inst_space, hasElement, inst_element))
                        graph.add((inst_element, hasLocation, inst_space))

thermostats = f.by_type("IfcUnitaryControlElement")
hasPoint = URIRef(NS_brick + "hasPoint")
for thermostat in thermostats:
        inst_thermostat = URIRef(NS_om + "inst_" + thermostat.GlobalId.replace("$","_"))
        for property in thermostat.IsDefinedBy: 
                for prop in property.RelatingPropertyDefinition.HasProperties:
                        if prop.Name == "SerialNumber":
                                hasNumber = URIRef(NS_props + "hasSerialNumber")
                                serial_number = Literal(prop.NominalValue.wrappedValue.replace(".","_"))
                                graph.add((inst_thermostat, hasNumber, serial_number))
                                #Create and add points
                                # CO2 sensor
                                co2_point = URIRef(NS_brick + "CO2_Sensor")
                                inst_co2_point = URIRef(NS_om + "inst_co2_" + prop.NominalValue.wrappedValue.replace(".","_"))
                                graph.add((inst_co2_point, RDF.type, co2_point))
                                # LUM sensor
                                lum_point = URIRef(NS_brick + "Luminance_Sensor")
                                inst_lum_point = URIRef(NS_om + "inst_lum_" + prop.NominalValue.wrappedValue.replace(".","_"))
                                graph.add((inst_lum_point, RDF.type, lum_point))
                                # PM2.5 sensor
                                pm25_point = URIRef(NS_brick + "PM2.5_Sensor")
                                inst_pm25_point = URIRef(NS_om + "inst_pm25_" + prop.NominalValue.wrappedValue.replace(".","_"))
                                graph.add((inst_pm25_point, RDF.type, pm25_point))
                                # RH sensor
                                rh_point = URIRef(NS_brick + "Relative_Humidity_Sensor")
                                inst_rh_point = URIRef(NS_om + "inst_rh_" + prop.NominalValue.wrappedValue.replace(".","_"))
                                graph.add((inst_rh_point, RDF.type, rh_point))
                                # TEMP sensor
                                temp_point = URIRef(NS_brick + "Temperature_Sensor")
                                inst_temp_point = URIRef(NS_om + "inst_temp_" + prop.NominalValue.wrappedValue.replace(".","_"))
                                graph.add((inst_temp_point, RDF.type, temp_point))
                                # OCC sensor
                                occ_point = URIRef(NS_brick + "Occupancy_Sensor")
                                inst_occ_point = URIRef(NS_om + "inst_occ_" + prop.NominalValue.wrappedValue.replace(".","_"))
                                graph.add((inst_occ_point, RDF.type, occ_point))
                                # Add sensors under thermostats
                                graph.add((inst_thermostat, hasPoint, inst_co2_point))                               
                                graph.add((inst_thermostat, hasPoint, inst_occ_point))
                                graph.add((inst_thermostat, hasPoint, inst_temp_point))
                                graph.add((inst_thermostat, hasPoint, inst_rh_point))
                                graph.add((inst_thermostat, hasPoint, inst_pm25_point))
                                graph.add((inst_thermostat, hasPoint, inst_lum_point))


#%% Export the graph
graph.serialize(destination="Output_original.ttl", format="turtle")


