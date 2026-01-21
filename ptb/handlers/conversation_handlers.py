from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters
)
from .callback_handlers import (
    handler_main_menu, handler_salon_menu, handler_procedure_menu,
    handler_date_menu, handler_time_menu, handler_name_menu,
    handler_phone_menu, handler_add_promo, handler_appointment_menu,
    handler_after_appointment, handler_master_menu, handler_master_feedback_menu,
    handler_feedback_menu, handler_confirm_feedback_menu, handler_after_feedback,
)
from . import cmd_handlers, states_bot


conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', cmd_handlers.start)
    ],
    states={
        states_bot.MAIN_MENU: [CallbackQueryHandler(handler_main_menu)],
        states_bot.SELECT_SALON: [CallbackQueryHandler(handler_salon_menu)],
        states_bot.SELECT_PROCEDURE: [CallbackQueryHandler(handler_procedure_menu)],
        states_bot.SELECT_DATE: [CallbackQueryHandler(handler_date_menu)],
        states_bot.SELECT_TIME: [CallbackQueryHandler(handler_time_menu)],
        states_bot.CLIENT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler_name_menu)],
        states_bot.CLIENT_PHONENUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler_phone_menu)],
        states_bot.APPOINTMENT: [CallbackQueryHandler(handler_appointment_menu)],
        states_bot.ADD_PROMO: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler_add_promo)],
        states_bot.AFTER_APPOINTMENT: [CallbackQueryHandler(handler_after_appointment)],
        states_bot.SELECT_MASTER: [CallbackQueryHandler(handler_master_menu)],
        states_bot.SELECT_MASTER_TO_FEEDBACK: [CallbackQueryHandler(handler_master_feedback_menu)],
        states_bot.CLIENT_FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler_feedback_menu)],
        states_bot.CONFIRM_FEEDBACK_MENU: [CallbackQueryHandler(handler_confirm_feedback_menu)],
        states_bot.AFTER_FEEDBACK: [CallbackQueryHandler(handler_after_feedback)],
    },
    fallbacks=[CommandHandler('start', cmd_handlers.start)]
)
