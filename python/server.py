# coding=utf-8
# @File  : server.py
# @Author: PuJi
# @Date  : 2018/4/10 0010

import os, time, requests
from uuid import uuid1

from flask import request, g, jsonify

from DBhelper.manage import app, db, User, Blog, Billing, Tag
from utils.Ulord import ulord_transmitter, ulord_helper
from utils import FileHelper
from config import baseconfig
from utils.Checker import checker

# app.config.from_object(DevConfig)


def auth_login_required():
    head_token = request.headers.get('token')
    if not head_token:
        return {
            'result':0,
            'msg': "need token"
        }
    login_user = User.query.filter_by(token=head_token).first()
    if not login_user:
        return {
            'result':0,
            'msg':"invalid token"
        }
    if int(login_user.timestamp) < time.time():
        return {
            'result': 0,
            'msg': "invalid token"
        }
    return login_user


@app.route('/user/regist',methods=['POST'])
def regist():
    username = request.json.get('username')
    password = request.json.get('password')
    cellphone = request.json.get('cellphone')
    email = request.json.get('email')
    if username is None or password is None:
        # missing arguments
        return jsonify({
            'result': 0,
            'msg': "missing arguments"
        })
    if User.query.filter_by(username=username).first() is not None:
        # existing user
        return jsonify({
            'result':0,
            'msg':"existing user"
        })
    # check cellphone and email
    if cellphone:
        if not checker.isCellphone(cellphone):
            return jsonify({
                'result': 0,
                'msg': 'error cellphone'
            })
    if email:
        if not checker.isMail(email):
            return jsonify({
                'result': 0,
                'msg': 'error email'
            })
    # user get wallet and password (or not) from ulord platform
    user = User(username=username)
    if ulord_helper.regist(username, password) & ulord_helper.paytouser(username):
        user.hash_password(password)
        if cellphone:
            user.cellphone = cellphone
        if email:
            user.email = email
        if baseconfig.activity:
            user.balance = baseconfig.amount
        user.wallet = username
        user.pay_password = user.password_hash
    else:
        return jsonify({
            'result': 0,
            'msg': "error create ulord wallet"
        })
    token = str(uuid1())
    user.token = token
    user.timestamp = int(time.time()) + 24 * 60 * 60
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'result': 1,
        'msg': token
    })


@app.route('/user/login',methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        # missing arguments
        return jsonify({
            'result': 0,
            'msg': "missing arguments"
        })
    login_user = User.query.filter_by(username=username).first()
    if not login_user:
        # no user
        return jsonify({
            'result':0,
            'msg': "error user"
        })
    if not login_user.verify_password(password):
        # error password
        return jsonify({
            'result': 0,
            'msg': "error password"
        })
    token = str(uuid1())
    login_user.token = token
    login_user.timestamp = int(time.time()) + 24 * 60 * 60
    db.session.commit()
    return jsonify({
        'result':1,
        'msg': token
    })


@app.route('/blog/publish',methods=['POST'])
def blog_publish():
    current_user = auth_login_required() # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    title = request.json.get('title')
    body = request.json.get('body')
    amount = request.json.get('amount')
    tags = request.json.get('tag')
    description = request.json.get('description')
    if title is None or body is None or amount is None:
        # missing arguments
        return jsonify({
            'result': 0,
            'msg':"missing arguments"
        })
    if Blog.query.filter_by(title=title, userid=current_user.id).first() is not None:
        # existing title
        return jsonify({
            'result': 0,
            'msg': "existing title"
        })
    if current_user.balance < 1:
        # less balance
        return jsonify({
            'result': 0,
            'msg': "Insufficient amount"
        })
    # TODO upload body to IPFS
    try:
        body_txt = os.path.join(os.path.join(os.getcwd(), 'blogs'), '{}.txt'.format(title))
    except:
        print("Doesn't support chinese.Using uuid")
        body_txt = os.path.join(os.path.join(os.getcwd(), 'blogs'), '{}.txt'.format(str(uuid1())))
    if FileHelper.saveFile(body_txt, body):
        file_hash = ulord_transmitter.upload(body_txt)
        try:
            os.remove(body_txt)
        except:
            print("Error rm {}".format(body_txt))

        # TODO publish
        # init data schema
        data = ulord_helper.ulord_publish_data
        data['author'] = current_user.username
        data['title'] = title
        data['tag'] = tags
        data['ipfs_hash'] = file_hash
        data['price'] = amount
        data['pay_password'] = current_user.pay_password
        data['description'] = description
        claimID = ulord_helper.publish(data)
        if claimID:
            # cost balance
            current_user.balance -= 1
            # save blog to local DB
            new_blog = Blog(id=str(uuid1()), title=title, amount=amount, views=0)
            if tags:
                for tag in tags:
                    if Tag.query.filter_by(tagname=tag).first() is None:
                        new_blog.tags.append(Tag(tag))
            if description:
                new_blog.description = description
            new_blog.body = file_hash
            new_blog.date = int(time.time())
            new_blog.userid = current_user.id
            new_blog.claimID = claimID
            db.session.add(new_blog)
            db.session.commit()
            return jsonify({
                'result': 1,
                'msg': 'None'
            })
        else:
            return jsonify({
                'result': 0,
                'msg': "error publish to the UlordPlatform"
            })
    else:
        return jsonify({
            'result': 0,
            'msg': "save file failed"
        })


@app.route('/blog/all/list',methods=['POST'])
def blog_list():
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    result = ulord_helper.queryblog(1)
    msg = result.get('result')
    return jsonify({
        'result': 1,
        'msg':msg
    })


# @app.route('/blog/record',methods=['POST'])
# def blog_record():
#     current_user = auth_login_required()  # check token
#     if type(current_user) is dict:
#         return jsonify(current_user)
#     try:
#         blog_ID = request.json.get('blog_ID')
#     except:
#         return jsonify({
#             "result": 0,
#             "msg": "need blog id"
#         })
#     if not blog_ID:
#         return jsonify({
#             "result": 0,
#             "msg": "need blog id"
#         })
#     current_blog = Blog.query.filter_by(id=blog_ID).first()
#     if not current_blog.views:
#         current_blog.views = 0
#     current_blog.views += 1
#     return jsonify({
#         'result': 1,
#         'msg':'None'
#     })


@app.route('/blog/isbought',methods=['POST'])
def check_bought():
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    claim_id = request.json.get('claim_id')
    if claim_id is None:
        result = 0
        msg = "missing arguments"
        return jsonify({
            'result':result,
            'msg':msg
        })
    # check if has bought
    result = ulord_helper.checkisbought(current_user.wallet, claim_id)
    return jsonify({
        'result': 1,
        'msg': result
    })


@app.route('/pay',methods=['POST'])
def pay():
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    password = request.json.get('password')
    title = request.json.get('title')
    amount = request.json.get('amount')
    auth = request.json.get('auth')
    if password is None or title is None or amount is None or auth is None:
        result = 0
        msg = "missing arguments"
        return jsonify({
            'result':result,
            'msg':msg
        })
    # 支付
    if current_user.balance < float(amount):
        return jsonify({
            'result': 0,
            'msg': "Insufficient amount"
        })
    if not current_user.verify_password(password):
        return jsonify({
            'result': 0,
            'msg': 'error password'
        })
    # hash值
    # TODO union query
    payee = User.query.filter_by(username=auth).first()
    current_blog = Blog.query.filter_by(title=title, userid=payee.id).first()
    # if True:
    if ulord_helper.transaction(current_user.wallet, current_blog.claimID, current_user.pay_password):

        current_user.balance -= current_blog.amount
        # write billing record
        billing = Billing(payer=current_user.id, amount=float(amount), payee=current_blog.userid, titleid=current_blog.id)
        # write read record
        current_user.reads.append(current_blog)
        # write payee balance

        payee.balance -= current_blog.amount
        db.session.add(billing)
        # db.session.add(current_user)
        db.session.commit()
        return jsonify({
            'result': 1,
            'msg': current_blog.body
        })
    else:
        return jsonify({
            'result': 0,
            'msg': "pay failed!"
        })


@app.route('/user/info',methods=['GET'])
def get_userinfo():
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    msg = {
    	"username": current_user.username,
    	"cellphone": current_user.cellphone,
    	"Email": current_user.email
    }
    return jsonify({
        'result':1,
        'msg':msg
    })


@app.route('/user/balance',methods=['GET'])
def get_userbalance():
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    billing_details = []
    #   [
    #     "billing1_id": {},
    #     "billing2_id": {}
    #   ]
    # TODO query payee is user
    billing_temp_details = Billing.query.filter_by(payer=current_user.id).all()
    for billing_temp_detail in billing_temp_details:
        payee = User.query.filter_by(id=billing_temp_detail.payee).first()
        blog = Blog.query.filter_by(id=billing_temp_detail.titleid).first()
        blog = {
            "billing_id": billing_temp_detail.id,
            "amount": billing_temp_detail.amount,
            "payee": payee.username,
            "title": blog.title
        }
        billing_details.append(blog)
    balance = ulord_helper.querybalance(current_user.wallet, current_user.pay_password)
    msg = {
    	"username": current_user.username,
    	"cellphone": current_user.cellphone,
    	"Email": current_user.email,
    	"balance": balance
    }
    return jsonify({
        'result':1,
        'msg':msg
    })


@app.route('/user/published',methods=['POST'])
def get_userpublished():
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    page = request.json().get('page')
    num = request.json().get('num')
    msg = ulord_helper.ulord_userpublished(current_user.wallet)

    return jsonify({
        'result':1,
        'msg':msg
    })


@app.route('/user/info',methods=['POST'])
def get_userbought():
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    page = request.json().get('page')
    num = request.json().get('num')
    msg = ulord_helper.ulord_userbought(current_user.wallet)

    return jsonify({
        'result':1,
        'msg':msg
    })


@app.route('/user/modify',methods=['GET'])
def modify_userinfo():
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    username = request.json.get('username')
    password = request.json.get('password')
    cellphone = request.json.get('cellphone')
    email = request.json.get('email')
    new_password = request.json.get('new_password')
    if not password:
        # missing arguments
        return jsonify({
            'result': 0,
            'msg': 'missing arguments'
        })
    # check cellphone and email
    if cellphone:
        if not checker.isCellphone(cellphone):
            return jsonify({
                'result': 0,
                'msg': 'error cellphone'
            })
    if email:
        if not checker.isMail(email):
            return jsonify({
                'result': 0,
                'msg': 'error email'
            })
    if username:
        if User.query.filter_by(username=username).first() is not None:
            # existing user
            return jsonify({
                'result': 0,
                'msg': "existing user"
            })
        current_user.username = username
    if new_password:
        current_user.hash_password(new_password)
    if cellphone:
        current_user.cellphone = cellphone
    if email:
        current_user.email = email
    if db.session.commit():
        return jsonify({
            'result': 1,
            'msg': "Success"
        })
    else:
        return jsonify({
            'result': 0,
            'msg': "Fail, try again."
        })


@app.route('/blog/modify',methods=['POST'])
def modify_blog():
    current_user = auth_login_required()  # check token
    if type(current_user) is dict:
        return jsonify(current_user)
    title = request.json.get('title')
    body = request.json.get('body')
    amount = request.json.get('amount')
    tags = request.json.get('tag')
    description = request.json.get('description')
    if title is None:
        # missing arguments
        result = 0
        msg = "missing arguments"
        return jsonify({
            'result': result,
            'msg': msg
        })
    current_blog = Blog.query.filter_by(title=title, userid= current_user.id)
    if body:
        blog_txt = os.path.join(os.path.join(os.getcwd(), 'blogs'), '{0}_{1}.txt'.format(title, str(uuid1())))
        FileHelper.saveFile(blog_txt, body)
        current_blog.body = ulord_transmitter.upload(blog_txt)
    if amount:
        current_blog.amount = amount
    if tags:
        current_blog.tag = tags
    if description:
        current_blog.description = description

    db.session.add(current_blog)
    # TODO publish
    # init data schema
    data = ulord_helper.ulord_publish_data
    data['author'] = current_user.username
    data['title'] = current_blog.title
    data['tag'] = current_blog.tag
    data['ipfs_hash'] = current_blog.body
    data['price'] = current_blog.amount
    data['pay_password'] = current_user.pay_password
    data['description'] = current_blog.description
    current_blog.claimID = ulord_helper.publish(data)
    if current_blog.claimID:
        db.session.commit()
        return jsonify({
            'result': 1,
            'msg': 'None'
        })
    else:
        return jsonify({
            'result': 0,
            'msg': "error publish to the UlordPlatform"
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0')