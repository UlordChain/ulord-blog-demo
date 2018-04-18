# coding=utf-8
# @File  : ipfs_module.py
# @Author: PuJi
# @Date  : 2018/4/10 0010
import os, time, json, logging, sys

import ipfsapi, requests

import FileHelper

sys.path.append('../')
from config import baseconfig


class UlordTransmitter():
    # download and upload files from Ulord
    def __init__(self, host='127.0.0.1', port='5001'):
        self.ipfs_host = host
        self.ipfs_port = port
        self.connect = ipfsapi.connect(self.ipfs_host, self.ipfs_port)
        self.log = ""
        self.chunks = {}
        self.objects = None
        self.links = []
        self.downloadpath = os.path.join(FileHelper.getRootPath(), 'download')

    def update(self, host='127.0.0.1', port='5001'):
        self.ipfs_host = host
        self.ipfs_port = port
        self.connect = ipfsapi.connect(self.ipfs_host, self.ipfs_port)
        self.log = ""
        self.chunks = {}
        self.objects = None
        self.links = []

    def upload_stream(self, stream):
        # TODO need fix
        try:
            start = time.time()
            result = self.connect.add(stream)
            end = time.time()
            print('upload stream cost:{}'.format(end - start))
            return result.get('Hash')
        except Exception, e:
            logging.error("Failed upload.{}".format(e))
            return None

    def upload(self, local_file):
        try:
            start = time.time()
            result = self.connect.add(local_file)
            end = time.time()
            print('upload {0} ,size is {1}, cost:{2}'.format(local_file, FileHelper.getSize(local_file), (end - start)))
            # TODO save filename in DB
            return result.get('Hash')
        except Exception, e:
            # TODO save e in the log
            return None

    def list(self, filehash):
        try:
            self.objects = self.connect.ls(filehash).get('Objects')
            if self.objects:
                for object in self.objects:
                    if 'Links' in object.keys():
                        for link in object.get('Links'):
                            self.links.append(link)
            else:
                self.links = "test"
        except Exception, e:
            logging.error("ls fail:{}".format(e))

    def downloadfile(self, localfile):
        # TODO query the file hash from DB
        pass

    def downloadhash(self, filehash, filepath=None):
        try:
            start = time.time()
            self.connect.get(filehash, filepath=filepath)
            end = time.time()
            print('download {0} cost:{1}'.format(filehash, (end - start)))
            print("download {} successfully!".format(filehash))
            return True
        except Exception, e:
            logging.error("download fail:{}".format(e))
            return False

    def resumableDownload(self, filehash, filename=None):
        # not thread safely.single thread
        filehash_path = os.path.join(self.downloadpath, filehash)
        tempjson = os.path.join(filehash_path, 'temp.json')
        if not os.path.isfile(tempjson):
            # save chunks result into the temp.json
            self.list(filehash)
            if self.links:
                i = 0
                for link in self.links:
                    if 'Hash' in link.keys():
                        self.chunks.update({
                            i: {
                                'filehash': link.get('Hash'),
                                'success': False
                            }
                        })
                    i += 1
                FileHelper.saveFile(tempjson, json.dumps(self.chunks))
            else:
                print("no chunks.Error get the {} chunks result".format(filehash))
        # download chunk
        with open(tempjson) as target_file:
            self.chunks = json.load(target_file)
        if self.chunks:
            for chunk, chunk_result in self.chunks.iteritems():
                if not chunk_result.get('success'):
                    chunk_result['success'] = self.downloadhash(chunk_result.get('filehash'), filehash_path) or chunk_result.get('success')
                    FileHelper.saveFile(tempjson, json.dumps(self.chunks))
            # merge chunks
            if filename:
                localfile = os.path.join(filehash_path, filename)
            else:
                localfile = os.path.join(filehash_path, filehash)
            with open(localfile, 'wb') as target_file:
                for i in range(len(self.chunks)):
                    chunk = os.path.join(filehash_path, self.chunks.get(str(i)).get('filehash'))
                    with open(chunk, 'rb') as source_file:
                        for line in source_file:
                            target_file.write(line)
                    try:
                        os.remove(chunk)  # 删除该分片，节约空间
                    except Exception, e:
                        print("{0}:{1} remove failed:{2}".format(chunk, os.path.isfile(chunk), e))
                try:
                    os.remove(tempjson)
                except Exception, e:
                    print("{0}:{1} remove failed:{2}".format(tempjson, os.path.isfile(tempjson), e))


class UlordHelper(object):
    # a helper to help request the ulord paltform
    def __init__(self):
        self.ulord_url = baseconfig.ulord_url
        self.ulord_head = baseconfig.ulord_head

        self.ulord_regist = baseconfig.ulord_url + baseconfig.ulord_regist # ulord regist webURL
        self.ulord_paytouser = baseconfig.ulord_url + baseconfig.ulord_paytouser # ulord transfer webURL

        self.ulord_publish = baseconfig.ulord_url + baseconfig.ulord_publish  # ulord publish webURL
        self.ulord_publish_data = baseconfig.ulord_publish_data  # ulord publish data

        self.ulord_queryblog = baseconfig.ulord_url + baseconfig.ulord_queryblog # query blog list webURL
        self.ulord_checkbought = baseconfig.ulord_url + baseconfig.ulord_checkbought # query if the blog has bought
        self.ulord_transaction = baseconfig.ulord_url + baseconfig.ulord_transaction  # ulord transaction webURL

        self.ulord_querybalance = baseconfig.ulord_url + baseconfig.ulord_querybalance  # qurey balance webURL
        self.ulord_userbought = baseconfig.ulord_url + baseconfig.ulord_userbought # query the blog that user has bought
        self.ulord_userpublished = baseconfig.ulord_url + baseconfig.ulord_userpublished # query the blog that user has published
        # TODO ulord other URL

    def post(self, url, data):
        print(url)
        print(data)
        r = requests.post(url=url, json=data, headers=self.ulord_head)
        print(r.status_code)
        if r.status_code == requests.codes.ok:
            print(r.json())
            return r.json()
        else:
            return {
                "errcode": 50000,
                "reason": "调用API网络错误"
            }

    def put(self, url):
        r = requests.get(url=url, headers=self.ulord_head)
        print(url)
        print(r.status_code)
        if (r.status_code == requests.codes.ok):
            print(r.json())
            return r.json()
        else:
            return {
                "errcode": 50000,
                "reason": "调用API网络错误"
            }

    def regist(self, username, password):
        # regist wallet address from the ulord platform
        data = {
            "username": username,
            "pay_password": password
        }
        return self.post(self.ulord_regist, data)

    def publish(self, data):
        # publish data to the ulord platform
        return self.post(self.ulord_publish, data)

    def transaction(self, payer, claim_id, pay_password):
        # record the transaction to the ulord platform
        data = {
            'username': payer,
            'claim_id': claim_id,
            'pay_password':pay_password
        }
        return self.post(self.ulord_transaction, data)

    def paytouser(self, username):
        # activity send some ulords to the user
        if baseconfig.activity:
            data = {
                'is_developer': True,
                'recv_user': username,
                'amount': baseconfig.amount
            }
            return self.post(self.ulord_paytouser, data)
        else:
            return {
                "errcode": 51000,
                "reason": "活动取消"
            }

    def queryblog(self, page=1, num=10):
        # query the blog list from the ulord platform.method is get
        temp_url = self.ulord_queryblog + "{0}/{1}/".format(page, num)
        return self.put(temp_url)

    def querybalance(self, payer, pay_password):
        # query the personal balance from the ulord platform
        data = {
            'username': payer,
            'pay_password':pay_password
        }
        return self.post(self.ulord_querybalance, data)

    def checkisbought(self, payer, claim_ids):
        # query the personal balance from the ulord platform
        data = {
            'username': payer,
            'claim_ids': claim_ids
        }
        return self.post(self.ulord_checkbought, data)

    def queryuserpublished(self, wallet_username, page=1, num=10):
        # query user published from ulort platform
        data = {
            'author': wallet_username,
        }
        temp_url = self.ulord_userpublished + "{0}/{1}/".format(page, num)
        return self.post(temp_url, data)

    def queryuserbought(self, wallet_username, page=1, num=10):
        # query user published from ulort platform
        data = {
            'customer': wallet_username,
        }
        temp_url = self.ulord_userbought + "{0}/{1}/".format(page, num)
        return self.post(temp_url, data)


ulord_transmitter = UlordTransmitter()


ulord_helper = UlordHelper()


if __name__ == '__main__':
    # localhost
    # ipfs_host = '127.0.0.1'
    # ipfs_port = '5001'
    #
    # ulord_transmitter = UlordTransmitter(ipfs_host, ipfs_port)
    # test_file = 'E:\ipfs\go-ipfs_v0.4.14_linux-amd64.tar.gz'
    # with open(test_file, 'rb') as target_file:
    #     result = ulord_transmitter.upload_stream(target_file)
    #     print(result)

    #ulord_test
    data = {
        'author': 'Test',
        'title': "test333",
        'tag': ['test','IPFS'],
        'ipfs_hash': 'QmXZ9dNRpkvP4eHDuqJsG7jZYVfuz7aKqTyuJjDicbnEet',
        'price': 0.2,
        'content_type': '.txt',
        'pay_password': None,
        'description': "this is a test"
    }

    # ulord_helper.regist('Test2', '123')
    ulord_helper.credit()
    ulord_helper.publish(data)
    ulord_helper.transaction('Test','', '123')