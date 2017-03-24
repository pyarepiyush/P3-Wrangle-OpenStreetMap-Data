# Clean and Upload as JSON format

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