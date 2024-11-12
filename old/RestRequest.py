from .Hub import Hub

class RestRequest:
    def __init__(self, hub: Hub, method: str, uriPath: str):
        self.hub: Hub = hub
        self.method: str = method
        self.uriPath: str = uriPath