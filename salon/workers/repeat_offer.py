import asyncio
from asgiref.sync import sync_to_async
from salon.services import get_appointments_for_repeat_offer
from ptb.keyboards.keyboard import to_main_menu


async def repeat_offer_worker(bot):
    while True:
        appointments = await sync_to_async(list)(get_appointments_for_repeat_offer())

        for appointment in appointments:
            telegram_id = await sync_to_async(lambda: appointment.client.telegram_id)()
            service_name = await sync_to_async(lambda: appointment.service.name)()

            await bot.send_message(
                chat_id=telegram_id,
                text=(
                    "💆‍♀️ Вы были у нас 100 дней назад!\n\n"
                    f"Хотите снова записаться на услугу «{service_name}»?"
                ),
                reply_markup=to_main_menu()
            )
            appointment.repeat_offer_sent = True
            await sync_to_async(appointment.save)()

        # ждем час
        await asyncio.sleep(3600)
