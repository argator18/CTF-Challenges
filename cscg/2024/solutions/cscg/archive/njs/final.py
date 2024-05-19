import requests
import tkinter as tk
from tkinter import filedialog
import sys
import random




def send_raw_post_request(url, data_bytes):
    """
    Send a raw POST request to the specified URL with the given byte data.

    Parameters:
    - url (str): The URL to which the POST request should be sent.
    - data_bytes (bytes): The byte data to be sent in the POST request.

    Returns:
    - response (requests.Response): The response from the server.
    """
    try:
        headers = {
            'Content-Type': 'application/octet-stream',
            'Accept': 'text/html; charset=utf-8'  # Explicitly setting Accept header
        }
        # Send a POST request to the URL with the raw byte data
        response = requests.post(url, data=data_bytes, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Success: Data posted successfully!")
        else:
            print(f"Failed to post data: Status code {response.status_code} - {response.text}")
        
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def random_bytes(num_bytes):
    return bytes([random.randint(0x80, 0xFF) for _ in range(num_bytes)])



# Example usage
if __name__ == "__main__":
    # URL to which the POST request will be sent
    post_url = "https://4fadd7cf68969a61be537735-1024-njs.challenge.cscg.live:1337//upload"
    content = random_bytes(4000)
    response = send_raw_post_request(post_url,content)

    if response:
        print(response.text)

