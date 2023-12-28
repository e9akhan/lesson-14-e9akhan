"""
    Module name :- extract
    Method(s) :- get_requests(url), fetch_links(text), fetch_websites(links),
    get_status_code(url), get_website_and_status(url), main(url, size)
"""

import random
import requests


def get_requests(url):
    """
    Make a get request to the specified url.

    Return
        Response object's text.
    """
    response = requests.get(url=url, timeout=10)
    return response.text


def fetch_links(text):
    """
    Finding the links in the response object's text.

    Return
        Links available in reponse object's text.
    """
    weblist = [
        website for website in text.split() if "http:" in website or "https:" in website
    ]
    links = [
        link[link.index('"http') + 1 : link.index('"', link.index('"http') + 1)]
        for link in weblist
    ]
    return links


def get_status_code(url):
    """
    Find the status code of the specified url.

    Return
        Status code of the specified url.
    """
    response = requests.get(url=url, timeout=10)
    return response.status_code


def get_website_and_status(url):
    """
    Adding the website in the dictionary as per their status code.

    Return
        Dictionary containing status code as keys and list of website as
        values.
    """
    status_website = {}

    text = get_requests(url=url)
    websites = fetch_links(text=text)

    for website in websites:
        status = get_status_code(website)
        if status in status_website:
            status_website[status] += [website]
        else:
            status_website[status] = [website]

    return status_website


def main(url, size):
    """
    Returning the dictionary containing status code as key and
    list of websites of size(size) sampled.

    Return
        Dictionary containing status code as key and
        list of websites of size(size)
    """
    status_website = get_website_and_status(url=url)
    resultant = {}

    for status, website in status_website.items():
        if len(website) > size:
            resultant[status] = random.sample(website, k=size)
        else:
            resultant[status] = random.sample(website, k=len(website))

    return resultant


if __name__ == "__main__":
    URL = "https://httpbin.org/"
    print(main(URL, 5))
