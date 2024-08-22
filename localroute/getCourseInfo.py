def get_course_info(base_url):
    """Function to retrieve disc golf course attributes form dgcoursereview.com"""

    import requests
    from bs4 import BeautifulSoup
    import json
    import re

    missing_value = None

    # Get html of desired dgcr page
    r = requests.get(base_url + "&mode=ci")
    html = BeautifulSoup(r.text, "html.parser")

    # Initialize dictionary to store course info parameters
    course_info = {}

    course_info["url"] = base_url

    # Grab tag with type 'application/ld+json' with multiple parameters of interest
    dict = json.loads(html.find("script", type="application/ld+json").text)
    dict_keys = [
        "name",
        "description",
        "isAccessibleForFree",
        "address",
        "geo",
        "aggregateRating",
        "amenityFeature",
    ]

    for d in ["name", "description", "isAccessibleForFree"]:
        # Handle potential missing values with try/except
        try:
            course_info[d] = dict[d]
        except:
            course_info[d] = missing_value

    # Handle items with dictionary values separately
    for d in ["address", "geo", "aggregateRating", "amenityFeature"]:
        try:
            course_info[d] = dict[d]
        except:
            course_info[d] = {}

    # Pull out some other info peppered throughout page
    keys = ["Year established", "Multiple Tees / Pins", "Tee Type", "Hole Type"]

    for key in keys:
        try:
            course_info[key] = html.find(string=re.compile(key)).find_parent().find_next().text
        except:
            course_info[key] = missing_value

    # Course designer
    key = "Designer"
    try:
        course_info[key] = html.find(class_="c-course-details").find(string=re.compile("Designer")).find_parent().find_next().text
    except:
        course_info[key] =  missing_value

    #  Parameters where value is listed before key
    for key in ["Water in play", "Baskets", "Holes"]:
        try:
            course_info[key] = (
                html.find(class_="c-course-stat-label", string=key).find_previous().text
            )
        except:
            course_info[key] = missing_value

    # Grab attributes from table rows

    rows = ["SSE", "Par Info"]

    for row in rows:
        try:
            S = (
                html.find(string=re.compile(row))
                .find_parent()
                .find_parent()
                .find_all(class_="c-bullet")
            )

            course_info[row] = [s.text.strip() for s in S]

        except:
            course_info[row] = []

    # Course conditions
    try:
        course_info["Course conditions"] = (
            html.find("h3", string="Course conditions:").find_parent().find(class_="active").text
        )
    except:
        course_info["Course conditions"] = missing_value

    # Course length - use class of "dg_unit"
    key = "Metric length"
    try:
        course_info[key] = [int(s["data-meters"]) for s in html.find_all(class_="dg_unit")]
    except:
        course_info[key] = missing_value

    key = "Imperial length"
    try:
        course_info[key] = [int(s["data-feet"]) for s in html.find_all(class_="dg_unit")]
    except:
        course_info[key] = missing_value

    # Terrain
    key = "Terrain"
    try:
        l = [
            v.text.strip()
            for v in html.find(class_="c-course-course_info").find_all(class_="c-course-stat")
        ]
        for t in ["Mostly Flat", "Moderately Hilly", "Very Hilly"]:
            if t in l:
                course_info[key] = t
    except:
        course_info[key] = missing_value

    # Woods
    key = "Woods"
    try:
        l = [
            v.text.strip()
            for v in html.find(class_="c-course-course_info").find_all(class_="c-course-stat")
        ]
        for t in ["Lightly Wooded", "Moderately Wooded", "Heavily Wooded"]:
            if t in l:
                course_info[key] = t
    except:
        course_info[key] = missing_value

    # Link:  Website(s) relevant to course
    key = "Links"
    course_info[key] = [tag.find_parent()["href"] for tag in html.find_all(class_="fas fa-link")]

    # Extinct:  Button below course name indicating if course is no longer open
    key = "Extinct"
    course_info[key] = len(html.find_all(class_="c-course _extinct"))

    # Local directions to navigate to course
    key = "Local Directions"
    course_info[key] = html.find(string="Local Directions:").find_next().text

    # Rounds recorded and average score(s)
    key = "Rounds Recorded & Average Score"

    tag = html.find(string="Rounds Recorded / Average Score:").find_parent().find_next()
    try:
        dict = {}
        dict["Total"] = tag.find("a").text

        for t in tag.find_all(class_="c-bullet"):
            layout_color = t.next_element["style"].split(":")[-1][:-1]
            layout_results = t.text
            dict[layout_color] = layout_results

        course_info[key] = dict

    except:
        course_info[key] = {}

    # Course type: permanent, seasonal, temporary, practice
    key = "course_type"
    try:
        course_info[key] = html.find(class_ = "c-course-info-type").text.split()[0]
    except:
        course_info[key] = missing_value

    return course_info


if __name__ == "__main__":
    base_url = "https://www.dgcoursereview.com/course.php?id="
    default_course_id = "5583"  # Stafford Woods, NJ

    course_id = input("\nEnter DGCR ID of interest (default is " + default_course_id + "): ")

    if course_id == "":
        course_id = default_course_id

    course_data = get_course_info(base_url + course_id)

    print("\nScraped data:\n")
    for key, value in course_data.items():
        print(f"{key:<25} {value}")
