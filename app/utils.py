from app import dao


def count_cart(cart):
    total_amount = 0

    if cart:
        for c in cart.values():
            total_amount += c['quantity'] * c['price']

    return total_amount


def total_bill(month):
    total = 0
    month_stats = dao.bill_stats(month)
    for s in month_stats:
        total = total + s[1]
    return total



