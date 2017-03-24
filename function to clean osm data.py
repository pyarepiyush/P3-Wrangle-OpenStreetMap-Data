import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict
import re
import string
import codecs
import json


CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


# patterns needed to identify tags
pattern_county = re.compile(r':county[_name]*$') # county name
pattern_zip = re.compile(r'zip|postcode') # zip/postal code
pattern_digit = re.compile(r'^\d*\d$') # integer characters

def shape_element(element):
    node = {}
                    
    if element.tag == "node" or element.tag == "way" :
        
        '''
        - all attributes of "node" and "way" should be turned into regular key/value pairs, except:
            - attributes in the CREATED array should be added under a key "created"
            - attributes for latitude and longitude should be added to a "pos" array,
              for use in geospacial indexing. Make sure the values inside "pos" array are floats
              and not strings. 
        '''
        node["created"] = {}
        node["pos"] = []       
        node["type"] = element.tag
        
        for key, value in element.attrib.items():
                
                
            if key in CREATED:
                node["created"][key] = value

            elif key in ["lat","lon"]:
                node["pos"].insert(0,float(value))
                
            else:
                node[key]  = value
                
                
            

        ''' 
        - if the second level tag "k" value contains problematic characters, it should be ignored
        - if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
        - if the second level tag "k" value does not start with "addr:", but contains ":", you can
          process it in a way that you feel is best. For example, you might split it into a two-level
          dictionary like with "addr:", or otherwise convert the ":" to create a valid key.

        '''
        
        create_addr = 0
        for tag in element.iter("tag"):
            
            # if the values are not problematic, start populating the dictionary
            if not(re.search(problemchars, tag.attrib["k"])):
                
                '''or 'zip' in element.attrib["k"]:'''
                # Initialize dict address
                if (tag.attrib["k"][:5]=="addr:" and tag.attrib["k"].count(':') == 1) or pattern_county.search(tag.attrib["k"]) or pattern_zip.search(tag.attrib["k"]):
                    if create_addr==0:
                        node["address"]={}
                    create_addr = 1                   


                # if tag attribute is :addr
                if tag.attrib["k"][:5]=="addr:":
                    
                    
                        
                    # Update county values and populate
                    if pattern_county.search(tag.attrib["k"]):
                        node["address"]["county"] = update_county(tag.attrib["v"])
                        
                    # Update zip values and populate  
                    elif  pattern_zip.search(tag.attrib["k"]):
                        node["address"]["zip"] = update_zip(tag.attrib["v"])                    

                    # Update street values and populate  
                    elif tag.attrib["k"][5:] == 'street':
                        node["address"]["street"] = update_address(tag.attrib["v"])

                    # Remaining
                    else:
                        node["address"][tag.attrib["k"][5:]] = tag.attrib["v"]

                # if tag attribute is not :addr
                elif tag.attrib["k"][:5] != 'addr:':
                   
                    # Update county values
                    if pattern_county.search(tag.attrib["k"]):
                        node["address"]["county"] = update_county(tag.attrib["v"])
                        
                    # Update zip values and populate  
                    elif  pattern_zip.search(tag.attrib["k"]):
                        node["address"]["zip"] = update_zip(tag.attrib["v"])  
                        
                    # Remove non-integer characters from building-levels
                    elif tag.attrib["k"] =="building:levels":
                        if pattern_digit.search(tag.attrib["v"]):
                            node[tag.attrib["k"]] =  int(tag.attrib["v"])
                        
                    else:
                        node[tag.attrib["k"]] =  tag.attrib["v"]
  
  
        create_node_ref=0
        if element.tag == "way":
            for nd in element.iter("nd"):
                if  create_node_ref==0:
                    node["node_refs"] = []
                create_node_ref=1    
                node["node_refs"].append(nd.attrib["ref"])
                

        return node
        
    else:
        return None

    
