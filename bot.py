import logging
from telegram import ReplyKeyboardMarkup
from random import choice
from telegram.ext import Updater, CommandHandler

logging.basicConfig(filename='bot.log', level=logging.INFO)

quotes = ["Цитата номер раз", "Цитата номер два", "Цитата номер три"]
my_keyboard = ReplyKeyboardMarkup([["/add_quote"], ["/random_quote"], ["/show_quotes"], ["/delete_quotes"]])


def greet_user(update, context):
    context.user_data['quotes'] = quotes.copy()
    print('Вызван /start')
    update.message.reply_text('Здравствуйте', reply_markup=my_keyboard)


def add_quote(update, context):
    if context.args:
        context.user_data['quotes'].append(" ".join(context.args))
        update.message.reply_text(f"Вы добавили цитату: '{context.user_data['quotes'][-1]}'", reply_markup=my_keyboard)
    else:
        update.message.reply_text("Вы не указали цитату", reply_markup=my_keyboard)


def show_quotes(update, context):
    message = ""
    for i, quote in enumerate(context.user_data['quotes'], start=1):
        message += f"{i}) {quote}\n"
    update.message.reply_text(message, reply_markup=my_keyboard)


def delete_quote(update, context):
    if context.args:
        if context.args[0].isnumeric():
            i = int(context.args[0]) - 1
            if 0 <= i < len(context.user_data['quotes']):
                message = f"Вы удалили цитату: '{context.user_data['quotes'][i]}'"
                context.user_data['quotes'].pop(i)
            else:
                message = f"Не существует цитаты под таким номером"
        else:
            message = "Вы ввели не число"
    else:
        message = "Вы не ввели ничего"
    update.message.reply_text(message, reply_markup=my_keyboard)


def random_quote(update, context):
    update.message.reply_text(f"Случайная цитата: '{choice(context.user_data['quotes'])}'", reply_markup=my_keyboard)


def main():
    mybot = Updater("5882954776:AAEzHI7P4l3pgYyl2bYPuB1rA6SDPvGFhig", use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("add_quote", add_quote))
    dp.add_handler(CommandHandler("random_quote", random_quote))
    dp.add_handler(CommandHandler("delete_quote", delete_quote))
    dp.add_handler(CommandHandler("show_quotes", show_quotes))
    logging.info("Bot started")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
