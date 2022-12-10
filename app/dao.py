import hashlib
from flask_login import current_user
from sqlalchemy import func, extract
from app import app, db, utils
from app.models import ListSchedule, ListDetail, User, Gender, Medicine, MedicallBillDetail, MedicalBill, \
    Bills, UnitMedicine


def add_user(fullname, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(fullname=fullname.strip(), username=username.strip(), password=password,
                email=kwargs.get('email'), avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def check_login(username, password, role):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()


def count_schedule_by_date(created_date='1212-12-12'):
    return db.session.query(ListDetail.id, ListSchedule.created_date) \
        .join(ListDetail, ListDetail.list_schedule_id.__eq__(ListSchedule.id)) \
        .filter(ListSchedule.created_date == created_date) \
        .group_by(ListDetail.id, ListSchedule.created_date).all()


def add_schedule(created_date, fullname, **kwargs):
    if Gender.Male == 1:
        gender = "Nam"
    else:
        if Gender.Female == 2:
            gender = kwargs.get('gender')
        else:
            gender = kwargs.get('gender')

    a = ListSchedule.query.filter(ListSchedule.created_date == created_date).first()

    if a is None:
        list = ListSchedule(created_date=created_date)
        db.session.add(list)
        db.session.commit()

        d = ListDetail(list_schedule_id=list.id, user=current_user,
                       fullname=fullname.strip(),
                       gender=kwargs.get('gender'),
                       year_born=kwargs.get('year_born'),
                       address=kwargs.get('address'))
    else:
        d = ListDetail(list_schedule_id=a.id, user=current_user,
                      fullname=fullname.strip(),
                      gender=gender,
                      year_born=kwargs.get('year_born'),
                      address=kwargs.get('address'))

    db.session.add(d)
    db.session.commit()


def get_medicine_by_id(id):
    return Medicine.query.get(id)


def add_MedicalBill(fullname, created_date, symptom, prognostication, cart):
    medicinalBill = MedicalBill(fullname=fullname, created_day=created_date,
                                symptom=symptom,
                                prognostication=prognostication,
                                user_id=current_user.id)

    db.session.add(medicinalBill)
    db.session.commit()
    # tạo một cái bill
    add_Bills(medicalBill=medicinalBill, cart=cart)

    # add medicalBillDetail
    for c in cart.values():
        medicalBillDetail = MedicallBillDetail(medicalbill_id=medicinalBill.id,
                                               medicine_id=c['id'],
                                               quantity=c['quantity'])
        db.session.add(medicalBillDetail)
    db.session.commit()


def search_medical_history(fullname):
    return db.session.query(MedicalBill.fullname, Medicine.name, func.sum(MedicallBillDetail.quantity)) \
        .join(MedicallBillDetail, MedicalBill.id.__eq__(MedicallBillDetail.medicalbill_id)) \
        .join(Medicine, Medicine.id.__eq__(MedicallBillDetail.medicine_id)) \
        .filter(MedicalBill.fullname.__eq__(fullname)) \
        .group_by(MedicalBill.fullname, Medicine.name).all()


def load_list_bills(user_id):
    return Bills.query.filter(Bills.user_id.__eq__(user_id))


def search_medicine_bill_by_id(medicine_bill_id):
    return Bills.query.filter(Bills.medical_bill_id.__eq__(medicine_bill_id))


def add_Bills(medicalBill, cart):
    user = get_user_by_id(medicalBill.user_id)
    bills = Bills(fullname=medicalBill.fullname, examined_date=medicalBill.created_day,
                 drug_money=utils.count_cart(cart),
                 user_id=user.id,
                 medical_bill_id=medicalBill.id)
    db.session.add(bills)
    db.session.commit()


def reload_state_pay(bill_id):
    p = Bills.query.filter(Bills.id.__eq__(bill_id)).first()
    p.state_pay = True
    db.session.commit()


def total_bill(month):
    return db.session.query(func.sum(Bills.medical_costs + Bills.drug_money))\
        .filter(extract('month', Bills.examined_date) == month).all()


def bill_stats(month):
    p = total_bill(month)
    q = p[0]
    x = q[0]

    p = db.session.query(extract('day', Bills.examined_date), func.sum(Bills.medical_costs + Bills.drug_money), func.count(Bills.medical_bill_id),
                            func.round(((func.sum(Bills.medical_costs + Bills.drug_money)/x)*100), 2))\
        .filter(extract('month', Bills.examined_date) == month) \
        .group_by(extract('day', Bills.examined_date))\
        .order_by(extract('day', Bills.examined_date))

    return p.all()


def medicine_month_stats(month, kw=None, id=None):
    p = db.session.query(Medicine.id, Medicine.name, UnitMedicine.name, MedicallBillDetail.quantity)\
                    .join(MedicallBillDetail, MedicallBillDetail.medicine_id.__eq__(Medicine.id), isouter=True)\
                    .join(MedicalBill, MedicalBill.id.__eq__(MedicallBillDetail.medicalbill_id))\
                    .join(UnitMedicine, Medicine.unit_id.__eq__(UnitMedicine.id))\
                    .join(Bills, Bills.medical_bill_id.__eq__(MedicalBill.id))\
                    .filter(extract('month', Bills.examined_date) == month)\
                    .group_by(Medicine.id, Medicine.name)\
                    .order_by(-MedicallBillDetail.quantity)

    if kw:
        p = p.filter(Medicine.name.contains(kw))
    if id:
        p = p.filter(Medicine.id.contains(id))
    return p.all()


