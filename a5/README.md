Assignment:

Learn how to create a socket with SSL (Secure Sockets Layer). You will write a script that establishes a secure connection to a server, sends an HTTP request, and processes the server’s response.

Tasks
You are required to implement a Python program (named secureget.py) that:

Uses the ssl module along with socket to create a secure (SSL-wrapped) TCP connectionLinks to an external site..
Connects to www.google.com on port 443 (HTTPS).
Sends a well-formed HTTP GET request for the root path (/).
Receives the HTTP response from the server.
Saves the complete HTML content of the response to a file named response.html.
