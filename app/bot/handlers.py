from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
)
from loguru import logger

from app.bot.dependencies import get_bot_instance
from app.dependencies import UnitOfWorkDep
from app.order.schemas import AddressInfo
from app.order.service import OrderService
from core.config import AppConfig

bot = get_bot_instance()


async def start_handler(message: Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Ознакомьтесь с нашим меню с помощью кнопок ниже.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Открыть меню [PROD]",
                        web_app=WebAppInfo(url=AppConfig.BOT_WEB_APP_HOST),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Открыть меню [DEV]",
                        web_app=WebAppInfo(url=AppConfig.BOT_WEB_APP_DEV_HOST),
                    )
                ],
            ]
        ),
        parse_mode="Markdown",
    )


async def notify_order_to_admins(uow: UnitOfWorkDep, order_id: int):
    try:
        async with uow:
            order = await OrderService.get_order(uow, order_id)
            address_info = AddressInfo.model_validate(
                await uow.address_info.find_one(order.address_info_id)
            )
            message = f"Новый заказ №{order.id}\n"
            message += f"Пользователь: {order.client.mention_html()}\n"
            message += f"Адрес: {address_info.address_link()}\n"
            message += f"Сумма: {order.amount} сум\n"
            message += f"Статус: {order.display_status()}\n"
            message += f"Способ оплаты: {order.display_payment_method()}\n"
            message += "Товары:\n"
            for item in order.items:
                message += (
                    f"  - {item.product.title} ({item.product.price} сум) x {item.quantity} = "
                    f"{round(item.product.price * item.quantity, 2)} сум\n"
                )

        await bot.send_message(
            chat_id=AppConfig.MANAGERS_CHANNEL_ID,
            text=message,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Принять заказ",
                            callback_data=f"invoice:{order.id}:confirm",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Отклонить заказ",
                            callback_data=f"invoice:{order.id}:decline",
                        )
                    ],
                ]
            ),
        )
    except Exception as e:
        logger.error(e)
