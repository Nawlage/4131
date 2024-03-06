from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote_plus


def get_body_params(body):
    if not body:
        return {}
    parameters = body.split("&")

    # split each parameter into a (key, value) pair, and escape both
    def split_parameter(parameter):
        k, v = parameter.split("=", 1)
        k_escaped = unquote_plus(k)
        v_escaped = unquote_plus(v)
        return k_escaped, v_escaped

    body_dict = dict(map(split_parameter, parameters))
    print(f"Parsed parameters as: {body_dict}")
    # return a dictionary of the parameters
    return body_dict


def submission_to_table(item):
    """TODO: Takes a dictionary of form parameters and returns an HTML table row

    An example input dictionary might look like: 
    {
     'event': 'Sleep',
     'day': 'Sun',
     'start': '01:00',
     'end': '11:00', 
     'phone': '1234567890', 
     'location': 'Home',
     'extra': 'Have a nice dream', 
     'url': 'https://example.com'
    }
    """
    tableRow = "<tr>"
    for value in item.values():
        tableRow += f"<td>{value}</td>"

    tableRow += "</tr>"
    return tableRow

# NOTE: Please read the updated function carefully, as it has changed from the
# version in the previous homework. It has important information in comments
# which will help you complete this assignment.
def handle_req(url, body=None):
    """
    The url parameter is a *PARTIAL* URL of type string that contains the path
    name and query string.

    If you enter the following URL in your browser's address bar:
    `http://localhost:4131/MyForm.html?name=joe` then the `url` parameter will have
    the value "/MyForm.html?name=joe"

    This function should return two strings in a list or tuple. The first is the
    content to return, and the second is the content-type.
    """

    # Get rid of any query string parameters
    url, *_ = url.split("?", 1)
    # Parse any form parameters submitted via POST
    parameters = get_body_params(body)

    if url == "/MySchedule.html":
        return open("HTML/MySchedule.html").read(), "text/html"
    
    if url == "/MyForm.html":
        return open("HTML/MyForm.html").read(), "text/html"
    
    elif url == "/AboutMe.html":
        return open("HTML/AboutMe.html").read(), "text/html"
    
    elif url == "/stockQuotes.html":
        return open("HTML/stockQuotes.html").read(), "text/html"
    #images/gophers-mascot.png
    elif url == "/images/gophers-mascot.png":
        return open("images/gophers-mascot.png", "rb").read(), "image/png"
    # NOTE: These files may be different for your server, but we include them to
    # show you examples of how yours may look. You may need to change the paths
    # to match the files you want to serve. Before you do that, make sure you
    # understand what the code is doing, specifically with the MIME types and
    # opening some files in binary mode, i.e. `open(..., "br")`.
    elif url == "/CSS/style.css":
        return open("css/style.css").read(), "text/css"
    elif url == "/js/script.js":
        return open("js/script.js").read(), "text/javascript"
    elif url == "/js/stocks.js":
        return open("js/stocks.js").read(), "text/javascript"
    elif url == "/images/Zach.jpg":
        return open("images/Zach.jpg", "br").read(), "image/jpeg"
    elif url == "/images/Smith.png":
        return open("images/Smith.png", "br").read(), "image/png"
    elif url == "/images/Mayo.png":
        return open("images/Mayo.png", "br").read(), "image/png"
    elif url == "/images/keller.jpg":
        return open("images/keller.jpg", "br").read(), "image/jpeg"
    elif url == "/images/zoom.jpg":
        return open("images/zoom.jpg", "br").read(), "image/jpeg"
    elif url == "/images/Church.png":
        return open("images/Church.png", "br").read(), "image/png"
    elif url == "/images/freetime.jpg":
        return open("images/freetime.jpg", "br").read(), "image/jpeg"
    elif url == "/images/track.jpg":
        return open("images/track.jpg", "br").read(), "image/jpeg"
    
    # TODO: Add update the HTML below to match your other pages and
    # implement the `submission_to_table`.
    elif url == "/EventLog.html":
        
        return (
            """
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <title> Event Submission </title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
                <link rel="/CSS/stylesheet" href="style.css">
            </head>
            <body>
                <header>
                  <nav class="nav nav-pills flex-column flex-sm-row mb-2" >
                        <a class="flex-sm-fill text-sm-center nav-link" aria-current="page" href="MySchedule.html">My Schedule</a>
                        <a class="flex-sm-fill text-sm-center nav-link" href="AboutMe.html">About Me</a>
                        <a class="flex-sm-fill text-sm-center nav-link active" href="MyForm.html">Form Input</a>
                    </nav>
                </header>
                <div>
                    <h1> My New Events </h1>
                    
                </div>
                <div>
                    <table>
                        <thead>
                            <tr>
                                <th>Event</th>
                                <th>Day</th>
                                <th>Start</th>
                                <th>End</th>
                                <th>Phone</th>
                                <th>Location</th>
                                <th>Extra Info</th>
                                <th>URL</th>
                            </tr>
                        </thead>
                        <tbody>
                        """
            + submission_to_table(parameters)
            + """
                        </tbody>
                    </table>
                </div>
                <script src="/js/script.js"></script>
            </body>
            </html>""",
            "text/html; charset=utf-8",
        )
    else:
        return open("HTML/404.html").read(), "text/html; charset=utf-8"


# You shouldn't change content below this. It would be best if you just left it alone.


class RequestHandler(BaseHTTPRequestHandler):
    def __c_read_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        body = str(body, encoding="utf-8")
        return body

    def __c_send_response(self, message, response_code, headers):
        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # Send the first line of response.
        self.protocol_version = "HTTP/1.1"
        self.send_response(response_code)

        # Send headers (plus a few we'll handle for you)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", len(message))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)

    def do_GET(self):
        # Call the student-edited server code.
        message, content_type = handle_req(self.path)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        self.__c_send_response(
            message,
            200,
            {
                "Content-Type": content_type,
                "Content-Length": len(message),
                "X-Content-Type-Options": "nosniff",
            },
        )

    def do_POST(self):
        body = self.__c_read_body()
        message, content_type = handle_req(self.path, body)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        self.__c_send_response(
            message,
            200,
            {
                "Content-Type": content_type,
                "Content-Length": len(message),
                "X-Content-Type-Options": "nosniff",
            },
        )


def run():
    PORT = 4131
    print(f"Starting server http://localhost:{PORT}/")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()


run()
