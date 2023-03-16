from bs4 import BeautifulSoup
import requests
from pprint import pprint

WEBSITE = 'https://subslikescript.com/'  # this is the homepage of the website

#################################################
# Get movies list and url to their detailed pages

result = requests.get(f"{WEBSITE}/movies")
content = result.text
soup = BeautifulSoup(content, 'lxml')

# Locate the box that contains the pagination bar => All page links
pagination_box = soup.find('ul', class_='pagination')
page_items = pagination_box.find_all('li', class_='page-item')
last_page_num = page_items[-2].get_text()

# Generate a page range list
pages_range = [i for i in range(1, int(last_page_num) + 1)]

#####################################
# Access and get data of one movie

def get_movie_transcripts(movie_link):
    result = requests.get(movie_link)
    content = result.text
    soup = BeautifulSoup(content, 'lxml')

    # Locate the box that contains title and transcript
    box = soup.find('article', class_='main-article')

    # Locate title and transcript
    title = box.find('h1').get_text()
    transcript = box.find('div', class_='full-script').get_text(strip=True, separator=' ')
    return {
        'title' : title,
        'transcript' :transcript
    }

####################################
# Get all movies link from all pages

links = []

for page_num in pages_range:
    # Locate the title link and text (li) of all article list
    article_box = soup.find(name='article', class_='main-article')

    # Pagination - Get data on multiple pages
    page_link = WEBSITE + f'movies?page={page_num}'

    # Get movies list with the page
    movies = article_box.find_all('a')

    # Append all the link to the list of link
    for movie in movies:
        links.append(movie.get('href'))

# print(links)
print(f"Total number of movies in all pages: {len(links)}")

#########################################
# Scraping all movies and stored in files
# NOTE: Execute the codes below will scrape more than 50000 movies scripts
########################### READ ABOW NOTES ###################################

try:
    for link in links:
        result = get_movie_transcripts(WEBSITE + link)
        title = result['title'].replace(':','-') # File name rules

        # Exporting data in a text file with the "title" name
        with open(f'3_Moviescripts\{title}.txt', 'w', encoding='utf-8') as file:
            file.write(result['transcript'])
except Exception as e:
    print(f"Error occur at {link}: {e}")
    