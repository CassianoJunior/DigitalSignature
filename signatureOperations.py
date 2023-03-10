import os
from base64 import b64decode, b64encode
from datetime import datetime

from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme


def assign(message, key, hash):
  hashObject = hash[0].new(message)
  hashHexadecimal = hashObject.hexdigest().encode('UTF-8')

  hashOfHashHex = hash[0].new(hashHexadecimal)
  digitalSignature = PKCS115_SigScheme(key).sign(hashOfHashHex)

  now = datetime.now().strftime("%Y%m%d%H%M%S")

  if not os.path.exists('signatures'): os.mkdir('signatures')

  os.mkdir(f'signatures/signature_{now}')
  
  with open(f'signatures/signature_{now}/signature.base64', 'wb') as file:
    file.write(b64encode(digitalSignature))
    file.close()
  
  with open(f'signatures/signature_{now}/publicKey.base64', 'wb') as file:
    file.write(b64encode(key.publickey().export_key('PEM')))
    file.close()
  
  with open(f'signatures/signature_{now}/USED_SHA.txt', 'w') as file:
    file.write(hash[1])

  return b64encode(digitalSignature), b64encode(key.publickey().export_key('PEM'))

def verify(message, digitalSignature, key, hash):
  hashObject = hash.new(message)
  hashHexadecimal = hashObject.hexdigest().encode('UTF-8')

  hashOfHashHex = hash.new(hashHexadecimal)
  digitalSignature = b64decode(digitalSignature)
  key = RSA.import_key(b64decode(key))
  verifier = PKCS115_SigScheme(key)

  try:
    verifier.verify(hashOfHashHex, digitalSignature)
    return True
  except:
    return False