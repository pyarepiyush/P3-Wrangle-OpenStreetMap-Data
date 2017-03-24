
# Update zip values: If zipcodeis longer than 5 characters, keep first 5 characters only 
def update_zip(zip):
    
    zip=re.findall(r'^(\d{5})-\d{4}$', zip)
    
    return zip