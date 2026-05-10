from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        order.created_at = date

    order.save()

    tickets_all = [
        Ticket(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )
        for ticket in tickets
    ]

    for ticket in tickets_all:
        ticket.save()

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
