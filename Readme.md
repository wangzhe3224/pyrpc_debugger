# RPC debugger

![Tests](https://github.com/wangzhe3224/pyrpc_debugger/actions/workflows/tests.yml/badge.svg)

A RPC process that can be attached to any objects. After attach, a PRC process will open the attached object's 
 attributes and method. Note that attributes can only be access as function call in the client side ( :( a bit sad.

How to use:

```python
from rpc_debugger.debugger import RPCDebugger

class Target:
    def __init__(self) -> None:
        self.a = []
        self.b = {"a": 1}
        self.c = (1,2,3,5)
        self.d = {"a": self.a}
    def m1(self):
        return 12
t = Target()
db = RPCDebugger(target=t, daemon=True)
db.start()

import xmlrpc.client
s = xmlrpc.client.ServerProxy('http://localhost:8000')
s.a()
s.b()
s.c()
s.m1()
```