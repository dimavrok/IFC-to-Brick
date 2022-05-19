#%% Import packages

import ifcopenshell
import json

from rdflib.namespace import NamespaceManager
from rdflib import Graph, RDF, URIRef, Literal

#%% Create a namespace
NS_om = "http://openmetrics.eu/openmetrics#"
NS_bot = "https://w3id.org/bot#"
NS_brick = "https://brickschema.org/schema/Brick#"
NS_rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
NS_rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
NS_owl = "http://www.w3.org/2002/07/owl#"
NS_schema = "http://schema.org#"


#%% Import IFC file
f = ifcopenshell.open("PM-Merged-Lighting-Spaces.ifc")

buildings = f.by_type("IfcBuilding")
stories = f.by_type("IfcBuildingStorey")
spaces = f.by_type("IfcSpace")
zones = f.by_type("IfcZone")
systems = f.by_type("IfcUnitaryEquipment")
thermostats = f.by_type("IfcUnitaryControlElement")
lights = f.by_type("IfcLightFixture")
bboxes = f.by_type("IfcBoundingBox")

#%% 
graph = Graph()
graph.namespace_manager.bind("om", URIRef(NS_om))
graph.namespace_manager.bind("bot", URIRef(NS_bot))
graph.namespace_manager.bind("brick", URIRef(NS_brick))
graph.namespace_manager.bind("rdf", URIRef(NS_rdf))
graph.namespace_manager.bind("owl", URIRef(NS_owl))
graph.namespace_manager.bind("schema", URIRef(NS_schema))

#%% Converter 

# Building instances
for building in buildings:        
        # Create the URIs for stories using the guid#
        inst_building = URIRef(NS_om + "inst_building_" + building.GlobalId.replace("$","_")[16:])
        bot_building = URIRef(NS_bot + "Building")
        # Create: inst_1234 a bot:storey
        graph.add((inst_building, RDF.type, bot_building))

# Storey instances
for storey in stories:
        # Create the URIs for stories
        inst_storey = URIRef(NS_om + "inst_storey_" + storey.GlobalId.replace("$","_")[16:])
        bot_storey = URIRef(NS_bot + "Storey")
        # Create: inst_1234 a bot:storey
        graph.add((inst_storey, RDF.type, bot_storey))
        # Storey-Building relationship
        try:
                # Try and find relating building
                building = storey.Decomposes[0].RelatingObject
                # Create relationship: inst_storey bot:hasSpace inst_space
                inst_building = URIRef(NS_om + "inst_building_" + building.GlobalId.replace("$","_")[16:])
                graph.add((inst_building, URIRef(NS_bot+"hasStorey"), inst_storey))
        except:
                pass

# Zone instances
for zone in zones:
        #Create the URIs using guid
        inst_zone = URIRef(NS_om + "inst_zone_" + zone.GlobalId.replace("$","_")[16:])
        brick_zone = URIRef(NS_brick + "Zone")
        # Create: inst_1234 a bot:zone, brick:Zone                         
        graph.add((inst_zone, RDF.type, brick_zone))

'''
# System instances
for system in systems:
        #Create the URIs using guid
        inst_system = URIRef(NS_om + "inst_system_" + system.GlobalId.replace("$","_")[16:])
        bot_element = URIRef(NS_bot + "Element")
        brick_system = URIRef(NS_brick + "Terminal_Unit")
        # Create: inst_1234 a bot:element, brick:Terminal_unit                          
        graph.add((inst_system, RDF.type, bot_element))
        graph.add((inst_system, RDF.type, brick_system))
        # Try and find related spaces
        try: 
                space = system.ContainedInStructure[0].RelatingStructure
                #Create relationship: inst_space bot:hasLocation inst_system
                inst_space = URIRef(NS_om + "inst_space_" + space.GlobalId.replace("$","_")[16:])
                graph.add((inst_system, URIRef(NS_bot+"hasLocation"), inst_space))      
                # Find the related zones for these spaces
        except:
                pass
        # Try and find relation of zones and systems
        try:
                space = system.ContainedInStructure[0].RelatingStructure
                zone = space.HasAssignments[0].RelatingGroup
                #Create relationship: inst_space bot:hasLocation inst_system
                inst_zone = URIRef(NS_om + "inst_zone_" + zone.GlobalId.replace("$","_")[16:])
                graph.add((inst_system, URIRef(NS_brick+"feeds"), inst_zone))
        except:
                pass
'''

# Space instances
for space in spaces:
        #Create the URIs for spaces
        inst_space = URIRef(NS_om + "inst_space_" + space.GlobalId.replace("$","_")[16:])
        bot_space = URIRef(NS_bot + "Space")
        brick_space = URIRef(NS_brick + "Space")
        # Create: Inst_1234 a bot:space
        graph.add((inst_space, RDF.type, bot_space))
        graph.add((inst_space, RDF.type, brick_space))
        # Storey-Space relationship
        try:
                # Try and find relating storey
                storey = space.Decomposes[0].RelatingObject
                # Create relationship: inst_storey bot:hasSpace inst_space
                inst_storey = URIRef(NS_om + "inst_storey_" + storey.GlobalId.replace("$","_")[16:])
                graph.add((inst_storey, URIRef(NS_bot+"hasSpace"), inst_space))
        except:
                pass
        # Zone-Space relationship
        try: 
                # Try and find relating zones
                zone = space.HasAssignments[0].RelatingGroup
                #Create relationship: inst_zone bot:hasPart inst:space
                inst_zone = URIRef(NS_om + "inst_zone_" + zone.GlobalId.replace("$","_")[16:])
                graph.add((inst_zone, URIRef(NS_brick+"hasPart"), inst_space))
                #Create relationship: inst_zone brick:hasPart inst:space

        except:
                pass
        #Extract the bounding box geometry (cp --> Corner Point,)  
        # ATTENTION: May need to debug in Representations[0] in case there are more representations as in the lighting instances - to discuss this
        try:
                cpx = space.Representation.Representations[1].Items[0].Corner.Coordinates[0]
                cpy = space.Representation.Representations[1].Items[0].Corner.Coordinates[1]
                cpz = space.Representation.Representations[1].Items[0].Corner.Coordinates[2]
                xDim = space.Representation.Representations[1].Items[0].XDim
                yDim = space.Representation.Representations[1].Items[0].YDim
                zDim = space.Representation.Representations[1].Items[0].ZDim
                # The element below is an effort to represent the bbox as a 3D vector: see here --> https://datatracker.ietf.org/doc/html/rfc7946#section-5   
                geojson_rep = {"type":"FeatureCollection","bbox":[cpx,cpy,cpz,cpx+xDim,cpy+yDim,cpz+zDim]}
                # Add instaces in the graph
                inst_3d_rep = Literal(json.dumps(geojson_rep))
                bot_simple3d = URIRef(NS_bot + "hasSimple3DModel")      
                graph.add((inst_space, bot_simple3d, inst_3d_rep))
        except:
                print("not detected")
                pass


'''
# Element (thermostat) instances
for thermostat in thermostats:
        #Create the URIs using guid
        inst_thermostat = URIRef(NS_om + "inst_thermostat_" + thermostat.GlobalId.replace("$","_")[16:])
        bot_element = URIRef(NS_bot + "Element")
        brick_thermostat = URIRef(NS_brick + "Thermostat")
        # Create: inst_1234 a bot:element, brick:thermostat                          
        graph.add((inst_thermostat, RDF.type, bot_element))
        graph.add((inst_thermostat, RDF.type, brick_thermostat))
        # Thermostat-Space relationship
        try: 
                # Try and find relating spaces
                space = thermostat.ContainedInStructure[0].RelatingStructure
                #Create relationship: inst_Space bot:containsElement inst:thermostat
                inst_space = URIRef(NS_om + "inst_space_" + space.GlobalId.replace("$","_")[16:])
                graph.add((inst_space, URIRef(NS_bot+"containsElement"), inst_thermostat))
        except:
                pass    
        # Thermostat-Systems(Terminal Units) relationship  
'''

# Lighting instances
for light in lights:
        #Extract the bounding box geometry (cp --> Corner Point,)  
        cpx = light.Representation.Representations[1].Items[0].Corner.Coordinates[0]
        cpy = light.Representation.Representations[1].Items[0].Corner.Coordinates[1]
        cpz = light.Representation.Representations[1].Items[0].Corner.Coordinates[2]
        xDim = light.Representation.Representations[1].Items[0].XDim
        yDim = light.Representation.Representations[1].Items[0].YDim
        zDim = light.Representation.Representations[1].Items[0].ZDim
        # Create instances
        inst_light_fixture = URIRef(NS_om + "inst_light_" + light.GlobalId.replace("$","_")[16:])
        bot_element = URIRef(NS_bot + "Element")
        brick_lighting = URIRef(NS_brick + "Lighting")
        bot_simple3d = URIRef(NS_bot + "hasSimple3DModel")      
        # The element below is an effort to represent the bbox as a 3D vector: see here --> https://datatracker.ietf.org/doc/html/rfc7946#section-5   
        geojson_rep = {"type":"FeatureCollection","bbox":[cpx,cpy,cpz,cpx+xDim,cpy+yDim,cpz+zDim]}
        inst_3d_rep = Literal(json.dumps(geojson_rep))
        # Add instances in the graph
        graph.add((inst_light_fixture, RDF.type, bot_element))
        graph.add((inst_light_fixture, RDF.type, brick_lighting))
        graph.add((inst_light_fixture, bot_simple3d, inst_3d_rep))


#%% Export the graph
graph.serialize(destination="Data_Graph.ttl", format="turtle")

