import telebot
from pyowm import OWM
from pyowm.utils.config import get_default_config
from keys import bot_api, owm_api

bot = telebot.TeleBot(bot_api)

@bot.message_handler(commands=['start'])
def help(message):
	bot.send_message(message.chat.id, 'Чтобы узнать погоду напишите в чат название города')

@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.chat.id, '/start - запуск бота\n/help - команды бота \nАвтор бота – https://vk.com/danielium \nЧтобы узнать погоду напишите в чат название города')

@bot.message_handler(content_types=['text'])
def test(message):
	try:
		place = message.text

		config_dict = get_default_config()
		config_dict['language'] = 'ru'

		owm = OWM(owm_api, config_dict)
		mgr = owm.weather_manager()
		observation = mgr.weather_at_place(place)
		w = observation.weather

		t = w.temperature("celsius")
		t1 = int(t['temp'])
		t2 = int(t['feels_like'])


		wi = int(w.wind()['speed'])
		humi = w.humidity
		cl = w.clouds
		st = w.status
		dt = w.detailed_status
		ti = w.reference_time('iso')
		pr = w.pressure['press']
		vd = w.visibility_distance


		bot.send_message(message.chat.id, "В городе " + str(place) + " температура: " + str(t1) + " °C" + "\n" +
				"Ощущается как: "  + str(t2) + " °C" + "\n" +
				"Скорость ветра: " + str(wi) + " м/с" + "\n" +
				"Давление: " + str(pr) + " мм.рт.ст" + "\n" +
				"Влажность: " + str(humi) + " %" + "\n" +
				"Осадки: " + str(dt))

		if t1 <= 0:
			bot.send_message(message.chat.id, "Ты точно хочешь пойти на улицу? Сейчас холодно.")
		elif t1 <= 10:
			bot.send_message(message.chat.id, "Сейчас прохладно,  надевай ветровку")
		elif t1 <= 15:
			bot.send_message(message.chat.id, "Сейчас тепло, можешь надеть футблоку, джинсы и легкую кофту")
		elif t1 <= 25:
			bot.send_message(message.chat.id, "Сейчас довольно телпо, надевай футболку и шорты")
		else:
			bot.send_message(message.chat.id, "Сейчас очень жарко, сиди дома под кондиционером")







	except:
		bot.send_message(message.chat.id,"Такой город не найден!")
		print(str(message.text),"- не найден")

bot.polling(none_stop=True, interval=0)