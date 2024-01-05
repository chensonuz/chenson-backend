from enum import Enum


class OrderStatus(Enum):
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    PAYMENT_REQUIRED = "Payment required"
    AWAITING_PAYMENT = "Awaiting payment"
    PAID = "Completed"
    CANCELLED = "Cancelled"
    EXPIRED = "Expired"
    FINISHED = "Finished"


class PaymentMethod(Enum):
    CASH = "Cash"
    CARD = "Card"
