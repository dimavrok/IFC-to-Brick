#%% Import packages
from re import U
from signal import SIG_DFL
from django.forms import URLInput
import ifcopenshell
import json
import pandas as pd

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
NS_mep = "https://pi.pauwel.be/voc/distributioncomponent#"
NS_fso = "http://www.w3id.org/fso#"
NS_props = "https://w3id.org/props#"

#%% Import IFC file
f = ifcopenshell.open("Basement_East_Plantroom.ifc")

'''
buildings = f.by_type("IfcBuilding")
stories = f.by_type("IfcBuildingStorey")
spaces = f.by_type("IfcSpace")
zones = f.by_type("IfcZone")
systems = f.by_type("IfcUnitaryEquipment")
thermostats = f.by_type("IfcUnitaryControlcomponent")
lights = f.by_type("IfcLightFixture")
'''


# components related to Ventilation System
ductsegments = f.by_type("IfcDuctSegment")
ductfittings = f.by_type("IfcDuctFitting")
airterminals = f.by_type("IfcAirTerminal")
dampers = f.by_type("IfcDamper")
fans = f.by_type("IfcFan")
ductsilencers = f.by_type("IfcDuctSilencer")

#components related to Electrical Systems 
electricdistributionboards = f.by_type("ifcelectricdistributionboard")
alarms = f.by_type("ifcalarm")
lightfixtures = f.by_type("IfcLightFixture")
switchingdevices = f.by_type("IfcSwitchingDevice")
electricappliances = f.by_type("IfcElectricAppliance")

#components related to Plumbing/Drainage
pipesegments = f.by_type("ifcpipesegment")
pipefittings = f.by_type("ifcpipefitting")
firesuppresionterminals = f.by_type("ifcFireSuppressionTerminal")
tanks = f.by_type("ifcTank")
pumps = f.by_type("ifcPump")

#components related to Central Heating
heatexchangers = f.by_type("IfcHeatExchanger")
spaceheaters = f.by_type("IfcSpaceHeater") 

#components related to "Others" - General
controllers = f.by_type("IfcController")
unitaryequipment = f.by_type("IfcUnitaryEquipment")
sensors = f.by_type("IfcSensor")

# These are used for creating relations
connections = f.by_type("IfcRelConnectsPorts")
nests = f.by_type("IfcRelNests")


#%% 
graph = Graph()
graph.namespace_manager.bind("om", URIRef(NS_om))
graph.namespace_manager.bind("bot", URIRef(NS_bot))
#graph.namespace_manager.bind("brick", URIRef(NS_brick))
graph.namespace_manager.bind("rdf", URIRef(NS_rdf))
graph.namespace_manager.bind("owl", URIRef(NS_owl))
graph.namespace_manager.bind("schema", URIRef(NS_schema))
graph.namespace_manager.bind("mep", URIRef(NS_mep))
graph.namespace_manager.bind("fso", URIRef(NS_fso))
graph.namespace_manager.bind("props", URIRef(NS_props))


# Some generic classes/relationships
fso_Component = URIRef(NS_fso + "Component")
fso_EnergyConversionDevice = URIRef(NS_fso + "EnergyConversionDevice")
fso_Fitting = URIRef(NS_fso + "Fitting")
fso_FlowController = URIRef(NS_fso + "FlowController")
fso_FlowMovingDevice = URIRef(NS_fso + "FlowMovingDevice")
fso_Segment = URIRef(NS_fso + "Segment")
fso_StorageDevice = URIRef(NS_fso + "StorageDevice")
fso_Terminal = URIRef(NS_fso + "Terminal")
fso_TreatmentDevice = URIRef(NS_fso + "TreatmentDevice")

bot_element = URIRef(NS_bot + "Element")
props_guid = URIRef(NS_props + "hasGuid")

#%% Converter 

#####################################################################################
###############     TRANSFORM and LOAD product instances      #######################
#####################################################################################


# IfcDuctfitting instances

for component in ductfittings:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "DuctFitting")
        graph.add((inst, RDF.type, fso_Fitting))
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))
        
# IfcDuctSilencer instances
for component in ductsilencers:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "DuctSilencer")
        graph.add((inst, RDF.type, fso_TreatmentDevice))
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))


# IfcDuctSegment instances
for component in ductsegments:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "DuctSegment")
        graph.add((inst, RDF.type, fso_Segment))
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))

# IfcAirTerminal instances
for component in airterminals:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "AirTerminal")
        graph.add((inst, RDF.type, fso_Terminal))
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))

# IfcDamper instances
for component in dampers:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "Damper")
        graph.add((inst, RDF.type, fso_FlowController))
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))
      
# IfcFan instances
for component in fans:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "Fan")
        graph.add((inst, RDF.type, fso_FlowMovingDevice))
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))

# IfcDuctSilencer instances
for component in ductsilencers:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "DuctSilencer")
        graph.add((inst, RDF.type, fso_TreatmentDevice))
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))

# ifcelectricdistributionboard instances
for component in electricdistributionboards:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "ElectricDistributionBoard")
        graph.add((inst, RDF.type, fso_FlowController))
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))

# ifcalarm instances
for component in alarms:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "Alarm")
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))

# IfcLightFixture instances
for component in lightfixtures:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "LightFixture")
        graph.add((inst, RDF.type, fso_Terminal))
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))
        
# IfcSwitchingDevice instances
for component in switchingdevices:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "SwitchingDevice")
        graph.add((inst, RDF.type, fso_FlowController))
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))

# IfcElectricAppliance instances
for component in electricappliances:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "ElectricAppliance")
        graph.add((inst, RDF.type, fso_Terminal))
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))

# ifcFireSuppressionTerminal instances
for component in firesuppresionterminals:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "FireSuppressionTerminal")
        graph.add((inst, RDF.type, fso_Terminal))
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))

# ifcTank instances
for component in tanks:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "Tank")
        graph.add((inst, RDF.type, fso_StorageDevice))
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))


# IfcPump instances
for component in pumps:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "Pump")
        graph.add((inst, RDF.type, fso_FlowMovingDevice))
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))

# IfcHeatExchanger instances
for component in heatexchangers:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "HeatExchanger")
        graph.add((inst, RDF.type, fso_EnergyConversionDevice))
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))
        
# IfcSpaceHeater instances
for component in spaceheaters:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "IfcSpaceHeater")
        graph.add((inst, RDF.type, fso_Terminal))
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))

# IfcController instances
for component in controllers:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "Controller")
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))

# IfcUnitaryEquipment instances
for component in unitaryequipment:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "UnitaryEquipment")
        graph.add((inst, RDF.type, fso_EnergyConversionDevice))
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))

# IfcSensor instances
for component in sensors:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "Sensor")
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))

# PipeSegment instances
for component in pipesegments:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "PipeSegment")
        graph.add((inst, RDF.type, fso_Segment))
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))

# Pipefitting instances
for component in pipefittings:
        inst = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
        mep = URIRef(NS_mep + "PipeFitting")
        graph.add((inst, RDF.type, fso_Fitting))
        graph.add((inst, RDF.type, mep))
        graph.add((inst, props_guid, Literal(component.GlobalId)))



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
        for component in system.IsGroupedBy[0].RelatedObjects:
                if component.__dict__["type"] != "IfcDistributionPort":
                        inst_component = URIRef(NS_om + "inst_" + component.GlobalId.replace("$","_"))
                        graph.add((inst_system, hascomponent, inst_component))   


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
                # The component below is an effort to represent the bbox as a 3D vector: see here --> https://datatracker.ietf.org/doc/html/rfc7946#section-5   
                geojson_rep = {"type":"FeatureCollection","bbox":[cpx,cpy,cpz,cpx+xDim,cpy+yDim,cpz+zDim]}
                # Add instaces in the graph
                inst_3d_rep = Literal(json.dumps(geojson_rep))
                graph.add((inst_space, bot_simple3d, inst_3d_rep))
        except:
                print("not detected")
                graph.add((inst_space, bot_simple3d, Literal("BBox not found in space with guID:" + str(space.GlobalId) )))
                pass


# component (thermostat) instances
for thermostat in thermostats:
        #Create the URIs using guid
        inst_thermostat = URIRef(NS_om + "inst_thermostat_" + thermostat.GlobalId.replace("$","_")[16:])
        fso_Component = URIRef(NS_bot + "component")
        brick_thermostat = URIRef(NS_brick + "Thermostat")
        # Create: inst_1234 a bot:component, brick:thermostat                          
        graph.add((inst_thermostat, RDF.type, fso_Component))
        graph.add((inst_thermostat, RDF.type, brick_thermostat))
        # Thermostat-Space relationship
        try: 
                # Try and find relating spaces
                space = thermostat.ContainedInStructure[0].RelatingStructure
                #Create relationship: inst_Space bot:containscomponent inst:thermostat
                inst_space = URIRef(NS_om + "inst_space_" + space.GlobalId.replace("$","_")[16:])
                graph.add((inst_space, URIRef(NS_bot+"containscomponent"), inst_thermostat))
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
        fso_Component = URIRef(NS_bot + "component")
        brick_lighting = URIRef(NS_brick + "Lighting")
        bot_simple3d = URIRef(NS_bot + "hasSimple3DModel")      
        # The component below is an effort to represent the bbox as a 3D vector: see here --> https://datatracker.ietf.org/doc/html/rfc7946#section-5   
        geojson_rep = {"type":"FeatureCollection","bbox":[cpx,cpy,cpz,cpx+xDim,cpy+yDim,cpz+zDim]}
        inst_3d_rep = Literal(json.dumps(geojson_rep))
        # Add instances in the graph
        graph.add((inst_light_fixture, RDF.type, fso_Component))
        graph.add((inst_light_fixture, RDF.type, brick_lighting))
        graph.add((inst_light_fixture, bot_simple3d, inst_3d_rep))
'''

#%% Export the graph
graph.serialize(destination="Data_Graph.ttl", format="turtle")


# %%
