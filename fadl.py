#!/usr/bin/python3

# standard library
import argparse, os, sys, time
import http.cookiejar as cookielib

# third-party libs
import requests
from bs4 import BeautifulSoup 

def download(path: str) -> None:
    page_url = 'https://www.furaffinity.net{}'.format(path)
    response = session.get(page_url)
    s = BeautifulSoup(response.text, 'html.parser')

    # an FACDN link, e.g. //d.furaffinity.net/art/forneus/1674442755/1674442755.forneus_iris.jpg
    image = s.find(class_='download').find('a').attrs.get('href')
    assert image
    # submission-title has a `p` inside an `h2` so just .find() it tbh
    title = s.find(class_='submission-title').find('p').contents[0]
    assert title
    filename = image.split("/")[-1:][0] # e.g. 1674442755.forneus_iris.jpg, using the above FACDN link
    assert filename

    # the href has two leading slashes so let's just reuse them
    url = 'https:{}'.format(image)
    print(f"Downloading image from {url}")
    # TODO: allow output to not-this-folder
    filepath = os.path.join('.', filename)
    
    r = session.get(url, stream=True)
    if r.status_code != 200:
        # FA really likes to eat files with special characters in them, rendering only a thumbnail
        # for example: https://www.furaffinity.net/view/18051993/ (EXTREMELY NSFW, YOU HAVE BEEN WARNED)
        # has a functional thumbnail but the gallery image is broken
        # so we can't really safely just die here
        print(f"Received HTTP code {r.status_code} for {filepath}")
        return

    with open(filepath, 'wb') as f:
        f.write(r.content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--username', '-u', type=str, help='username of the furaffinity user')
    parser.add_argument('--cookies', '-c', type=str, help='a path to a Netscape cookie file (see README for more)')

    args = parser.parse_args()

    username = args.username
    if not username:
        print("Username is required, please pass -u/--username")
        sys.exit(1)

    print(f"Downloading the gallery of {username}")
    # shrug, a reasonably modern user agent is probably fine here, though maybe there's a scraper UA we can use?
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13.2; rv:111.0) Gecko/20100101 Firefox/111.0'

    session = requests.session()
    session.headers.update({'User-Agent': USER_AGENT})

    if args.cookies:
        cookies = cookielib.MozillaCookieJar(args.cookies)
        cookies.load()
        session.cookies = cookies

    # TODO: scraps, favs, etc, probably not hard
    gallery_url = f"https://www.furaffinity.net/gallery/{username}" 

    page = 1
    while True:
        page_url = f"{gallery_url}/{page}"
        response = session.get(page_url)
        s = BeautifulSoup(response.text, 'html.parser')

        if page == 1:
            if s.find(class_='loggedin_user_avatar'):
                acct = s.find(class_='loggedin_user_avatar').attrs.get('alt')
                print(f"Logged in as {acct}")
            else:
                print('Not logged in, cannot access adult content; see the README for authentication instructions')

        # every image in an FA gallery is in a `figure` tag so this part's actually easy enough
        for img in s.findAll('figure'):
            download(img.find('a').attrs.get('href'))
            time.sleep(0.2)

        next_button = s.find('button', class_='button standard', string="Next")
        if next_button is None or next_button.parent is None or s.find(id='no-images') is not None:
            print('Reached the end of the gallery')
            break

        page += 1
        print(f"Downloading page {page}")