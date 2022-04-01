# Building-Metadata-Integration
This project attempts to integrate IFC and Brick Schema to allow configuration of data analytics in building operation

This is a simple example of transforming an IFC file using Python

Dependencies: 

IFC to RDF --> ifcopenshell/RDFlib

BMS to RDF --> RDFlib/pybrickschema

RDF validation --> RDFlib/pySHACL



Objectives of this project: 
1. Transform IFC instances (spaces/zones/systems/equipment) into RDF using BOT, Brick Schema or any other ontology 
2. Translate BMS metadata into RDF using Brick Schema or any other ontology
3. Provide guidelines on how these metadata should be integrated, e.g. aligning ifcSpace with brick:Space
4. Investigate how SHACL can perform completeness checking: Is the final model complete to allow application dvelopers create analytics? 
