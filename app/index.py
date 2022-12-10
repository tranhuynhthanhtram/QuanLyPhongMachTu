from app import *
from app import controllers
from app.admin import *


app.add_url_rule('/', 'home', controllers.home)
app.add_url_rule('/register', 'register', controllers.user_register, methods=['get', 'post'])
app.add_url_rule('/user-login', 'user-login', controllers.user_signin, methods=['get', 'post'])
app.add_url_rule('/staff-login', 'staff-login', controllers.staff_signin, methods=['get', 'post'])
app.add_url_rule('/doctor-login', 'doctor-login', controllers.doctor_signin, methods=['get', 'post'])
app.add_url_rule('/admin-login', 'admin-login', controllers.signin_admin, methods=['post'])
app.add_url_rule('/user-logout', 'user-logout', controllers.user_signout)
app.add_url_rule('/staff-logout', 'staff-logout', controllers.staff_signout)
app.add_url_rule('/doctor-logout', 'doctor-logout', controllers.doctor_signout)
app.add_url_rule('/book-schedule', 'book-schedule', controllers.book_schedule, methods=['get', 'post'])
app.add_url_rule('/add-phieu-kham', 'add-phieu-kham', controllers.add_phieu_kham, methods=['get', 'post'])
app.add_url_rule('/api/add-medicine-to-cart', 'add-medicine-to-cart', controllers.add_medicine_to_cart, methods=['post'])
app.add_url_rule('/api/update-quantity', 'update-quantity', controllers.update_quantity, methods=['put'])
app.add_url_rule('/api/delete-medicine-cart', 'delete-medicine-cart', controllers.delete_medicine_cart, methods=['delete'])
app.add_url_rule('/api/search-medical-history', 'search-medical-history', controllers.search_medical_history, methods=['get', 'post'])
app.add_url_rule('/bills-staff/', 'bills-staff', controllers.staff_bills_list, methods=['get', 'post'])
app.add_url_rule('/api/pay', 'pay', controllers.pay, methods=['post'])


@login.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id=user_id)


if __name__ == "__main__":
    app.run(debug=True)
