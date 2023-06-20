#!/home/username/virtualenv/application/x.y/bin/python

activate_this = "/home/username/virtualenv/application/x.y/bin/activate_this.py"
with open(activate_this) as f:
        code = compile(f.read(), activate_this, 'exec')
        exec(code, dict(__file__=activate_this))

import sys
from module import variable

print ("Content-type:text/html\r\n\r\n")
print ('<html>')
print ('<head>')
print ('<title>Virtualenv test</title>')
print ('</head>')
print ('<body>')
print ('<h3>If you see this, the module import was successful</h3>')
print (sys.version)
print ('</body>')
print ('</html>')