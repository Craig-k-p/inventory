from resources.utilities import Security
import json

s = Security()

data = {
	'containers': {},
	'things': {}
}
data = bytes(json.dumps(data).encode('utf-8'))
print(type(data))

s.encryptFile('TEST_ENCRYPT.inventory', data)

print(s.decryptFile('TEST_ENCRYPT.inventory'))