def makeDataFrame(json_file):
    '''Takes json file.'''

    import pandas as pd
    import json

    new_dict = {}

    for id, dict in json_file.items():
        for key in ['address', 'geo', 'aggregateRating']:
            if key in dict: # check key exists
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


    # Rename columns
    df = df.rename(columns={
                    #'url', 'name', 'description', 
                   'isAccessibleForFree':'free', 'Year established':'year_established',
                   'Designer':'designer', 'Tee Type':'tee_type', 'Hole Type':'basket_type', 
                    'Water in play':'water_in_play', 'Baskets': 'basket_number',
                    'Holes':'number_of_holes', 'SSE':'sse', 'Par Info':'par', 'Course conditions':'course_condition', 
                    'Metric length':'length_metric', 'Imperial length':'length_imperial', 'Links':'links', 
                    'Extinct':'is_extinct', 'Local Directions':'local_directions',
                   #'Rounds Recorded & Average Score', '@type', 
                    'streetAddress':'street_address',
                   'addressLocality':'town', 'addressRegion':'region', 'postalCode':'postal_code', 
                    'addressCountry':'country',
                   #'latitude', 'longitude', 
                    'rating':"rating_avg", 'bestRating':'rating_max', 'worstRating':'rating_min',
                   'ratingCount':'rating_count', 
                    'Disc golf course':'disc_golf_course', 'Camping':'camping', 'Pet-Friendly':'pet_friendly',
                   'Restrooms':'has_restrooms', 'On ball golf':'on_ball_golf_course', 'Cart-Friendly':'cart_friendly', 
                    #'multiple_tees', 'multiple_pins'
                  }).copy()

    # Remove needless columns
    df.drop(['@type'], axis=1, inplace=True) # vestige of scraping
    df.drop(['disc_golf_course'], axis=1, inplace=True) # included in every entry for some reason
    
    # Change column dtypes
    

    return df


if __name__ == "__main__":

    import json

    default_file = "database-2024-08-11"
    file_name = input("Which file to process?  (Default is \'" + default_file + "\')")

    if file_name == "":
        file_name = default_file

    with open("data/raw/" + file_name + ".json", "r") as f:
        json_file = json.load(f)

    df = makeDataFrame(json_file)

    df.to_pickle("data/interim/" + file_name + "-processed.pkl")


    
    

