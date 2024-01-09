from enum import Enum

ORDER_STATUS_DISPLAY_NAMES = {
    "Accepted": "Принят",
    "Rejected": "Отклонен",
    "Payment required": "Требуется оплата",
    "Awaiting payment": "Ожидает оплаты",
    "Completed": "Завершен",
    "Cancelled": "Отменен",
    "Expired": "Просрочен",
    "Finished": "Завершен",
}

PAYMENT_METHOD_DISPLAY_NAMES = {
    "Cash": "Наличные",
    "Card": "Карта",
}


class OrderStatus(Enum):
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    PAYMENT_REQUIRED = "Payment required"
    AWAITING_PAYMENT = "Awaiting payment"
    PAID = "Completed"
    CANCELLED = "Cancelled"
    EXPIRED = "Expired"
    FINISHED = "Finished"

    def display_name(self) -> str:
        try:
            return ORDER_STATUS_DISPLAY_NAMES[self.value]
        except KeyError:
            return self.value


class PaymentMethod(Enum):
    CASH = "Cash"
    CARD = "Card"

    def display_name(self) -> str:
        try:
            return PAYMENT_METHOD_DISPLAY_NAMES[self.value]
        except KeyError:
            return self.value
