import http.client
import sys

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
    if len(sys.argv)<3:
        print("Usage: python3 client.py <host:port> <key>")
        exit(0)
    try:
        host,port = sys.argv[1].split(":")
    except:
        print("Invalid host:port format")
        exit(0)
    key = sys.argv[2]

    send_get_request(host, port, key)
