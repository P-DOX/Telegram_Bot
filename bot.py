from corona import *
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent

class tbot:
	def __init__(self):
		logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
		self.id=''
		self.updater = Updater(token=self.id, use_context=True)
		self.dispatcher = self.updater.dispatcher
		self.message = 'Hi!! \nI am your friend \nTell me the state whose record you want to see. \nFormat : /input <state> \n eg. /input maharashtra'
		self.error = "I didn't understand !!"
		self.handlers()

	def poll(self):
		self.updater.start_polling()

	def get_data(self,state):
		obj = corona()
		return obj.process(state)
		
	def unknown(self,update,context):
		context.bot.sendMessage(chat_id=update.effective_chat.id, text=self.error)

	def start(self,update,context):
		context.bot.send_message(chat_id=update.effective_chat.id, text=self.message)
	
	def input(self,update, context):
		text = ' '.join(context.args).lower()
		data = self.get_data(text)
		text = data[1]
		context.bot.send_message(chat_id=update.effective_chat.id, text=text)

	def inline_input(self,update, context):
		query = update.inline_query.query
		if not query:
			return
		results = list()
		data = self.get_data(query.lower())
		text = data[1]		
		results.append(
			InlineQueryResultArticle(
		    id=query.upper(),
		    title='Corona info',
		    input_message_content=InputTextMessageContent(text)
			)
			)
		context.bot.answer_inline_query(update.inline_query.id, results)

	def handlers(self):
		start_handler = CommandHandler('start', self.start)
		self.dispatcher.add_handler(start_handler)
		input_handler = CommandHandler('input', self.input)
		self.dispatcher.add_handler(input_handler)
		inline_input_handler = InlineQueryHandler(self.inline_input)
		self.dispatcher.add_handler(inline_input_handler)

		# self.dispatcher.addUnknownTelegramCommandHandler(self.unknown)
		self.poll()


obj = tbot()




