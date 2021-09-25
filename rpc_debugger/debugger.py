import multiprocessing
import logging
from typing import Callable, Union
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class RPCDebugger(multiprocessing.Process):
    """
    What:
    Make target object a RPC process with XMLRPC server.
    Note some constraints from XMLRPC server/client:
    - object attributes will be flatten to dict
    - key of dict attributes must be str

    Why:
    Debug long running job memory leak or check object interactivly.

    How:
    >>> class Target:
    >>>     def __init__(self) -> None:
    >>>         self.a = []
    >>>         self.b = {"a": 1}
    >>>         self.c = (1,2,3,5)
    >>>         self.d = {"a": self.a}
    >>>     def m1(self):
    >>>         return 12
    # Inject debuger in the code
    >>> t = Target()
    >>> db = RPCDebugger(target=t, daemon=True)
    >>> db.start()

    On the client side:
    >>> import xmlrpc.client
    >>> s = xmlrpc.client.ServerProxy('http://localhost:8000')
    >>> s.a()
    >>> s.b()
    >>> s.c()
    >>> s.m1()
    """

    def __init__(self, target: object,
                 daemon: bool = True,
                 host: str = 'localhost',
                 port: int = 8000) -> None:
        super().__init__()
        self.daemon = daemon
        self.target = target
        self.host = host
        self.port = port
        self.server: Union[SimpleXMLRPCServer, None] = None

    def run(self):
        try:
            self.server = SimpleXMLRPCServer((self.host, self.port), requestHandler=RequestHandler)
            self.server.register_introspection_functions()
            self.server.register_instance(self.target, allow_dotted_names=True)
            self.register_attributes()
            self.server.serve_forever()
        except Exception:
            self.server.shutdown()

    def register_attributes(self):
        if '__dict__' in dir(self.target):
            for name, value in self.target.__dict__.items():
                print(f"Registering {name=} {type(value)=}")
                if isinstance(value, Callable):
                    self.server.register_function(value, name)
                else:
                    def _f(v=value):
                        return v
                    # lambda has a scope issue..
                    self.server.register_function(_f, name)
        else:
            logging.warning("Cannot find __dict__ in target. Failed to attach attributes. Only method is attached")