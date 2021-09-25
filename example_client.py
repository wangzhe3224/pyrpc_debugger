import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8000')

print(s.a())
print(s.b())

"""
Output: 
[]
{'a': 1}
"""