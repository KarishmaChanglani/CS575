class Server:
    def __init__(self, routing):
        self.routing = routing

    def run(self):
        self.routing.run(host="0.0.0.0", debug=True)
