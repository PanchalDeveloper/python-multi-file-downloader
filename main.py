import os, json, requests
from os import path
from urllib.parse import unquote
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor

# Directory for Output Data
download_data_dir = 'data'

data_urls = []

# Get Data Urls from database
with open(path.join('data_urls.json')) as f:
    data_urls = json.load(f)

download_errors = []

def download_image(url):
    # Get the image data from the url using requests.get method
    response = requests.get(url)
    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        # Get the image file name from the url by splitting it on "/" and taking the last element
        raw_file_name = url.split("/")[-1].replace(' ', '-')
        file_name = ''.join(letter for letter in raw_file_name if (letter.isalnum() or letter in ['.', '_', '-']))

        # Create directory for image (if doesn't exists)
        if not os.path.exists(download_data_dir):
            os.mkdir(download_data_dir)

        # Open a file with the same name as the image file name in binary mode
        with open(path.join(download_data_dir, unquote(file_name)), "wb") as f:
            # Write the image data to the file
            f.write(response.content)
            # Print a message indicating the download is complete
            print(f"Downloaded {file_name} from {url}")
    else:
        # Print a message indicating an error occurred
        print(f"Error downloading {url}: {response.status_code}")
        download_errors.append(url)

# Create a thread pool executor with 8 threads
with ThreadPoolExecutor(max_workers=8) as executor:
    # Submit each url to be downloaded concurrently
    running_futures = [executor.submit(download_image, url) for url in data_urls]

    futures.wait(running_futures)
    
    print('\n\n')

    if not len(download_errors):
        print('Downloading Completed Successfully.')
    else:
        print('Number of Errors Encountered While Downloding These Files: ', download_errors)