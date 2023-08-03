import http.client

def send_get_request(host, port, key):
    conn = http.client.HTTPConnection(host, port)
    path = f"/?key={key}"
    conn.request("GET", path)
    response = conn.getresponse()
    
    if response.status == 200:
        print(f"Key: {key}, Value: {response.read().decode()}")
    elif response.status == 404:
        print(f"Key: {key} not found.")
    elif response.status == 400:
        print("Missing 'key' parameter in the request.")
    else:
        print(f"Unexpected response: {response.status}, {response.reason}")

    conn.close()

if __name__ == "__main__":
    host = "localhost"
    port = 8000
    key = "apple"

    send_get_request(host, port, key)
