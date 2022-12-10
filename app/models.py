from sqlalchemy.orm import relationship, backref
from app import db, app
from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, Boolean, ForeignKey
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    Admin = 1
    Customer = 2
    Staff = 3
    Doctor = 4
    Nurse = 5


class User(BaseModel, UserMixin):
    fullname = Column(String(255), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.Customer)
    details = relationship('ListDetail', backref='user', lazy=True)
    bills = relationship('Bills', backref='user', lazy=True)

    def __str__(self):
        return self.fullname


class ListSchedule(BaseModel):
    __tablename__ = 'listschedule'

    created_date = Column(DateTime, default=datetime.now(), nullable=False)
    details = relationship('ListDetail', backref='listschedule', lazy=True)

    def __str__(self):
        return self.created_date.__str__()


class Gender(UserEnum):
    Male = 1
    Female = 2
    Other = 3


class ListDetail(BaseModel):
    __tablename__ = 'listdetail'

    list_schedule_id = Column(Integer, ForeignKey(ListSchedule.id), nullable=False)
    fullname = Column(String(255), nullable=False)
    gender = Column(Enum(Gender), default=Gender.Female)
    year_born = Column(String(20))
    address = Column(String(100))
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True)


class MedicallBillDetail(db.Model): # bảng sinh ra từ Medicine và MedicalBil
    medicine_id = Column(Integer, ForeignKey('medicine.id'), nullable=False, primary_key=True) #id thuốc
    medicalbill_id = Column(Integer, ForeignKey('medicalbill.id'), nullable=False, primary_key=True) #id phiếu thuốc
    quantity = Column(Integer, nullable=False, default=1) #số lượng thuốc

    def __str__(self):
        return self.medicalbill_id.__str__()


class UnitMedicine(BaseModel):
    __tablename__ = 'unitmedicine'

    name = Column(String(20), nullable=False)
    medicines = relationship('Medicine', backref='unitmedicine', lazy=True)

    def __str__(self):
        return self.name


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class Medicine(BaseModel):
    __tablename__ = 'medicine'

    name = Column(String(50), nullable=False)
    unit_id = Column(Integer, ForeignKey(UnitMedicine.id), nullable=False)
    price = Column(Float, default=0)
    how_to_use = Column(String(500))
    medicalbill = relationship('MedicallBillDetail', backref='medicine', lazy=True)
    cates = relationship('Category', secondary='medi_cates', lazy='subquery', backref=backref('medicine', lazy=True))

    def __str__(self):
        return self.name


medi_cates = db.Table('medi_cates', Column('medicine_id', Integer, ForeignKey('medicine.id'), primary_key=True),\
                                Column('category_id', Integer, ForeignKey('category.id'), primary_key=True))


class MedicalBill(BaseModel):#phiếu khám bệnh
    __tablename__ = 'medicalbill'
    fullname = Column(String(50), nullable=False)
    created_day = Column(DateTime, default=datetime.now())
    symptom = Column(String(100))  #triệu chứng
    prognostication = Column(String(100)) # dự đoán bệnh
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    medicine = relationship('MedicallBillDetail', backref='medicalbill', lazy=True)

    def __str__(self):
        return self.id.__str__()


class Bills(BaseModel):#hóa đơn
    __tablename__ = 'bills'

    fullname = Column(String(50), nullable=False)
    examined_date = Column(DateTime, nullable=False) #ngày khám bệnh
    medical_costs = Column(Float, default=100000) #tiền khám
    drug_money = Column(Float, default=0) #tiền thuốc
    state_pay = Column(Boolean, default=False)  # true là thanh toán rồi, false là chưa thanh toán
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    medical_bill_id = Column(Integer, ForeignKey(MedicalBill.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #
        # #Đơn vị thuốc
        # u1 = UnitMedicine(name='Chai')
        # u2 = UnitMedicine(name='Vỹ')
        # u3 = UnitMedicine(name='Viên')
        # db.session.add(u1)
        # db.session.add(u2)
        # db.session.add(u3)
        # #Loại thuốc
        # c1 = Category(name='Say xe')
        # c2 = Category(name='Đau bụng')
        # c3 = Category(name='Nhức đầu')
        # c4 = Category(name='Canxi')
        # db.session.add(c1)
        # db.session.add(c2)
        # db.session.add(c3)
        # db.session.add(c4)
        # #Thuốc
        # t1 = Medicine(name='diphenhydramine', unit_id=3, price=5000,
        #               how_to_use='Uống trước khi khởi hàng 30 phút', )
        #
        # t2 = Medicine(name='dimenhydrinate', unit_id=3, price=6000,
        #               how_to_use='Uống trước khi khởi hàng 30 phút', )
        # t3 = Medicine(name='cinnarizine', unit_id=3, price=7000,
        #               how_to_use='Uống trước khi khởi hàng 30 phút', )
        # t4 = Medicine(name='meclizine', unit_id=3, price=8000,
        #               how_to_use='Uống trước khi khởi hàng 30 phút', )
        # t5 = Medicine(name='Ostelin Vitamin D3 & Calcium.', unit_id=3, price=10000,
        #               how_to_use='Uống vào buổi sáng', )
        # t6 = Medicine(name="Calcium Magnesium Zinc của Nature's Bounty", unit_id=3, price=12000,
        #               how_to_use='Uống vào buổi sáng', )
        # t7 = Medicine(name='Total Calcium Magnesium + D3.', unit_id=3, price=15000,
        #               how_to_use='Uống vào buổi sáng', )
        # t8 = Medicine(name='Kirkland Calcium 600mg + D3', unit_id=1, price=18000,
        #               how_to_use='Uống vào buổi sáng', )
        # t9 = Medicine(name='nizatidine (Axid)', unit_id=2, price=50000,
        #               how_to_use='Uống sau khi ăn', )
        # t10 = Medicine(name='famotidine (Pepcid, Pepcid AC)', unit_id=3, price=180000,
        #               how_to_use='Uống sau khi ăn', )
        # t11 = Medicine(name='cimetidine (Tagamet, Tagamet HB)', unit_id=1,
        #                price=18000, how_to_use='Uống sau khi ăn')
        #
        # # t1.cates.add(c1)
        # t1.cates.append(c1)
        # t1.cates.append(c2)
        # db.session.add(t1)
        #
        # # t2.cates.add(c1)
        # t2.cates.append(c1)
        # t2.cates.append(c3)
        # db.session.add(t1)
        #
        # # t3.cates.add(c1)
        # t3.cates.append(c1)
        # t3.cates.append(c4)
        # db.session.add(t1)
        #
        # # t4.cates.add(c1)
        # t4.cates.append(c1)
        # t4.cates.append(c4)
        # db.session.add(t4)
        #
        # # t5.cates.add(c2)
        # t5.cates.append(c2)
        # t5.cates.append(c3)
        # db.session.add(t5)
        #
        # # t6.cates.add(c2)
        # t6.cates.append(c2)
        # db.session.add(t6)
        #
        # # t7.cates.add(c2)
        # t7.cates.append(c2)
        # t7.cates.append(c1)
        # db.session.add(t7)
        #
        # # t8.cates.add(c2)
        # t8.cates.append(c2)
        # t8.cates.append(c3)
        # db.session.add(t8)
        #
        # # t9.cates.add(c3)
        # t9.cates.append(c3)
        # t9.cates.append(c4)
        # db.session.add(t9)
        #
        # # t10.cates.add(c3)
        # t10.cates.append(c3)
        # t9.cates.append(c2)
        # t9.cates.append(c1)
        # db.session.add(t10)
        #
        # # t11.cates.add(c4)
        # t11.cates.append(c4)
        # t11.cates.append(c3)
        # t11.cates.append(c2)
        # t11.cates.append(c1)
        # db.session.add(t11)
        #
        # #User
        # user1 = User(fullname='admin', username='admin', password='202cb962ac59075b964b07152d234b70',
        #              avatar='https://res.cloudinary.com/dxajszqyt/image/upload/v1670597632/ae382fmw4ye8lamhsvlc.png',
        #              user_role='1')
        #
        # user2 = User(fullname='tram', username='tram', password='202cb962ac59075b964b07152d234b70',
        #              avatar='https://res.cloudinary.com/dxajszqyt/image/upload/v1670597632/ae382fmw4ye8lamhsvlc.png',
        #              user_role='2')
        #
        # user3 = User(fullname='staff', username='staff', password='202cb962ac59075b964b07152d234b70',
        #              avatar='https://res.cloudinary.com/dxajszqyt/image/upload/v1670597632/ae382fmw4ye8lamhsvlc.png',
        #              user_role='3')
        #
        # user4 = User(fullname='doctor', username='doctor', password='202cb962ac59075b964b07152d234b70',
        #              avatar='https://res.cloudinary.com/dxajszqyt/image/upload/v1670597632/ae382fmw4ye8lamhsvlc.png',
        #              user_role='4')
        #
        # user5 = User(fullname='nurse', username='nurse', password='202cb962ac59075b964b07152d234b70',
        #              avatar='https://res.cloudinary.com/dxajszqyt/image/upload/v1670597632/ae382fmw4ye8lamhsvlc.png',
        #              user_role='5')
        # db.session.add(user1)
        # db.session.add(user2)
        # db.session.add(user3)
        # db.session.add(user4)
        # db.session.add(user5)
        #
        #
        # db.session.commit()
        #
        #
        #
