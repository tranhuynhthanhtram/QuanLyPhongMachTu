from datetime import datetime
import cloudinary
from flask import render_template, request, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, login_required
from app import dao, app, client
from app.decorators import annonymous_user
from app.models import UserRole, Medicine, Bills


def home():
    return render_template('index.html')


def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        fullname = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        avatar_path = None

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                dao.add_user(fullname=fullname, username=username,
                             password=password, email=email,
                             avatar=avatar_path)
                return redirect(url_for('user-login'))
            else:
                err_msg = 'Mật khẩu không khớp!!!'
        except Exception as ex:
            err_msg = 'Hệ thống đang có lỗi: ' + str(ex)

    return render_template('register.html', err_msg=err_msg)


@annonymous_user
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user_cus = dao.check_login(username=username, password=password, role=UserRole.Customer)
        if user_cus:
            login_user(user=user_cus)
            return redirect('/')

        user_nur = dao.check_login(username=username, password=password, role=UserRole.Nurse)
        if user_nur:
            login_user(user=user_nur)
            return redirect('/book-schedule')
        else:
            err_msg = 'Tên đăng nhập hoặc mật khẩu không chính xác!!!'

    return render_template('login.html', err_msg=err_msg)


@annonymous_user
def staff_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.check_login(username=username, password=password, role=UserRole.Staff)
        if user:
            login_user(user=user)
            return redirect(url_for('bills-staff'))
        else:
            err_msg = 'Tên đăng nhập hoặc mật khẩu không chính xác!!!'

    return render_template('bills.html', err_msg=err_msg)


@annonymous_user
def doctor_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.check_login(username=username, password=password, role=UserRole.Doctor)
        if user:
            login_user(user=user)
            return redirect(url_for('add-phieu-kham'))
        else:
            err_msg = 'Tên đăng nhập hoặc mật khẩu không chính xác!!!'

    return render_template('phieu_kham.html', err_msg=err_msg)


def signin_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.check_login(username=username, password=password, role=UserRole.Admin)
    if user:
        login_user(user=user)
    return redirect('/admin')


def user_signout():
    logout_user()
    return redirect(url_for('user-login'))


def staff_signout():
    logout_user()
    return redirect(url_for('staff-login'))


def doctor_signout():
    logout_user()
    return redirect(url_for('doctor-login'))


@login_required
def book_schedule():
    err_msg = ""
    msg_success = ''
    full_patient = ''
    if request.method.__eq__('POST'):
        date = request.form.get('date')
        created_date = datetime.strptime(date, "%Y-%m-%d")
        fullname = request.form.get('name')
        gender = request.form.get('gender')
        year_born = request.form.get('year_born')
        address = request.form.get('address')

        try:
            count = dao.count_schedule_by_date(created_date)
            dem = 0
            for c in count:
                dem = dem + 1
            if dem < 30:
                dao.add_schedule(created_date=created_date, fullname=fullname, gender=gender, year_born=year_born,
                                 address=address)
            else:
                full_patient = " Đủ 30 bệnh nhân trong ngày"
        except Exception as err:
            err_msg = " Hệ thống báo lỗi " + str(err)
        else:
            msg_success = "Đặt lịch thành công"
            message = client.messages.create(
                messaging_service_sid='MG7d95f17888d4b32c271025663602add6',
                body='Đặt lịch thành công',
                to='+84769669147'
            )

    return render_template('book_schedule.html', err_msg=err_msg, msg_success=msg_success,
                           full_patient=full_patient)


def add_phieu_kham():
    err_msg = ""
    msg_success = ''
    if request.method.__eq__('POST'):
        fullname = request.form.get('name')
        # medical_examination = request.form.get('medical_examination')
        NgayKham = request.form.get('NgayKham')
        created_date = datetime.strptime(NgayKham, "%Y-%m-%d")
        symptom = request.form.get('symptom')
        prognostication = request.form.get('prognostication')

        try:
            key = app.config['CART_KEY']
            cart = session.get(key)
            dao.add_MedicalBill(fullname, created_date, symptom, prognostication, cart)

        except Exception as err:
            err_msg = " Hệ thống báo lỗi " + str(err)

        else:
            msg_success = "Lưu phiếu thành công"
            del session[key]
    medicine = Medicine.query.all()
    return render_template('phieu_kham.html', err_msg=err_msg, msg_success=msg_success, medicine=medicine)


def add_medicine_to_cart():
    data = request.json
    id = str(data.get('id'))

    p = dao.get_medicine_by_id(id=id)
    price = p.price

    key = app.config['CART_KEY']
    # ban đầu giỏ rỗng
    cart = {}
    # kiểm tra đã có giỏ hàng chưa
    if key in session:
        cart = session[key]  # có rồi

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            'id': id,
            'price': price,
            'quantity': 1
        }
    session[key] = cart

    unit = p.unit_id
    how_to_use = p.how_to_use

    return jsonify({
        'unit_id': unit,
        'how_to_use': how_to_use
    })


# Cập nhật số lượng thuốc
def update_quantity():
    data = request.json
    id = str(data.get('id'))
    quantity = data.get('quantity')

    try:
        key = app.config['CART_KEY']
        cart = session.get(key)
        if cart and id in cart:
            cart[id]['quantity'] = quantity
        session[key] = cart
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})


def delete_medicine_cart():
    data = request.json
    id = str(data.get('id'))

    try:
        key = app.config['CART_KEY']
        cart = session.get(key)
        if cart and id in cart:
            del cart[id]
        session[key] = cart

    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})


def search_medical_history():
    name = []
    quantity = []
    data = request.json
    fullname = str(data.get('fullname'))

    search = dao.search_medical_history(fullname)

    for x in search:
        name.append(x[1])
        quantity.append(x[2])

    return jsonify({
        'name': name,
        'quantity': quantity
    })


#nhân viên thanh toán hóa đơn
def staff_bills_list():
    bills = Bills.query.all()
    medicine_bill_id = request.form.get('medicine_bill_id')
    if medicine_bill_id:
        return render_template('bills.html', bills=dao.search_medicine_bill_by_id(medicine_bill_id))
    return render_template('bills.html', bills=bills)


def pay():
    data = request.json
    id = str(data.get('id'))
    try:
        dao.reload_state_pay(id)
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})
