import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict
import re
import string
import codecs
import json


# ### Apply function to clean the data (where problems are detected)

# In[9]:

# Functions to clean data

# update Address values   
mapping = { "St": "Street",
            "St.": "Street",
            "Ave":"Avenue",
            "Rd":"Road",
            "Pl":"Place",
            "Blvd":"Boulevard",
            "Ave":"Avenue",
            "avenue":"Avenue"
            }


def update_address(name):    

    for k,v in mapping.iteritems():
        m = pattern.search(name)
        #print 'm.group() -->',m.group()
        #print 'Old Name -->',name
        if m:
            if m.group() == k:
                name = string.replace(name, k, v, 1)
                #print 'Map -->',k,':',v,'| ', 'Changed Name -->',name
                break
            

    
    return name


# Update county values
def update_county(county):
    
    # remove , CA from county names if exists    
    if ',' in county:
        pos=county.index(",")
        county=county[:pos]
    
    return county
    
    

# Update zip values: If zipcodeis longer than 6 characters, keep first 6 characters only 
def update_zip(zip):
    
    if len(zip)>6:
        zip = zip[:5]
    
    return zip


# ### Clean the data where needed and save the results in JSON file format

# In[10]:


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


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        counter_nodes=0
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")

    return data

data = process_map('sf_sample.osm', False)
    

   


# ### Visually check that the cleaning was successful

# In[11]:

# Visually Check address keys
allzip = defaultdict(int)
count=0
for d in data:
    #print v
    for k in d:
        if k =="address":
            if count<30:
                print d[k]
                count+=1
    


# In[12]:

# Visually Check building values
building = defaultdict(set)
count=0
for d in data:
    
    #print v
    for k in d:
        if "building" in k:
                building[k].add(d[k])
                
for k in building:
    count1=0
    print 'Distinct Value in for building key :',k
    print '----------------------------------------'
    for a in building[k]:        
        if count1<20:            
            print a
            count1+=1
            
    print '----------------------------------------'
   


# In[13]:

# Most common zip-codes
allzip = defaultdict(int)

for d in data:
    #print v
    for k in d:
        if k =="address":
                for j in d[k]:
                    if j == 'zip':
                            allzip[d[k][j]]+=1
#print allzip
print_sorted_list(allzip, 'Top 20 zip values')
    
