from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler, ContextTypes
from cities import cities_reply_keyboard
from save_data import save_data

# Define conversation stages
(CHOOSING_ACTION, TYPING_NAME, TYPING_AGE, CHOOSING_CITY, CHOOSING_LEVEL, CHOOSING_LOCATION, TYPING_PRICE, SHARING_PHONE) = range(8)

# Start the conversation
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['Обучать', 'Обучиться']]
    await update.message.reply_text(
        "Вы хотите обучиться или же обучать игре на пианино?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CHOOSING_ACTION

# Choose action
async def choosing_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['action'] = update.message.text
    await update.message.reply_text('Как вас зовут?')
    return TYPING_NAME

# Input name
async def typing_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text('Сколько вам лет?')
    return TYPING_AGE

# Input age
async def typing_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['age'] = update.message.text
    reply_keyboard = cities_reply_keyboard
    await update.message.reply_text(
        "Ваш город?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CHOOSING_CITY

# Choose city
async def choosing_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['city'] = update.message.text
    reply_keyboard = [['Средний', 'Высшее', 'Магистратура']]
    await update.message.reply_text(
        text="Какой у Вас уровень игры на пианино?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CHOOSING_LEVEL


# Choose level
async def choosing_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['level'] = update.message.text
    action = context.user_data.get('action')
    question = 'Где вы можете проводить обучение?'
    if action == 'Обучиться':
        question = 'Где вы можете обучаться?'
    reply_keyboard = [['Дома', 'На выезд']]
    await update.message.reply_text(question, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CHOOSING_LOCATION

# Choose location
async def choosing_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['location'] = update.message.text
    action = context.user_data.get('action')
    reply_keyboard = [['3000', '5000', '10000']]
    question = 'Сколько стоит ваш урок?'
    if action == 'Обучиться':
        question = 'Сколько вы готовы платить за урок?'
    await update.message.reply_text(question, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return TYPING_PRICE

# Input price
async def typing_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['price'] = update.message.text
    button = KeyboardButton(text="Поделитесь вашим номером телефона", request_contact=True)
    await update.message.reply_text('Поделитесь вашим номером телефона', reply_markup=ReplyKeyboardMarkup([[button]], one_time_keyboard=True))
    return SHARING_PHONE

# Share phone number
async def sharing_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    context.user_data['phone'] = contact.phone_number
    await update.message.reply_text('Спасибо за информацию!')
    save_data(context.user_data)
    return ConversationHandler.END

# Cancel conversation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Диалог завершен.')
    return ConversationHandler.END

# Main function to run the bot
def main():
    # Create the Application and pass in the bot's token
    application = Application.builder().token("6612564814:AAHzxOrOg4MKUQehkfQ2qDOLRtjHw1IvcnA").build()

    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING_ACTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, choosing_action)],
            TYPING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, typing_name)],
            TYPING_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, typing_age)],
            CHOOSING_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, choosing_city)],
            CHOOSING_LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, choosing_level)],
            CHOOSING_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, choosing_location)],
            TYPING_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, typing_price)],
            SHARING_PHONE: [MessageHandler(filters.CONTACT, sharing_phone)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
