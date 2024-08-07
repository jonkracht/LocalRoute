import getCourseInfo
import json

base_url = 'https://www.dgcoursereview.com/course.php?id='


dict = {}
for i in range(1, 100):
    print(i)
    url = base_url + str(i)

    try:
        dict[int(i)] = getCourseInfo.get_course_info(url)
    except:
        dict[int(i)] = {}

# Save data
with open('data/raw/database.json', 'w') as f:
    f.write(json.dumps(dict))

