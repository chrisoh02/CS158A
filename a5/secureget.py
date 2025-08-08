import socket
import ssl
import certifi

hostname = 'www.google.com'
port = 443
context = ssl.create_default_context(cafile=certifi.where())

# connect and wrap in ssl
with socket.create_connection((hostname, port)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        # sent http get request
        request = f"GET / HELP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n"
        ssock.sendall(request.encode('utf-8'))

        # receive response
        response = b""
        while True:
            data = ssock.recv(4096)
            if not data:
                break
            response += data


# save to file
with open('response.html', 'wb') as f:
    f.write(response)

print("done")