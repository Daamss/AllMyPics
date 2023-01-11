import os
import requests
import urllib
import threading
from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup

# Enter the word you want to search
words = input('Enter the keywords you want to search, separated by commas: ').split(',')

# Create the media folder if it doesn't exist
if not os.path.exists('media'):
    os.makedirs('media')

# Create the links.txt file
f = open("links.txt", "a")

# Download all the images and gifs
def download_image(url):
    filename = 'media/image' + str(image_urls.index(url)) + '_' + word + '.jpg'
    urllib.request.urlretrieve(url, filename)
    f.write(url + "\n")
    print(url)

# Iterate through the keywords and make requests for each
for word in words:
    # Get the search results page
    url = "https://www.google.com/search?q=" + word + "&tbm=isch"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract all the image and gif urls
    images = soup.find_all('img')
    image_urls = []
    for image in images:
        if image['src'].startswith('/'):
            image_urls.append('https://www.google.com' + image['src'])
        else:
            image_urls.append(image['src'])

    # Use a thread pool to download the images in parallel
    pool = ThreadPool(10)
    results = pool.map(download_image, image_urls)

# Close the file
f.close()

print('Images, gifs and links have been downloaded and saved successfully!')