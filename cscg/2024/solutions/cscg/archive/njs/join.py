import requests
import sys
def send_join_request(url, endpoints):
    """
    Sends a POST request to the specified URL to join files from given endpoints.

    Parameters:
    - url (str): The URL to which the POST request should be sent.
    - endpoints (list of str): List of file paths (endpoints) to be joined.

    Returns:
    - response (requests.Response): The response from the server.
    """
    # Data to be sent in POST request
    payload = {
        "endpoints": endpoints
    }

    try:
        headers = {
            'Accept': 'text/html; charset=utf-8'  # Explicitly setting Accept header
        }

        # Send POST request with JSON payload
        response = requests.post(url, json=payload,headers = headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            #print("Success: Files joined successfully!")
            pass
        else:
            print(f"Failed to join files: Status code {response.status_code} - {response.text}")
        
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # URL to which the POST request will be sent (assuming localhost and port configured in Nginx)
    join_url = "https://4fadd7cf68969a61be537735-1024-njs.challenge.cscg.live:1337//join"
    
    files_to_join = ["0000000001","0000000001","0000000001","0000000001","0000000001","0000000001","0000000001","0000000001","0000000001","0000000001","0000000001","0000000001","0000000001","0000000001"]


    # Send the join request
    response = send_join_request(join_url, files_to_join)
    
    # Optionally print the response text
    if response:
        print(response.text)

