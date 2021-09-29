import logging

from telegram.ext import Updater, CommandHandler

from trash_master_demo import TrashRequester


class TelegramBot:
    def __init__(self) -> None:
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )

        self.logger = logging.getLogger(__name__)
        self.updater = Updater("TOKEN", use_context=True) #TOKEN - from @BotFather 

        self.trash_requester = TrashRequester()

    def create_calendar(self) -> str:
        message = self.trash_requester.get_data()
        text = ""

        for i in message:
            text += f"{i[0]} {i[1]}\n"

        return text

    def reply_calendar(self, update, *args, **kwargs) -> None:
        print(args, kwargs)
        update.message.reply_text(self.create_calendar())

    def reply_hello(self, update, *args, **kwargs):
        update.message.reply_text("Elo mordy!")

    def error(self, update, context):
        self.logger.warning('Update "%s" caused error "%s"', update, context.error)

    def bot_body(self):
        dp = self.updater.dispatcher
        dp.add_error_handler(self.error)
        dp.add_handler(CommandHandler("trash", self.reply_calendar))
        dp.add_handler(CommandHandler("hello", self.reply_hello))

        self.updater.start_polling()
        self.updater.idle()


if __name__ == "__main__":
    bot = TelegramBot()
    bot.bot_body()
