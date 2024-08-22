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
                   'isAccessibleForFree':'is_free', 'Year established':'year_established',
                   'Designer':'designer', 'Tee Type':'tee_type', 'Hole Type':'basket_type', 
                    'Water in play':'water_in_play', 'Baskets': 'basket_number',
                    'Holes':'number_of_holes', 'SSE':'sse', 'Par Info':'par', 'Course conditions':'course_condition', 
                    'Metric length':'length_metric', 'Imperial length':'length_imperial', 'Links':'links',
                    'Terrain':'terrain', 'Woods':'woods',
                    'Extinct':'is_extinct', 'Local Directions':'local_directions',
                   #'Rounds Recorded & Average Score', '@type', 
                    'streetAddress':'street_address',
                   'addressLocality':'town', 'addressRegion':'region', 'postalCode':'postal_code', 
                    'addressCountry':'country',
                   #'latitude', 'longitude', 
                    'ratingValue':'rating_mean', 'bestRating':'rating_max', 'worstRating':'rating_min',
                   'ratingCount':'rating_count', 
                    'Disc golf course':'disc_golf_course', 
                    'Camping':'has_camping', 'Pet-Friendly':'is_pet_friendly',
                   'Restrooms':'has_restrooms', 'On ball golf':'on_ball_golf_course', 'Cart-Friendly':'is_cart_friendly', 
                   'multiple_tees':'has_multiple_tees', 'multiple_pins':'has_multiple_pins'
                  }).copy()

    # Remove needless columns
    df.drop(['@type'], axis=1, inplace=True) # vestige of scraping
    df.drop(['disc_golf_course'], axis=1, inplace=True) # included in every entry for some reason
    df.drop(['is_extinct'], axis=1, inplace=True) # don't worry about non-existent courses
    df = df[~df["url"].isna()].copy() # drop rows with empty "url" column and therefore no other relevant data
    

    # Change column dtypes
    
    ## Integer columns
    int_cols = ["year_established", "basket_number", "water_in_play", "number_of_holes", "rating_count"]
    for i in int_cols:
        df[i] = df[i].astype('Int64').copy()

    ## Float columns
    float_cols = ["latitude", "longitude", "rating_mean", "rating_max", "rating_min"]
    for f in float_cols:
        df[f] = pd.to_numeric(df[f])

    ## Boolean columns with values "true" or "false"
    tf_list = ["has_camping", "is_pet_friendly", "has_restrooms", "on_ball_golf_course", "is_cart_friendly"]
    
    df["is_free"] = df["is_free"].astype("bool")

    for i in tf_list:
        df[i] = df[i].map({"true":True, "false": False})

    ## Boolean columns with values of "No" or "Yes"
    yn_list = ["has_multiple_tees", "has_multiple_pins"]
    for i in yn_list:
        df[i] = df[i].map({"Yes" :True, "No": False})


    # Map course condition
    df["course_condition"] = df["course_condition"].map({"Perfect": 5, "Good": 4, "Decent": 3, "Bad": 2, "Unplayable": 1})

    return df



if __name__ == "__main__":

    import json, os

    default_file = "database-2024-08-22"
    
    print("\nContents of data/raw:")
    print(os.listdir("data/raw/"))

    file_name = input("\nWhich file to process?  (Default is " + default_file + ")\n")

    if file_name == "":
        file_name = default_file

    with open("data/raw/" + file_name + ".json", "r") as f:
        json_file = json.load(f)

    df = makeDataFrame(json_file)

    df.to_pickle("data/interim/" + file_name + "-interim.pkl")


    
    

