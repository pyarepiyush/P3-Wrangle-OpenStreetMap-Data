
# Update county values
def update_county(county):
    
    # remove , CA from county names if exists    
    if ',' in county:
        pos=county.index(",")
        county=county[:pos]
    
    return county
    