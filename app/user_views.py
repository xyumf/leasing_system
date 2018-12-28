import re
from flask import Blueprint, request, render_template, jsonify, url_for, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import random
from app.models import db, User

user_blue = Blueprint('user', __name__)


@user_blue.route('/create/')
def create():
    db.create_all()
    return '创建成功'


@user_blue.route('/register/',methods=['GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')


@user_blue.route('/register/',methods=['POST'])
def register2():
    if request.method == 'POST':
        phone = request.form.get('mobile')
        imagecode = request.form.get('imagecode')
        # phonecode = request.form.get('phonecode')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        imagecode2 = request.form.get('imagecode2')
        user = User.query.filter(User.phone == phone).first()
        if user:
            return jsonify({'code':10001, 'msg': '该手机号码已经注册'})
        if not imagecode == imagecode2:
            return jsonify({'code':10000, 'msg': '验证码错误'})
        if not password == password2:
            return jsonify({'code':9999, 'msg': '两次密码输入不一致'})
        pwd_hash = generate_password_hash(password)
        user = User()
        user.phone = phone
        user.pwd_hash = pwd_hash
        user.save()
        return jsonify({'code':200, 'msg': '注册成功'})


@user_blue.route('/login/',methods=['GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')


@user_blue.route('/login/',methods=['POST'])
def login2():
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')
        if not all([phone, password]):
            return jsonify({'code':10002, 'msg': '请填写完整参数'})
        user = User.query.filter(User.phone == phone).first()
        if not user:
            return jsonify({'code':10003, 'msg': '用户不存在'})
        if not check_password_hash(user.pwd_hash, password):
            return jsonify({'code':10004, 'msg':'密码错误'})
        session['user_id'] = user.id
        return jsonify({'code':200, 'msg':'请求成功'})


@user_blue.route('/auth/', methods=['GET'])
def auth():
    if request.method == 'GET':
        return render_template('auth.html')


@user_blue.route('/is_auth/', methods=['POST'])
def is_auth():
    if request.method == 'POST':
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        if user.id_card:
            id_name = user.id_name
            id_card = user.id_card
            return jsonify({'code':200, 'msg': '请求成功', 'id_name': id_name, 'id_card': id_card})

@user_blue.route('/auth/', methods=['POST'])
def auth2():
    if request.method == 'POST':
        id_name = request.form.get('id_name')
        id_card = request.form.get('id_card')
        print(id_card, id_name)
        if not all([id_name, id_card]):
            return jsonify({'code': 10005, 'msg': '请填写完整参数'})
        is_id = r'(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)'
        if not re.match(is_id, id_card):
            return jsonify({'code':10006, 'msg': '身份证号不合法'})
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        if not user:
            return jsonify({'code': 10009, 'msg': '用户未登录'})
        user.id_name = id_name
        user.id_card = id_card
        user.save()
        return jsonify({'code':200, 'msg': '实名验证成功'})


@user_blue.route('/quit/', methods=['POST'])
def quit():
    if request.method == 'POST':
        session.clear()
        return jsonify({'code': 200, 'msg': '退出成功'})
