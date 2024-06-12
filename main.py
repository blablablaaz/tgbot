import json
import random

from telegram.ext import CommandHandler, MessageHandler, Updater, Filters

with open('test.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)['test']


    def start(update, context):
        context.user_data['count'] = 0
        context.user_data['score'] = 0
        context.user_data['asked'] = []
        random.shuffle(questions)
        update.message.reply_text('Привет! Я бот для проверки твоих знаний. Готов начать? /ask')


def ask(update, context):
    user_data = context.user_data
    while True:
        q = random.choice(questions)
        if q['question'] not in user_data['asked']:
            user_data['asked'].append(q['question'])
            break
    update.message.reply_text(q['question'])



def answer(update, context):
    user_data = context.user_data
    last_question = user_data['asked'][-1]
    for q in questions:
        if q['question'] == last_question:
            if q['response'].lower() == update.message.text.lower():
                user_data['score'] += 1
                update.message.reply_text('Верно!')
            else:
                update.message.reply_text('Неверно. Правильный ответ: {}'.format(q['response']))
            user_data['count'] += 1

    if len(user_data['asked']) != len(questions):
        ask(update, context)
    print(update.message.text.lower())
    if len(user_data['asked']) == len(questions) and len(questions) == user_data['count']:
        update.message.reply_text(
            'Тест завершен. Правильных ответов: {}. ваш IQ = 20. Хочешь пройти еще раз? /start'.format(
                user_data['score']))
        return





updater = Updater('7365323940:AAFebdXiHcmpjhghuVjFZrjqKmuC40J7vZw' , use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('ask', ask))
updater.dispatcher.add_handler(MessageHandler(Filters.text, answer))
updater.start_polling()
updater.idle()
