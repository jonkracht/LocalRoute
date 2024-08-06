
# Function to return a list of URL's on the DGCR website satisfying certain criteria

import requests
from bs4 import BeautifulSoup


def scrape_html(some_url):
    """Function to return formatted HTML for an arbitrary website"""
    r = requests.get(some_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup




# URL of first page of search results (should include something like 'page=X' in it)
#baseurl = 'https://www.dgcoursereview.com/browse.php?cname=&designer=&holes=&length_min=&length_max=&holetype=&coursetype=a%3A2%3A{i%3A0%3Bi%3A1%3Bi%3A1%3Bi%3A2%3B}&terrain=a%3A3%3A{i%3A0%3Bi%3A1%3Bi%3A1%3Bi%3A2%3Bi%3A2%3Bi%3A3%3B}&landscape=a%3A3%3A{i%3A0%3Bi%3A1%3Bi%3A1%3Bi%3A2%3Bi%3A2%3Bi%3A3%3B}&teetype=&mtees=&mpins=&cf=&num_reviews=&rating_min=&rating_max=&yem=&yex=&country=1&state=45&city=&photos=&videos=&tourneys=&camping=&restrooms=&nopets=&private=1&paytoplay=1&on_bg=&extinct=&zipcode=&zip_distance=25&sort=name&order=ASC&page='
# save_name = '

baseurl = 'https://www.dgcoursereview.com/browse.php?cname=&designer=&holes=&length_min=&length_max=&holetype=&coursetype=a%3A2%3A{i%3A0%3Bi%3A1%3Bi%3A1%3Bi%3A2%3B}&terrain=a%3A3%3A{i%3A0%3Bi%3A1%3Bi%3A1%3Bi%3A2%3Bi%3A2%3Bi%3A3%3B}&landscape=a%3A3%3A{i%3A0%3Bi%3A1%3Bi%3A1%3Bi%3A2%3Bi%3A2%3Bi%3A3%3B}&teetype=&mtees=&mpins=&cf=&num_reviews=&rating_min=&rating_max=&yem=&yex=&country=1&state=&city=&photos=&videos=&tourneys=&camping=&restrooms=&nopets=&private=1&paytoplay=1&on_bg=&extinct=&zipcode=&zip_distance=25&sort=name&order=ASC&page='
save_name = 'all_course_URLs'

# Initialize list into which URLs will be added
url_list = []

# Scrape first page
html = scrape_html(baseurl + '1')

# Determine number of pages over which to scrape (website specific)
n_results = int(html.find(class_ = 'right note_bold').get_text().strip().split()[0])

results_per_page = 20
n_pages = (n_results-1)//results_per_page + 1


for page_ct in range(1, n_pages+1):

    print('Grabbing page ' + str(page_ct) + ' of ' + str(n_pages))

    if page_ct > 1:
        html = scrape_html(baseurl + str(page_ct))

    table = html.find('table', {'class':'form_cell'})

    rows = table.find_all(class_ = 'note')

    for r in rows:
        url_list.append(r.find('a')['href'])

# Save file
f = open(save_name + '.txt', 'w')

for line in url_list:
    f.write(line + '\n')

f.close()
