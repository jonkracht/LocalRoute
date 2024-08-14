import pandas as pd
import json

with open('data/raw/database-2024-08-11.json', 'r') as f:
    data = json.load(f)

new_dict = {}

for id, dict in data.items():
    for key in ['address', 'geo', 'aggregateRating']:
        if key in dict: # check that key is in dictionary
            for k, v in dict[key].items():
                dict[k] = v
            del dict[key]

    if 'amenityFeature' in dict:
        for feature in dict['amenityFeature']:
            dict[feature['name']] = feature['value']
        
        del dict['amenityFeature']

    
    if 'Multiple Tees / Pins' in dict:
        dict['multiple_tees'], dict['multiple_pins'] = [el.strip() for el in dict['Multiple Tees / Pins'].split('/')]
        del dict['Multiple Tees / Pins']

    new_dict[id] = dict


# Convert to pandas dataframe
df = pd.DataFrame(new_dict).T

# Save as pickle
df.to_pickle('data/interim/processed-data.pkl')
