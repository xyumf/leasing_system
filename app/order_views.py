from flask import Blueprint, request, render_template, session,jsonify

from app.models import User, House, Order, db

order_blue = Blueprint('order', __name__)


@order_blue.route('/orders/', methods=['GET'])
def orders():
    if request.method == 'GET':
        return render_template('orders.html')


@order_blue.route('/orders/', methods=['POST'])
def orders2():
    if request.method == 'POST':
        user_id = session.get('user_id')
        order = Order.query.filter(Order.user_id == user_id).all()
        order_dic = [i.to_dict() for i in order]
        return jsonify({'code': 200, 'msg': '获取订单成功', 'order_dic': order_dic})


@order_blue.route('/lorders/', methods=['GET'])
def lorders():
    if request.method == 'GET':
        return render_template('lorders.html')


@order_blue.route('/lorders/', methods=['POST'])
def lorders2():
    if request.method == 'POST':
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        houses = user.houses
        orders = []
        for i in houses:
            order = Order.query.filter(Order.house_id == i.id).first()
            if order:
                order = order.to_dict()
                orders.append(order)
        return jsonify({'code': 200, 'msg': '订单信息加载成功', 'orders': orders})


@order_blue.route('/order_take/', methods=['POST'])
def order_take():
    if request.method == 'POST':
        orderstr = request.form.get('order_id')
        order_id = orderstr.split('：')[1]
        order = Order.query.filter(Order.id == order_id ).first()
        order.status = 'WAIT_PAYMENT'
        db.session.add(order)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '已接单'})


@order_blue.route('/cancel_order/', methods=['POST'])
def cancel_order():
    if request.method == 'POST':
        comment = request.form.get('comment')
        orderstr = request.form.get('order_id')
        order_id = orderstr.split('：')[1]
        order = Order.query.filter(Order.id == order_id ).first()
        order.status = 'CANCELED'
        order.comment = comment
        db.session.add(order)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '订单已取消'})


@order_blue.route('/order_comment/', methods=['POST'])
def order_comment():
    if request.method == 'POST':
        comment = request.form.get('comment')
        orderstr = request.form.get('order_id')
        order_id = orderstr.split('：')[1]
        order = Order.query.filter(Order.id == order_id).first()
        order.comment = comment
        db.session.add(order)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '评论发布成功'})


@order_blue.route('/booking/', methods=['GET'])
def booking():
    if request.method == 'GET':
        return render_template('booking.html')


@order_blue.route('/booking/', methods=['POST'])
def booking2():
    if request.method == 'POST':
        house_id = request.form.get('house_id')
        house = House.query.filter(House.id == house_id).first()
        house_dic = house.to_dict()
        images = house.images
        if images:
            image = images[0].url
        return jsonify({'code': 200, 'msg': '房屋信息请求成功', 'house_dic': house_dic, 'image': image})


@order_blue.route('/book_order/', methods=['POST'])
def book_order():
    if request.method == 'POST':
        user_id = session.get('user_id')
        house_id = request.form.get('house_id')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        price = request.form.get('price')
        order_amount = request.form.get('order_amount')
        amount = order_amount.split('(')[0]
        days = order_amount.split('共')[1].split('晚')[0]
        order = Order()
        order.user_id = user_id
        order.house_id = house_id
        order.begin_date = start_date
        order.end_date = end_date
        order.house_price = price
        order.days = days
        order.amount = amount
        db.session.add(order)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '房屋订单提交成功'})