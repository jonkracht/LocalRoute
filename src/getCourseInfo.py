def get_course_info(base_url):

    """Function to retrieve disc golf course attributes form dgcoursereview.com"""

    import requests
    from bs4 import BeautifulSoup
    import json
    import re

    missing_value = None

    # Get html of desired dgcr page
    r = requests.get(base_url + '&mode=ci')
    html = BeautifulSoup(r.text, 'html.parser')

    # Initialize dictionary to store course info parameters
    course_info = {}

    course_info['url'] = base_url
    
    # Grab tag with type 'application/ld+json' with multiple parameters of interest
    dict=json.loads(html.find('script', type="application/ld+json").text)
    dict_keys=['name','description','isAccessibleForFree','address','geo','aggregateRating','amenityFeature']

    for d in dict_keys:
        # Handle potential missing values with try/except
        try: 
            course_info[d] = dict[d]
        except:
            course_info[d] = missing_value

    # Pull out some other info peppered throughout page
    keys = ['Year established', 'Designer', 'Multiple Tees / Pins', 'Tee Type', 'Hole Type']

    for key in keys:
        try: 
            course_info[key] = html.find(string = re.compile(key)).find_parent().find_next().text
        except:
            course_info[key] = missing_value


    #  Parameters where value is listed before key
    for key in ['Water in play', 'Baskets', 'Holes']:
        try: 
            course_info[key] = html.find(class_='c-course-stat-label', string = key).find_previous().text
        except:
            course_info[key] = missing_value
    

    # Grab attributes from table rows
    
    rows = ['SSE', 'Par Info']

    for row in rows:
        try:
            S = html.find(string=re.compile(row)).find_parent().find_parent().find_all(class_="c-bullet")

            course_info[row] = [s.text.strip() for s in S]

        except:
            course_info[row] = []

    # Course conditions
    try: 
        course_info['Course conditions']  = html.find('h3', string="Course conditions:").find_parent().find(class_='active').text
    except:
        course_info['Course conditions'] = missing_value


    # Course length - use class of "dg_unit"
    key='Metric length'
    try:
        course_info[key] = [int(s['data-meters']) for s in html.find_all(class_="dg_unit")]
    except:
        course_info[key] = missing_value

    key='Imperial length'
    try:
        course_info[key] = [int(s['data-feet']) for s in html.find_all(class_="dg_unit")]
    except:
        course_info[key] = missing_value
    

    # Wooded-ness: find string "Wooded" in html
    key = 'Woodedness'
    try:
        course_info[key] = html.find(class_='c-course-stat-label', string=re.compile('Wooded')).text
    except:
        course_info[key] = missing_value

    # Terrain:  Values of Mostly Flat, Moderately Hilly, Very Hilly
    key = 'Terrain'
    try:
        isFlat = html.find(string=re.compile('Flat'))
        if isFlat:
            course_info[key] = isFlat
        else:
            course_info[key] = html.find(string=re.compile('Hilly'))
    except:
        course_info[key] = missing_value


    return course_info



if __name__ == '__main__':
    base_url = 'https://www.dgcoursereview.com/course.php?id='
    default_course_id = '5583' # Stafford Woods, NJ

    course_id = input('\nEnter DGCR ID of interest (default is ' + default_course_id + '): ')

    if course_id == "":
        course_id = default_course_id

    course_data = get_course_info(base_url + course_id)
    
    print("\nScraped data:")
    for key, value in course_data.items():
        print(f"{key:<25} {value}")

