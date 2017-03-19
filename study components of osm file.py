
import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict
import re
import string
import codecs
import json



    
###################################
# Study components of the OSM file
###################################


dist_tags = defaultdict(int)
# Count instance of distinct tags
def count_tags(elem,elem_tag):
    
    if elem.tag == elem_tag:
        
        for elements in elem.iter(None):
            #print elements.tag

            dist_tags[elements.tag] +=1
           
    return dist_tags




# return counts of values for tag attribute based on lower, lower+colon, problamechars, or others
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

alltags={}
alltags["lower"]= defaultdict(int)
alltags["lower_colon"]= defaultdict(int)
alltags["problemchars"]= defaultdict(int)
alltags["others"]= defaultdict(int)

def tag_values(event,elem,elem_tag):
    if elem.tag ==elem_tag:
        for elements in elem.iter('tag'): 
            if re.match(lower,elements.attrib['k']):
                alltags["lower"][elements.attrib['k']]+=1
            elif re.match(lower_colon,elements.attrib['k']):
                alltags["lower_colon"][elements.attrib['k']]+=1         
            elif re.match(problemchars,elements.attrib['k']):
                alltags["problemchars"][elements.attrib['k']]+=1 
            else:
                 alltags["others"][elements.attrib['k']]+=1
            

    return alltags






# return counts of zip code values for tag attribute
zip_val= defaultdict(set)

def zip_values(event,elem,elem_tag):
    if elem.tag == elem_tag:
        for elements in elem.iter('tag'):
            if 'zip' in elements.attrib['k'] and len(elements.attrib['v']) > 6:
                zip_val[elements.attrib['k']].add( elements.attrib['v']  )         
    return zip_val


    
# Check Address values
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Real", "Terrace", "Way", "Circle","Highway"]

pattern = re.compile(r'\b\S+\.?$', re.IGNORECASE)

address = defaultdict(set)

def address_values(elem,elem_tag):
    #addr= defaultdict(set)
    if elem.tag == elem_tag:
        for elements in elem.iter('tag'): 
            if elements.attrib['k'] == 'addr:street':
                m = pattern.search(elements.attrib['v'])
                if m:
                    addr_type = m.group()                
                    if addr_type not in expected:
                        address[addr_type].add(elements.attrib['v'] ) 
    #print address
    return address
        
        




# sort by contents of dict by value and print top 20 sorted list
def print_sorted_list(d, message):
    a = sorted(d.iteritems(), key = lambda (k,v): (-v,k)) 
    for i,key in enumerate(a):
        if i<21:
             print i,key

    


    
# Read and Parse the osm file 
counter=0
n_tags={}
ktag_values = {}
address_val = {}
county_list = {}



def read_file(filename,elem_tag):
    global counter 
    global n_tags 
    global ktag_values 
    global address_val 
    global county_list
    for event, elem in ET.iterparse(filename):        

        n_tags =count_tags(elem,elem_tag)  
        ktag_values = tag_values(event,elem,elem_tag)
        address_val = address_values(elem,elem_tag)
        zip_val= zip_values(event,elem,elem_tag)
        
        # Check distinct county names and determine any inconsistensies
        # Check county values
        if counter==0:
            county_list=defaultdict(set)

        if elem.tag == elem_tag:       
            for elements in elem.iter('tag'):
                if ':county' in elements.attrib['k']:            

                    county_list[elements.attrib['k']].add(elements.attrib['v'])
        
        
            counter+=1       
 
    
  
        

    
if __name__ == "__main__":
     read_file('sf_sample.osm','way')


# ### Check resulting value from initial study

# In[3]:

# Print Distinct upper level tags       
print
print "Ct Distinct upper-level tag : ", n_tags
    
    


# In[7]:

# Print different types of keys based on lower, lower+colon, problamechars, or others
print
for k in ktag_values.keys():
    print '--------------'
    print 'values of keys that are ', k
    print_sorted_list(ktag_values[k], 'Top 20 k values')
 


# In[8]:

# print Address types with address values as arrays
print    
print "Address Types: " 
pprint.pprint(address_val) 


# In[93]:

# print county list
    
print "Unique values for counties"
print county_list


# In[120]:

# print distinct keys for zip and their values
    
print "Zip Values"
pprint.pprint(dict(zip_val))
