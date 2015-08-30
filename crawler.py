import requests
from bs4 import BeautifulSoup

linkq = list()
imgq = list()


def process_url(root, url):

    def clean(u):
        u = u.split('?')[0].rstrip('/')
        return u

    root = clean(root)

    if url == "/":
        return None
    elif url.startswith("http://"):
        return clean(url)
    elif url.startswith("/"):
        return root + url


def crawl(root="http://nextdrop.org", depth=3):
    print "crawling {0} at depth {1}".format(root, depth)

    response = requests.get(root)
    soup = BeautifulSoup(response.content)

    for img in soup.find_all('img', src=True):
        img_src = process_url(root, img['src'])

        if img_src and img_src not in imgq:
            imgq.append(img_src)

    if depth:
        for link in soup.find_all('a', href=True):
            new_root = process_url(root, link['href'])

            if new_root and new_root not in linkq:
                linkq.append(new_root)
                print "inner crawling {0} links at depth {1}".format(new_root, depth).rjust(50)
                crawl(new_root, depth - 1)
