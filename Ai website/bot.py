import threading
import time
import telebot

TOKEN = '8969546003:AAGjJjaAKJcLewi84ZdJUiRd1mgu1rZhOTc'
bot = telebot.TeleBot(TOKEN)

users = {}


def get_user(user_id):
  if user_id not in users:
    users[user_id] = {
        'water': 0,
        'reminder_interval': 0,
        'last_reminded': time.time(),
    }
  return users[user_id]


@bot.message_handler(commands=['start'])
def start_cmd(message):
  get_user(message.from_user.id)
  text = (
      '👋 Сәлем! Мен саған су ішуді ұмытпауға көмектесетін ботпын.\n\n'
      '📜 Командалар тізімі:\n'
      '• /start — Нұсқаулық және сәлемдесу\n'
      '• /setreminder 30 — Ескертуді әр 30 минутқа орнату\n'
      '• /setreminder 60 — Ескертуді әр 60 минутқа орнату\n'
      '• /drank 300 — Ішілген суды қосу (мл)\n'
      '• /status — Бүгінгі прогресті көру'
  )
  bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['setreminder'])
def setreminder_cmd(message):
  user = get_user(message.from_user.id)
  args = message.text.split()

  if len(args) < 2:
    bot.reply_to(
        message, 'Уақытты (минутпен) көрсетіңіз. Мысалы: /setreminder 30'
    )
    return

  try:
    minutes = int(args[1])
    if minutes <= 0:
      user['reminder_interval'] = 0
      bot.reply_to(message, '❌ Ескерту өшірілді.')
    else:
      user['reminder_interval'] = minutes
      user['last_reminded'] = time.time()
      bot.reply_to(
          message, f'✅ Ескерту орнатылды: әр {minutes} минут сайын.'
      )
  except ValueError:
    bot.reply_to(message, 'Сан жазыңыз (мысалы: /setreminder 30).')


@bot.message_handler(commands=['drank'])
def drank_cmd(message):
  user = get_user(message.from_user.id)
  args = message.text.split()

  if len(args) < 2:
    bot.reply_to(message, 'Су мөлшерін жазыңыз. Мысалы: /drank 300')
    return

  try:
    amount = int(args[1])
    if amount <= 0:
      bot.reply_to(message, 'Сан 0-ден үлкен болуы керек.')
      return

    user['water'] += amount
    remaining = max(0, 2000 - user['water'])

    bot.reply_to(
        message,
        f'👍 {amount} мл су қосылды!\n'
        f'💧 Барлығы: {user["water"]} / 2000 мл\n'
        f'🎯 Қалғаны: {remaining} мл',
    )
  except ValueError:
    bot.reply_to(message, 'Сан жазыңыз (мысалы: /drank 300).')


@bot.message_handler(commands=['status'])
def status_cmd(message):
  user = get_user(message.from_user.id)
  water = user['water']
  remaining = max(0, 2000 - water)

  text = (
      f'📊 Бүгінгі су балансыңыз:\n\n'
      f'💧 Ішілгені: {water} мл / 2000 мл\n'
      f'🎯 Қалғаны: {remaining} мл'
  )
  if remaining == 0:
    text += '\nҚұттықтаймыз! Күндік норманы (2 литр) орындадыңыз!'

  bot.send_message(message.chat.id, text)


def reminder_checker():
  while True:
    now = time.time()
    for user_id, data in list(users.items()):
      interval = data['reminder_interval']
      if interval > 0:
        if now - data['last_reminded'] >= interval * 60:
          try:
            bot.send_message(
                user_id, 'Су ішуді ұмытпаңыз! Бір стақан су ішіп алыңыз 💧'
            )
            data['last_reminded'] = now
          except Exception:
            pass
    time.sleep(10)


threading.Thread(target=reminder_checker, daemon=True).start()

if __name__ == '__main__':
  bot.infinity_polling()