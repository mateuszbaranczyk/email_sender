import logging

from telegram.ext import CommandHandler, Updater

from trash_master_demo import TrashRequester


class TelegramBot:
    def __init__(self) -> None:
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )

        self.logger = logging.getLogger(__name__)
        self.updater = Updater(
            "TELEGRAM:TOKEN", use_context=True
        )

        self.trash_requester = TrashRequester()

    def _create_whole_message(self):
        self.trash_requester.get_data()
        self.trash_requester.convert_confusing_type()

        return self._convert_message_to_str(self.trash_requester.schedule)

    def _create_short_message(self):
        self.trash_requester.get_data()
        self.trash_requester.convert_confusing_type()
        self.trash_requester.create_short_list()

        return self._convert_message_to_str(self.trash_requester.short_list)

    def _convert_message_to_str(self, data) -> str:
        text = ""

        for i in data:
            text += f"{i[0]} {i[1]}\n"

        return text

    def reply_schedule(self, update, *args, **kwargs) -> None:
        print(args, kwargs)
        update.message.reply_text(self._create_short_message())

    def reply_whole_schedule(self, update, *args, **kwargs) -> None:
        print(args, kwargs)
        update.message.reply_text(self._create_whole_message())

    def reply_hello(self, update, *args, **kwargs):
        update.message.reply_text("Elo mordy!")

    def error(self, update, context):
        self.logger.warning('Update "%s" caused error "%s"', update, context.error)

    def bot_body(self):
        dp = self.updater.dispatcher
        dp.add_error_handler(self.error)
        dp.add_handler(CommandHandler("trash", self.reply_schedule))
        dp.add_handler(CommandHandler("trashall", self.reply_whole_schedule))
        dp.add_handler(CommandHandler("hello", self.reply_hello))

        self.updater.start_polling()
        self.updater.idle()


if __name__ == "__main__":
    bot = TelegramBot()
    bot.bot_body()
