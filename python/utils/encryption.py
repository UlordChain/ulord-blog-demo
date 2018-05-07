# coding=utf-8
# @File  : encryption.py
# @Author: PuJi
# @Date  : 2018/4/17 0017
import os, base64


from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random


utilspath = os.path.split(__file__)[0]
# utilspath = os.getcwd()
pubkeypath = os.path.join(utilspath, 'public.pem')
privkeypath = os.path.join(utilspath, 'private.pem')
RANDOM_GENERATOR=Random.new().read


# save random_generator
# with open(os.path.join(utilspath, 'random_generator'), 'wb') as target:
#     target.write(RANDOM_GENERATOR)


class RSAHelper(object):

    def __init__(self):
        if os.path.isfile(pubkeypath):
            with open(pubkeypath) as publickfile:
                p = publickfile.read()
                self.pubkeybytes = p
                self.pubkey = RSA.import_key(p)
            with open(privkeypath) as privatefile:
                p = privatefile.read()
                self.privkeybytes = p
                self.privkey = RSA.import_key(p)
        else:
            self.generate()

    def generate(self):
        self.key = RSA.generate(1024, RANDOM_GENERATOR)
        self.privkey = self.key.export_key()
        with open(privkeypath, 'wb') as pubfile:
            pubfile.write(self.privkey)

        self.pubkey = self.key.publickey().export_key()
        with open(pubkeypath, 'wb') as prifile:
            prifile.write(self.pubkey)
        return (self.pubkey, self.privkey)

    def load(self):
        with open(pubkeypath) as publickfile:
            p = publickfile.read()
            self.pubkey = RSA.import_key(p)
        with open(privkeypath) as privatefile:
            p = privatefile.read()
            self.privkey = RSA.import_key(p)

    def encry(self, pubkey, comment):
        cipher = PKCS1_v1_5.new(pubkey)
        return (cipher.encrypt(comment))

    def decrypt(self, prikey, message):
        cipher = PKCS1_v1_5.new(prikey)
        return (cipher.decrypt(base64.b64decode(message), RANDOM_GENERATOR))

    def test(self, prikey, message):
        cipher = PKCS1_v1_5.new(prikey)
        return (cipher.decrypt(message))


rsahelper = RSAHelper()


if __name__ == '__main__':
    message = rsahelper.encry(rsahelper.pubkey, "test")
    print(message)
    print(rsahelper.test(rsahelper.privkey, message))