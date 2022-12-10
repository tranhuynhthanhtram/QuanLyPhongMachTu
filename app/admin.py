from datetime import datetime
from flask import redirect, request
from app import db, app, dao
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from app.models import UserRole, Medicine, Category, UnitMedicine, User, ListDetail


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.Admin)


class UserView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    details_modal = True
    column_filters = ['fullname', 'username']
    column_searchable_list = ['fullname', 'username']
    column_exclude_list = ['avatar', 'active', 'joined_date']
    column_labels = {
        'id': 'STT',
        'fullname': 'Họ và tên',
        'username': 'Tên đăng nhập',
        'password': 'Mật khẩu',
        'user_role': 'Quyền',
        'avatar': 'Ảnh',
        'joined_date': 'Ngày tạo'
    }
    form_excluded_columns = ['active', 'details', 'bills', 'joined_date']


class UnitView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    details_modal = True
    column_searchable_list = ['id', 'name']
    column_labels = {
        'id': 'Mã đơn vị',
        'name': 'Tên đơn vị',
        'medicines': 'Thuốc'
    }
    form_excluded_columns = ['medicines']


class CateView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    details_modal = True
    column_searchable_list = ['id', 'name']
    column_labels = {
        'id': 'Mã loại thuốc',
        'name': 'Tên loại thuốc'
    }
    form_excluded_columns = ['medicine']


class MedicineView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    details_modal = True
    column_searchable_list = ['id', 'name', 'unit_id']
    column_filters = 'id', 'name', 'medicalbill'
    column_display_all_relations = True
    column_exclude_list = ['medicalbill']
    column_labels = {
        'id': 'Mã thuốc',
        'name': 'Tên thuốc',
        'unit_id': 'Đơn vị tính',
        'price': 'Giá tiền',
        'how_to_use': 'Cách dùng',
        'unitmedicine': 'Đơn vị tính',
        'cates': 'Loại thuốc',
        'medicalbill': 'Đơn thuốc'
    }
    form_excluded_columns = ['medicalbill']


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class ListDetailView(AuthenticatedModelView):
    can_create = False
    edit_modal = True
    column_labels = {
        'listschedule': 'Ngày khám',
        'fullname': 'Tên bệnh nhân',
        'gender': 'Giới tính',
        'year_born': 'Năm sinh',
        'address': 'Địa chỉ',
        'user': 'Tên người đăng kí'
    }
    column_exclude_list = ['user']
    form_excluded_columns = ['user']


class Stats(BaseView):
    @expose('/')
    def index(self):
        month = request.args.get('month', datetime.now().month)
        kw = request.args.get('kw')
        id = request.args.get('id')
        return self.render('admin/stats.html',
                           medi_month_stats=dao.medicine_month_stats(kw=kw, id=id, month=month))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.Admin)


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        total = 0
        month = request.args.get('month', datetime.now().month)
        return self.render('admin/index.html', month_stats=dao.bill_stats(month), total=dao.total_bill(month))


admin = Admin(app=app, name='QUẢN LÝ PHÒNG MẠCH', template_mode='bootstrap4', index_view=MyAdminIndexView())

admin.add_view(ListDetailView(ListDetail, db.session, name='Danh sách ngày khám', category='Quản lý danh sách khám'))
admin.add_sub_category(name='medicine_manager ', parent_name='Quản lý danh sách khám')

admin.add_view(UnitView(UnitMedicine, db.session, name='Đơn vị tính', category='Quản lý thuốc'))
admin.add_view(CateView(Category, db.session, name='Loại thuốc', category='Quản lý thuốc'))
admin.add_view(MedicineView(Medicine, db.session, name='Thuốc', category='Quản lý thuốc'))
admin.add_sub_category(name='medicine_manager ', parent_name='Quản lý thuốc')

admin.add_view(UserView(User, db.session, name='Người dùng'))
admin.add_view(Stats(name='Thống kê - báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))

