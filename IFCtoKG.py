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
NS_mep = "https://pi.pauwel.be/voc/distributionelement#"
NS_fso = "http://www.w3id.org/fso#"


#%% Import IFC file
f = ifcopenshell.open("MoL_GM_Services_Example_Geometry_01.ifc")

'''
buildings = f.by_type("IfcBuilding")
stories = f.by_type("IfcBuildingStorey")
spaces = f.by_type("IfcSpace")
zones = f.by_type("IfcZone")
systems = f.by_type("IfcUnitaryEquipment")
thermostats = f.by_type("IfcUnitaryControlElement")
lights = f.by_type("IfcLightFixture")
'''

# Elements related to Ventilation System
ductsegments = f.by_type("IfcDuctSegment")
ductfittings = f.by_type("IfcDuctFitting")
airterminals = f.by_type("IfcAirTerminal")
dampers = f.by_type("IfcDamper")
fans = f.by_type("IfcFan")
ductsilencers = f.by_type("IfcDuctSilencer")

#Elements related to Electrical Systems 
electricdistributionboards = f.by_type("ifcelectricdistributionboard")
alarms = f.by_type("ifcalarm")
lightfixtures = f.by_type("IfcLightFixture")
switchingdevices = f.by_type("IfcSwitchingDevice")
electricappliances = f.by_type("IfcElectricAppliance")

#Elements related to Plumbing/Drainage
pipesegments = f.by_type("ifcpipesegment")
pipefittings = f.by_type("ifcpipefitting")
firesuppresionterminals = f.by_type("ifcFireSuppressionTerminal")
tanks = f.by_type("ifcTank")
pumps = f.by_type("ifcPump")

#Elements related to Central Heating
heatexchangers = f.by_type("IfcHeatExchanger")
spaceheaters = f.by_type("IfcSpaceHeater") 

#Elements related to "Others" - General
controllers = f.by_type("IfcController")
unitaryequipment = f.by_type("IfcUnitaryEquipment")
sensors = f.by_type("IfcSensor")

# These are used for creating relations
connections = f.by_type("IfcRelConnectsPorts")
nests = f.by_type("IfcRelNests")


#%% 
graph = Graph()
graph.namespace_manager.bind("om", URIRef(NS_om))
#graph.namespace_manager.bind("bot", URIRef(NS_bot))
#graph.namespace_manager.bind("brick", URIRef(NS_brick))
graph.namespace_manager.bind("rdf", URIRef(NS_rdf))
graph.namespace_manager.bind("owl", URIRef(NS_owl))
graph.namespace_manager.bind("schema", URIRef(NS_schema))
graph.namespace_manager.bind("mep", URIRef(NS_mep))
graph.namespace_manager.bind("fso", URIRef(NS_fso))


# Some generic classes
fso_element = URIRef(NS_fso + "Component")

#%% Converter 

#####################################################################################
###############     TRANSFORM and LOAD product instances      #######################
#####################################################################################

# IfcDuctfitting instances
for element in ductfittings:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "DuctFitting")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))

# IfcDuctSilencer instances
for element in ductsilencers:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "DuctSilencer")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))

# IfcDuctSegment instances
for element in ductsegments:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "DuctSegment")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))

# IfcAirTerminal instances
for element in airterminals:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "AirTerminal")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))

# IfcDamper instances
for element in dampers:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "Damper")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))
        
# IfcFan instances
for element in airterminals:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "Fan")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))

# IfcDuctSilencer instances
for element in ductsilencers:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "DuctSilencer")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))

# ifcelectricdistributionboard instances
for element in electricdistributionboards:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "ElectricDistributionBoard")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))

# ifcalarm instances
for element in alarms:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "Alarm")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))

# IfcLightFixture instances
for element in lightfixtures:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "LightFixture")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))
        
# IfcSwitchingDevice instances
for element in switchingdevices:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "SwitchingDevice")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))

# IfcSwitchingDevice instances
for element in electricappliances:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "ElectricAppliance")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))

# ifcFireSuppressionTerminal instances
for element in firesuppresionterminals:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "FireSuppressionTerminal")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))

# ifcTank instances
for element in tanks:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "Tank")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))

# IfcTank instances
for element in tanks:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "Tank")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))

# IfcPump instances
for element in pumps:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "Pump")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))


# IfcHeatExchanger instances
for element in heatexchangers:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "HeatExchanger")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))
        
# IfcSpaceHeater instances
for element in spaceheaters:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "IfcSpaceHeater")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))

# IfcController instances
for element in controllers:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "Controller")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))

# IfcUnitaryEquipment instances
for element in unitaryequipment:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "UnitaryEquipment")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))

# IfcSensor instances
for element in sensors:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "Sensor")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))


# PipeSegment instances
for element in pipesegments:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "PipeSegment")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))

# Pipefitting instances
for element in pipefittings:
        inst = URIRef(NS_om + "inst_" + element.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "PipeFitting")
        graph.add((inst, RDF.type, fso_element))
        graph.add((inst, RDF.type, mep))


#########################################################################################
############################     Create Relationships      ##############################
#########################################################################################

# Distribution Element Ports for connecivity of elements (using BOT, FSO)

connections = f.by_type("IFCRELCONNECTSPORTS")

connectedWith = URIRef(NS_fso + "connectedWith")

for connection in connections:
        component_1 = connection.RelatedPort.Nests[0].RelatingObject
        inst_1 = URIRef(NS_om + "inst_" + component_1.GlobalId.replace("$","_"))
        component_2 = connection.RelatingPort.Nests[0].RelatingObject              
        inst_2 = URIRef(NS_om + "inst_" + component_2.GlobalId.replace("$","_"))
        graph.add((inst_1, connectedWith, inst_2))     
                
'''
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
        inst_zone = URIRef(NS_om + "inst_" + zone.GlobalId.replace("$","_"))
        brick_zone = URIRef(NS_brick + "Zone")
        graph.add((inst_zone, RDF.type, brick_zone))
'''
'''
# Space instances
for space in spaces:
        #Create the URIs for spaces
        inst_space = URIRef(NS_om + "inst_space_" + space.GlobalId.rfgveplace("$","_")[16:])
        bot_space = URIRef(NS_bot + "Space")
        brick_space = URIRef(NS_brick + "Space")
        bot_simple3d = URIRef(NS_bot + "hasSimple3DModel")      
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
                graph.add((inst_space, bot_simple3d, inst_3d_rep))
        except:
                print("not detected")
                graph.add((inst_space, bot_simple3d, Literal("BBox not found in space with guID:" + str(space.GlobalId) )))
                pass


# Element (thermostat) instances
for thermostat in thermostats:
        #Create the URIs using guid
        inst_thermostat = URIRef(NS_om + "inst_thermostat_" + thermostat.GlobalId.replace("$","_")[16:])
        fso_element = URIRef(NS_bot + "Element")
        brick_thermostat = URIRef(NS_brick + "Thermostat")
        # Create: inst_1234 a bot:element, brick:thermostat                          
        graph.add((inst_thermostat, RDF.type, fso_element))
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
        fso_element = URIRef(NS_bot + "Element")
        brick_lighting = URIRef(NS_brick + "Lighting")
        bot_simple3d = URIRef(NS_bot + "hasSimple3DModel")      
        # The element below is an effort to represent the bbox as a 3D vector: see here --> https://datatracker.ietf.org/doc/html/rfc7946#section-5   
        geojson_rep = {"type":"FeatureCollection","bbox":[cpx,cpy,cpz,cpx+xDim,cpy+yDim,cpz+zDim]}
        inst_3d_rep = Literal(json.dumps(geojson_rep))
        # Add instances in the graph
        graph.add((inst_light_fixture, RDF.type, fso_element))
        graph.add((inst_light_fixture, RDF.type, brick_lighting))
        graph.add((inst_light_fixture, bot_simple3d, inst_3d_rep))
'''

#%% Export the graph
graph.serialize(destination="Data_Graph.ttl", format="turtle")


# %%
