import os
from flask import Blueprint, request, render_template, session, url_for, jsonify
from werkzeug.utils import redirect
from app.models import User, House, Facility, Area, HouseImage, db, Order
from utils.settings import MEDIA_PATH

home_blue = Blueprint('home', __name__)


@home_blue.route('/index/', methods=['GET'])
def index():
    if request.method == 'GET':

        return render_template('index.html')


@home_blue.route('/index/', methods=['POST'])
def index2():
    if request.method == 'POST':
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        name = user.name
        phone = user.phone
        area = Area.query.all()
        areas = [i.to_dict() for i in area]
        user_list = [user_id, name, phone]
        return jsonify({'code':200, 'msg': '请求数据成功', 'areas': areas, 'user_list': user_list})


@home_blue.route('/my/', methods=['GET'])
def my():
    if request.method == 'GET':
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        return render_template('my.html', user=user)


@home_blue.route('/profile/', methods=['GET'])
def profile():
    if request.method == 'GET':
        return render_template('profile.html')


@home_blue.route('/profile/', methods=['POST'])
def profile2():
    if request.method == 'POST':
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        if not user:
            return jsonify({'code': 10008, 'msg': '您还没有登录' })
        avatar = request.files.get('avatar')
        name = request.form.get('name')
        if avatar:
            path = os.path.join(MEDIA_PATH, avatar.filename)
            avatar.save(path)
            user.avatar = avatar.filename
            user.save()
        if name:
            user2 = User.query.filter(User.name == name).first()
            if user2:
                return jsonify({'code': 10007, 'msg': '该用户名已被注册' })
            user.name = name
            user.save()
        return jsonify({'code': 200, 'msg': '上传成功'})


@home_blue.route('/myhouse/', methods=['GET'])
def myhouse():
    if request.method == 'GET':

        return render_template('myhouse.html')


@home_blue.route('/myhouse/', methods=['POST'])
def myhouse2():
    if request.method == 'POST':
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        if not user:
            return jsonify({'code': 10010, 'msg': '用户未登录'})
        houses1 = user.houses
        houses = [i.to_dict() for i in houses1]
        for i in range(len(houses)):
            if houses1[i].images:
                image = houses1[i].images[0].url
                houses[i]['image'] = image
        id_card = user.id_card
        return jsonify({'code': 200, 'houses': houses,'id_card': id_card})


@home_blue.route('/new_house/', methods=['POST'])
def new_house():
    if request.method == 'POST':
        area = Area.query.all()
        facility = Facility.query.all()
        areas = [i.to_dict() for i in area]
        facilitys = [i.to_dict() for i in facility]
        return jsonify({'code': 200, 'areas': areas, 'facilitys': facilitys})



@home_blue.route('/newhouse/', methods=['GET'])
def newhouse():
    if request.method == 'GET':
        return render_template('newhouse.html')


@home_blue.route('/newhouse/', methods=['POST'])
def newhouse2():
    if request.method == 'POST':
        user_id = session.get('user_id')
        if user_id:
            title = request.form.get('title')
            price = request.form.get('price')
            area_id = request.form.get('area_id')
            address = request.form.get('address')
            room_count = request.form.get('room_count')
            acreage = request.form.get('acreage')
            unit = request.form.get('unit')
            capacity = request.form.get('capacity')
            beds = request.form.get('beds')
            deposit = request.form.get('deposit')
            min_days = request.form.get('min_days')
            max_days = request.form.get('max_days')
            facility = request.form.getlist('facility')
            house = House()
            house.user_id = user_id
            house.title = title
            house.price = price
            house.area_id = area_id
            house.address = address
            house.room_count = room_count
            house.acreage = acreage
            house.unit = unit
            house.capacity = capacity
            house.beds = beds
            house.deposit = deposit
            house.min_days = min_days
            house.max_days = max_days
            db.session.add(house)
            db.session.commit()

            for i in facility:
                fac = Facility.query.filter(Facility.id == i).first()
                house.facilities.append(fac)
                db.session.commit()

            return jsonify({'code':200, 'msg': '添加成功', 'house_id': house.id})
        else:
            return redirect(url_for('user.login'))


@home_blue.route('/house_image/', methods=['POST'])
def house_image():
    if request.method == 'POST':
        house_id = request.form.get('house_id')
        house_image = request.files.get('house_image')
        path = os.path.join(MEDIA_PATH, house_image.filename)
        house_image.save(path)
        h_image = HouseImage()
        h_image.house_id = house_id
        h_image.url = house_image.filename
        db.session.add(h_image)
        db.session.commit()
        return jsonify({'code':200, 'msg': '添加成功'})


@home_blue.route('/detail/', methods=['GET'])
def detail():
    if request.method == 'GET':
        return render_template('detail.html')


@home_blue.route('/detail/', methods=['POST'])
def detail2():
    if request.method == 'POST':
        user_id = session.get('user_id')
        house_id = request.form.get('house_id')
        house = House.query.filter(House.id == house_id).first()
        book_house = 1
        if user_id == house.user_id:
            book_house = 0
        user = User.query.filter(User.id == house.user_id).first()
        user_dic = user.to_basic_dict()
        house_dic = house.to_dict()
        facilities = house.facilities
        facilities_dic = [i.to_dict() for i in facilities]
        images = house.images
        image_url = []
        if images:
            for i in images:
                image_url.append(i.url)
        return jsonify({'code': 200, 'house_dic': house_dic, 'user_dic': user_dic, 'facilities_dic': facilities_dic, 'image_url': image_url, 'book_house': book_house})


@home_blue.route('/search/', methods=['GET'])
def search():
    if request.method == 'GET':
        return render_template('search.html')


@home_blue.route('/search/', methods=['POST'])
def search2():
    if request.method == 'POST':
        areas = Area.query.all()
        areas = [i.to_dict() for i in areas]
        return jsonify({'code': 200, 'msg': '页面加载成功', 'areas': areas})


@home_blue.route('/search11/', methods=['POST'])
def search3():
    if request.method == 'POST':
        name = request.form.get('areaName')
        sd = request.form.get('startDate')
        ed = request.form.get('endDate')
        now = request.form.get('now')
        area = Area.query.filter(Area.name == name).first()
        house_list1 = House.query.filter(House.area_id == area.id).all()
        orders = Order.query.all()
        house_list2 = []
        for order in orders:
            begin = str(order.begin_date)
            end = str(order.end_date)
            if not(begin > ed or end < sd):
                house = House.query.filter(House.id == order.house_id).first()
                house_list2.append(house)
        house_list = list(set(house_list1) - set(house_list2))
        if now == '最新上线':
            house_list = sorted(house_list, key=lambda house: house.id)
        elif now == '入住最多':
            house_list = sorted(house_list, key=lambda house: house.capacity, reverse=True)
        elif now == '价格 低-高':
            house_list = sorted(house_list, key=lambda house: house.price)
        elif now == '价格 高-低':
            house_list = sorted(house_list, key=lambda house: house.price, reverse=True)
        house_dic = [i.to_full_dict() for i in house_list]
        return jsonify({'code': 200, 'msg': '页面加载成功', 'house_dic': house_dic})