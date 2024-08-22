import getCourseInfo
import json
from datetime import datetime

base_url = "https://www.dgcoursereview.com/course.php?id="
course_ids = range(1, 15361 + 1)

dict = {}

for id in course_ids:
    print(id)
    url = base_url + str(id)

    try:
        dict[int(id)] = getCourseInfo.get_course_info(url)
    except:
        dict[int(id)] = {}

# Save data
date = datetime.today().strftime("%Y-%m-%d")
with open("data/raw/database-" + date + ".json", "w") as f:
    f.write(json.dumps(dict))
