# coding=utf-8
# @File  : encryption.py
# @Author: PuJi
# @Date  : 2018/4/17 0017

import rsa, os, sys

utilspath = os.path.split(__file__)[0]
# utilspath = os.getcwd()
pubkeypath = os.path.join(utilspath, 'public.pem')
privkeypath = os.path.join(utilspath, 'private.pem')
# pubkeypath = baseconfig.pubkeypath
# privkeypath = baseconfig.privkeypath


class RSAHelper(object):

    def __init__(self):
        if os.path.isfile(pubkeypath):
            with open(pubkeypath) as publickfile:
                p = publickfile.read()
                self.pubkeybytes = p
                self.pubkey = rsa.PublicKey.load_pkcs1(p)
            with open(privkeypath) as privatefile:
                p = privatefile.read()
                self.privkeybytes = p
                self.privkey = rsa.PrivateKey.load_pkcs1(p)
        else:
            (self.pubkey, self.privkey) = self.generate()

    def generate(self):
        (self.pubkey, self.privkey) = rsa.newkeys(1024)
        pub = self.pubkey.save_pkcs1()
        with open(pubkeypath, 'w+') as pubfile:
            pubfile.write(pub)
        pri = self.privkey.save_pkcs1()
        with open(privkeypath, 'w+') as prifile:
            prifile.write(pri)
        return (self.pubkey, self.privkey)

    def load(self):
        with open(pubkeypath) as publickfile:
            p = publickfile.read()
            self.pubkey = rsa.PublicKey.load_pkcs1(p)
        with open(privkeypath) as privatefile:
            p = privatefile.read()
            self.privkey = rsa.PrivateKey.load_pkcs1(p)

    def loads(self):
        with open(pubkeypath) as publickfile:
            p = publickfile.read()
            self.pubkeybytes = p
        with open(privkeypath) as privatefile:
            p = privatefile.read()
            self.privkeybytes = p

    def encry(self, pubkey, comment):
        return rsa.encrypt(comment, pubkey)

    def decrypt(self, prikey, message):
        return rsa.decrypt(message, prikey)


rsahelper = RSAHelper()


if __name__ == '__main__':
    test = RSAHelper()
    print(test.load())
    message = test.encry(test.pubkey, "123")
    print(message)
    password = test.decrypt(test.privkey, message)
    print(password)