# coding=utf-8
# @File  : junior.py
# @Author: PuJi
# @Date  : 2018/5/14 0014

import os, time, requests, json, logging
from uuid import uuid1

from flask import request, g, jsonify

from ulordapi.manage import app, User
from ulordapi.errcode import return_result
from ulordapi.user import Junior


log = logging.getLogger('webServer')

junior = Junior(appkey="5d42b27e581c11e88b12f48e3889c8ab", secret="5d42b27f581c11e8bf63f48e3889c8ab")
# blog_config = {
#     'baseconfig':{
#         'config_file':'E:\ulord\ulord-blog-demo\config'
#     },
#     'logconfig':{
#         'log_file_path': "E:\ulord\ulord-blog-demo\junior.log"
#     }
# }
# junior.config_edit(blog_config)

junior.create_database('E:\ulord\ulord-blog-demo')


def auth_login_required():
    """
    check token

    :return: current user
    """
    head_token = request.headers.get('token')
    if not head_token:
        return {
            'errcode':60103,
            'reason': "需要token"
        }
    login_user = User.query.filter_by(token=head_token).first()
    if not login_user:
        return return_result(60104)
    if int(login_user.timestamp) < time.time():
        return return_result(60104)
    return login_user


@app.route('/user/password', methods=['GET', 'POST'])
def get_pubkey():
    """
    Get:generate publikey to fronted-end.Post:Check the message if crypted.

    :return: get-publickey/post-decrypted message
    """
    log.info("start get password")
    if request.method == 'GET':
        return jsonify(return_result(0, result={"pubkey":junior.rsahelper.pubkeybytes}))
    elif request.method == 'POST':
        message = request.json.get("password")
        return jsonify(return_result(0, result={'password': junior.get_purearg(message)}))


@app.route('/user/encrypt',methods=['POST'])
def encrypt():
    messages = request.json.get("messages")
    result = {}
    for message in messages:
        message = message.encode('utf-8')
        result.update({
            message:junior.rsahelper._encry(message)
        })
    return jsonify(result)


@app.route('/user/regist',methods=['POST'])
def regist():
    """
    user regist

    :return: user token
    """
    username = request.json.get('username')
    password = request.json.get('password')
    cellphone = request.json.get('cellphone')
    email = request.json.get('email')
    if username is None or password is None:
        # missing arguments
        return jsonify(return_result(60100))
    args = junior.decrypt([username, password, cellphone, email])
    if args:
        result = junior.user_regist(username=args[0],password=args[1],cellphone=args[2],email=args[3])
        return jsonify(result)
    else:
        return jsonify(return_result(60100))

@app.route('/user/activity', methods=['GET'])
def activity():
    """
    activity.Send 10 ulord to new user.
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    return jsonify(junior.user_activity(current_user.token))


@app.route('/user/login',methods=['POST'])
def login():
    """
    user login

    :return: user token
    """
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        # missing arguments
        return jsonify({
            'errcode': 60100,
            'reason': "缺少参数"
        })
    username = junior.decrypt(username)
    return jsonify(junior.user_login(username=username, password=password,encrypted=True))


@app.route('/user/logout',methods=['POST','GET'])
def logout():
    """
    user logout

    :return: success
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    return jsonify(junior.user_logout(current_user.token))


@app.route('/blog/publish',methods=['POST'])
def blog_publish():
    """
    publish blog

    :return: claim id,ulord-platform DB ID
    """
    current_user = auth_login_required() # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    title = request.json.get('title')
    body = request.json.get('body')
    amount = request.json.get('amount')
    tags = request.json.get('tag')
    description = request.json.get('description')
    body_hash = junior.udfs_upload([body])
    # print(body)
    # print(body_hash)
    if body_hash and body_hash.get(body):
        return jsonify(junior.resource_publish(title=title, udfshash=body_hash.get(body),amount=amount,tags=tags,des=description,
                                           usercondition={'usertoken':current_user.token}))
    else:
        return jsonify(return_result(errcode=60400))


@app.route('/blog/update',methods=['POST'])
def blog_update():
    """
    update blog

    :return: claim id,ulord-platform DB id
    """
    current_user = auth_login_required() # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    id = request.json.get('id')
    if id:
        try:
            id = str(id)
        except:
            return return_result(60100)
    pay_password = request.json.get('password')
    if not id and not pay_password:
        return  jsonify(return_result(60100))
    title = request.json.get('title')
    body = request.json.get('body')
    amount = request.json.get('amount')
    tags = request.json.get('tag')
    description = request.json.get('description')

    return jsonify(junior.resource_update(id=id, pay_password=pay_password,encrypted=True,title=title,body=body,price=amount,tags=tags,des=description))


@app.route('/blog/delete', methods=['POST'])
def blog_delete():
    """
    delete blog
    :return: errcode.You can query from the errcode dict.
    """
    current_user = auth_login_required() # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    id = request.json.get('id')
    password = request.json.get('password')
    if not id and not password:
        return return_result(60100)
    password = junior.decrypt(password)
    print(password)
    if not current_user.verify_password(password):
        return jsonify(return_result(60003))
    return jsonify(junior.delete(id, current_user.pay_password))


@app.route('/blog/all/list',methods=['POST'])
def blog_list():
    """
    list all blog

    :return: blog list
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    try:
        page = request.json.get('page')
        num = request.json.get('num')
    except:
        page = 1
        num = 10
    if not page:
        page = 1
    if not num:
        num = 10
    return jsonify(junior.queryresource(page, num))


@app.route('/blog/condition/id',methods=['POST'])
def blog_list_by_ID():
    """
    list blogs by ID

    :return: blog list
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    ids = request.json.get('ids')
    if not ids and not isinstance(ids, list):
        return jsonify(return_result())
    return jsonify(junior.query_resourc_by_ID(ids))


@app.route('/blog/isbought',methods=['POST'])
def check_bought():
    """
    check the resource if has been bought

    :return: if has bought return resource hash,if not existed return null,if hasn't bought return none.
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    claim_ids = request.json.get('claim_ids')
    if claim_ids is None:
        return jsonify({
            'errcode': 60100,
            'reason': '缺少参数'
        })
    # check if has bought
    return jsonify(junior.checkisbought(current_user.wallet, claim_ids))


@app.route('/blog/views',methods=['POST'])
def add_views():
    """
    add views according to the resource's title

    :return: current views
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    title = request.json.get('title')
    if title is None:
        return jsonify({
            'errcode': 60100,
            'reason': '缺少参数'
        })
    # add blog views
    return jsonify(junior.resouce_views(title))


@app.route('/pay/blogs',methods=['POST'])
def pay_blogs():
    """
    user pay blogs to view

    :return: blog hash
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    password = request.json.get('password')
    claim_id = request.json.get('claim_id')
    if password is None or claim_id is None:
        return jsonify({
            'errcode':60100,
            'reason':"缺少参数"
        })
    return jsonify(junior.pay_resources(current_user, claim_id, password, encrypted=True))


@app.route('/pay/ads',methods=['POST'])
def pay_ads():
    """
    get ulord from ads

    :return: ads hash
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    claim_id = request.json.get('claim_id')
    authorname = request.json.get('author')
    if claim_id is None or authorname is None:
        return jsonify({
            'errcode': 60100,
            'reason': "缺少参数"
        })
    return jsonify(junior.pay_ads(current_user.wallet, claim_id, authorname))


@app.route('/user/info',methods=['GET'])
def get_userinfo():
    """
    get user infor

    :return: dict.User information
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    return jsonify(junior.user_info_query(token=current_user.token))


@app.route('/user/balance',methods=['GET'])
def get_userbalance():
    """
    get user balance

    :return: user balance
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)

    return jsonify(junior.querybalance(payer=current_user.wallet, pay_password=current_user.pay_password))


@app.route('/user/published',methods=['POST'])
def get_userpublished():
    """
    get blog list the user has published
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    try:
        page = request.json.get('page')
        num = request.json.get('num')
        category = request.json.get('category')
    except:
        page = 1
        num = 10
    if not page:
        page = 1
    if not num:
        num = 10
    return jsonify(junior.queryuserpublished(current_user.wallet, page, num))


@app.route('/user/published/num',methods=['GET'])
def get_userpublishednum():
    """
    get the num of the blogs that user has published
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    return jsonify(junior.ulord_published_num(current_user.wallet))


@app.route('/user/billings',methods=['POST'])
def get_billings():
    """
    query user's billing
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    sdate = request.json.get('sdate')
    edate = request.json.get('edate')
    if not sdate or not edate:
        return jsonify(return_result(60100))
    return jsonify(junior.querybillings(current_user.wallet, sdate, edate))


@app.route('/user/billings/details',methods=['POST'])
def get_billingsdetail():
    """
    query user billing detail
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    try:
        page = request.json.get('page')
        num = request.json.get('num')
    except:
        page = 1
        num = 10
    if not page:
        page = 1
    if not num:
        num = 10
    return jsonify(junior.querybillingsdetail(current_user.wallet, page, num))


@app.route('/user/billings/income',methods=['POST'])
def get_incomebillings():
    """
    get user income billing information
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    try:
        page = request.json.get('page')
    except:
        page = 1
    try:
        num = request.json.get('num')
    except:
        num = 10
    try:
        category = request.json.get('category')
    except:
        category = 2
    sdate = request.json.get('sdate')
    edate = request.json.get('edate')
    if not page:
        page = 1
    if not num:
        num = 10
    if not category:
        category = 2
    if not sdate or not edate:
        return jsonify(return_result(60100))
    return jsonify(junior.queryincomebillings(current_user.wallet, sdate, edate, page, num, category=category))


@app.route('/user/billings/outgo',methods=['POST'])
def get_expensebillings():
    """
    get user expense billing information
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    try:
        page = request.json.get('page')
    except:
        page = 1
    try:
        num = request.json.get('num')
    except:
        num = 10
    try:
        category = request.json.get('category')
    except:
        category = 2
    sdate = request.json.get('sdate')
    edate = request.json.get('edate')
    if not page:
        page = 1
    if not num:
        num = 10
    if not category:
        category = 2
    if not sdate or not edate:
        return jsonify(return_result(60100))
    return jsonify(junior.queryoutgobillings(current_user.wallet, sdate, edate ,page, num, category=category))


@app.route('/user/modify',methods=['POST'])
def modify_userinfo():
    """
    Delete modify username.It will make publish error
    """
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    # change demand: cann't change username
    # username = request.json.get('username')
    password = request.json.get('password')
    cellphone = request.json.get('cellphone')
    email = request.json.get('email')
    new_password = request.json.get('new_password')
    if not password:
        # missing arguments
        return jsonify({
            'errcode': 60100,
            'reason': '缺少参数'
        })
    if cellphone:
        cellphone = junior.decrypt(cellphone)
    if email:
        email = junior.decrypt(email)
    return jsonify(junior.user_infor_modify(username=current_user.username, encrypted=True, password=password,cellphone=cellphone,email=email,new_password=new_password))


def start():
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop
    from flask_cors import CORS

    CORS(app, supports_credentials=True)
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()
    # app.run(host='0.0.0.0', port=5050)


if __name__ == '__main__':
    start()