from typing import Dict
import requests
from wgsi import HOST_URL, HOST_PORT

# Host used is the same as the one in wgsi
HOST = 'http://' + HOST_URL + ":" + str(HOST_PORT)


def change(title: str, artist: str, timeout=0.1) -> Dict:
    """
    Change page title and artist
    :param title: the new title
    :param artist: the new artist
    :param timeout: set timeout for request
    :return: response in dict
    """
    url = HOST + '/change_text'
    data = {'title': title, 'artist': artist}
    response = requests.post(url, json=data, timeout=timeout)
    return response.json()


def timestamp(timestamp: str, timeout=0.1) -> Dict:
    """
    Change page timestamp
    :param timestamp: new timestamp
    :param timeout: request timeout
    :return: response in dict
    """
    url = HOST + '/change_timestamp'
    data = {"timestamp": timestamp}
    response = requests.post(url, json=data, timeout=timeout)
    return response.json()
