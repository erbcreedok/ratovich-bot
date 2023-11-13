from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext

# Define conversation states
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

# Define reply keyboard
reply_keyboard = [
    ['Обучать', 'Обучиться'],
    ['Отмена']
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Вы хотите обучиться или же обучать пианино?", reply_markup=markup)
    return CHOOSING

async def regular_choice(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['choice'] = text
    if text == 'Обучать':
        await update.message.reply_text("Введите данные: \n- Имя")
    else:
        await update.message.reply_text("Введите данные: \n- Имя")
    return TYPING_REPLY

async def received_information(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    await update.message.reply_text(f"Ваши данные:\n{category}: {text}\nВведите возраст:")
    return TYPING_CHOICE

async def done(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    await update.message.reply_text("Спасибо за информацию!")
    user_data.clear()
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token("6874324316:AAGuPEjR_P25ASyBK93RWb_ZdDiLtPM_oOI").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [MessageHandler(filters.Regex('^(Обучать|Обучиться)$'), regular_choice)],
            TYPING_CHOICE: [MessageHandler(filters.TEXT, regular_choice)],
            TYPING_REPLY: [MessageHandler(filters.TEXT, received_information)]
        },
        fallbacks=[MessageHandler(filters.Regex('^Отмена$'), done)]
    )

    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
