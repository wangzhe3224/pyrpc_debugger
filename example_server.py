from time import sleep
from rpc_debugger.debugger import RPCDebugger

class Target:
    def __init__(self) -> None:
        self.a = []
        self.b = {"a": 1}
        self.c = (1,2,3,5)
        self.d = {"a": self.a}
    def m1(self):
        return 12


if __name__ == "__main__":
    t = Target()
    db = RPCDebugger(target=t, daemon=False)
    db.start()
