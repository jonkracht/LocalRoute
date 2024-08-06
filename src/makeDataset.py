
# Script to create database of disc golf courses and their features using 'get_course_info.py'

import get_course_info, json

# Input names of files from which to read and write
#file_name, save_name = '/home/jon/PycharmProjects/jon-insight-project/data/raw/PA_course_URLs.txt', 'pa_course_database'
file_name, save_name = '/home/jon/PycharmProjects/jon-insight-project/data/raw/all_course_URLs.txt', 'all_course_database'
file_name, save_name = '../data/raw/', 'pa_course_database'

with open(file_name, 'r') as open_file:
    text_file = open_file.read()

url_list = text_file.split()

# Initialize list in which to store information for the various courses
courses_info = []

# Loop over 'url_list' and retrieve course information
for url in url_list:
    print('Getting info for ' + str(url))
    courses_info.append(get_course_info.get_course_info(url))

# Save file via json
outpath = save_name + '.json'
with open(outpath, "w") as f:
    f.write(json.dumps(courses_info))
