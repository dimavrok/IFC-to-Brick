#%% Import packages

import ifcopenshell

from rdflib.namespace import NamespaceManager
from rdflib import Graph, RDF, URIRef

#%% Create a namespace
NS_om = "http://openmetrics.eu/openmetrics#"
NS_bot = "https://w3id.org/bot#"
NS_brick = "https://brickschema.org/schema/1.1/Brick#"
NS_rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

#%% Import IFC file
f = ifcopenshell.open("Example.ifc")
buildings = f.by_type("IfcBuilding")
stories = f.by_type("IfcBuildingStorey")
spaces = f.by_type("IfcSpace")
zones = f.by_type("IfcZone")
systems = f.by_type("IfcUnitaryEquipment")
thermostats = f.by_type("IfcUnitaryControlElement")

#%% 
graph = Graph()
graph.namespace_manager.bind("om", URIRef(NS_om))
graph.namespace_manager.bind("bot", URIRef(NS_bot))
graph.namespace_manager.bind("brick", URIRef(NS_brick))

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

#%% Export the graph
graph.serialize(destination="graph.ttl", format="turtle")



# %% VALIDATION
#import pyshacl
#from pyshacl import validate

#shapes_graph = 
"""
@prefix sh:     <http://www.w3.org/ns/shacl#> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix schema: <http://schema.org/> .
@prefix bot: <https://w3id.org/bot#> .
@prefix brick: <https://brickschema.org/schema/1.1/Brick#> .
@prefix om: <http://openmetrics.eu/openmetrics#> .

schema:PersonShape
    a sh:NodeShape ;
    sh:targetClass schema:Person ;
    sh:property [
        sh:path schema:givenName ;
        sh:datatype xsd:string ;
        sh:name "given name" ;
    ] ;
    sh:property [
        sh:path schema:birthDate ;
        sh:lessThan schema:deathDate ;
        sh:maxCount 1 ;
    ] ;
    sh:property [
        sh:path schema:gender ;
        sh:in ( "female" "male" "nonbinary" "self-descr" ) ;
    ] ;
    sh:property [
        sh:path schema:address ;
        sh:node schema:AddressShape ;
    ] .

schema:AddressShape
    a sh:NodeShape ;
    sh:closed true ;
    sh:property [
        sh:path schema:streetAddress ;
        sh:datatype xsd:string ;
    ] ;
    sh:property [
        sh:path schema:postalCode ;
        sh:datatype xsd:integer ;
        sh:minInclusive 10000 ;
        sh:maxInclusive 99999 ;
    ] .
"""

"""results = validate(graph,               #Insert the graph you want to validate
        shacl_graph = shapes_graph,     #Insert the shapes graph
        graph_format="ttl",             #Specify the format of the graph, can be JSonLD
        shacl_graph_format="ttl",       #Sepcify the format of the shapes graph
        inference="rdfs",               #Say if you want to infer data and how
        debug=True,                     #Report violations
        serialize_report_graph="ttl",   #....covert the report into ttl
    )
conforms, report_graph, report_text = results

print("conforms", conforms)"""