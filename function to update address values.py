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