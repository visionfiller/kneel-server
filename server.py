import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from urllib.parse import urlparse

from views import get_all_orders, get_single_order, create_order, delete_order, update_order
from repository import all, retrieve, create, update, retrieve_query


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def do_GET(self):
        """Handles GET requests to the server """
        response = None
        (resource, id, query_params) = self.parse_url(self.path)
        if id is not None:
            response = retrieve(resource,id)
            if response is not None:
                self._set_headers(200)
            
            else:
                self._set_headers(404)
                if resource == "orders":
                    response = { "message": "This order does not exist"}
                else:
                    response = { "message": "This item does not exist"}
        if id is not None and query_params is not None:
            self._set_headers(200)
            response = retrieve_query(resource,id, query_params)
        else :
            self._set_headers(200)
            response = all(resource)
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handles POST requests to the server """

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id, query_params) = self.parse_url(self.path)

        # Initialize new animal
        new_order = None
        if resource == "orders":
            if "sizeId" in post_body and "styleId" in post_body and "metalId" in post_body:
                self._set_headers(201)
                new_order = create(resource, post_body)
               
            else:
                self._set_headers(400)
                new_order = {"message": f'{"style is required" if "styleId" not in post_body else ""} {"metal is required" if "metalId" not in post_body else ""} {"size is required" if "sizeId" not in post_body else ""}'}
        else: 
            self._set_headers(400)
            new_order = {"message": "Cannot Add Selection"}
        # Encode the new animal and send in response
            self.wfile.write(json.dumps(new_order).encode())

    def do_DELETE(self):
        self._set_headers(405)
        (resource, id, query_params) = self.parse_url(self.path)
        response = {"message": "Cannot Delete Item"}

        self.wfile.write(json.dumps(response).encode())

    def do_PUT(self):
        response = None
        
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)

    # Delete a single animal from the list
        if resource == "metals":
            self._set_headers(204)
            response = update(id, post_body, resource)
        else:
            self._set_headers(405)
            response = {"message": "Cannot Modify Item"}
        self.wfile.write(json.dumps(response).encode())

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Replace existing function with this
    def parse_url(self, path):
        url_components = urlparse(path)
        path_params = url_components.path.strip("/").split("/")
        query_params = url_components.query.split("&")
        resource = path_params[0]
        id = None
        print(query_params)
        try:
            id = int(path_params[1])
        except IndexError:
            pass
        except ValueError:
            pass

        return (resource, id, query_params)  # This is a tuple
# This function is not inside the class. It is the starting
# point of this application.


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
