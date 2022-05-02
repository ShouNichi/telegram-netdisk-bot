import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import os
import logging
import database


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start_callback(update, context):
    user = update.message.from_user
    user_id = user.id
    db_file = str(user_id) + '.db'
    exists = os.path.isfile(db_file)
    if not exists:
        logging.info('Will create db file')
        database.create_db(db_file)
        logging.info('Created db file')
        context.bot.send_message(chat_id=update.effective_chat.id, text="Database created.")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome!")


def help_bot(update, context):
    user = update.message.from_user
    user_id = user.id
    message_chat_id = update.message.chat_id
    logging.info("HELP (%s)" % (user_id,))
    with open('./233.md', 'r', encoding='utf-8') as file:
        context.bot.send_message(chat_id=message_chat_id, text=file.read(), parse_mode=telegram.ParseMode.MARKDOWN)


def list_all(update, context):
    list_sub_directory(update, context)
    list_current_directory(update, context)


def list_current_directory(update, context):
    user = update.message.from_user
    user_id = user.id
    db_file = str(user_id) + '.db'
    current_folder = database.get_current_directory(db_file)
    current_folder_name = database.get_directory_info(db_file, current_folder)[0][0]
    test = database.get_files_by_folder(db_file, current_folder)
    temp = [current_folder_name + ' file list:']
    for p in test:
        temp.append(str(p[0]) + '  $  ' + p[1])
    context.bot.send_message(chat_id=update.effective_chat.id, text='\n'.join(temp))


def list_sub_directory(update, context):
    user = update.message.from_user
    user_id = user.id
    db_file = str(user_id) + '.db'
    current_folder = database.get_current_directory(db_file)
    current_folder_name = database.get_directory_info(db_file, current_folder)[0][0]
    test = database.get_sub_folders(db_file, current_folder)
    temp = [current_folder_name + ' subdirectory:']
    for p in test:
        temp.append(str(p[0]) + '  $  ' + p[1])
    context.bot.send_message(chat_id=update.effective_chat.id, text='\n'.join(temp))


def download_file(update, context):
    user = update.message.from_user
    user_id = user.id
    db_file = str(user_id) + '.db'
    file_hash = database.get_file_hash(db_file, int(context.args[0]))[0][0]
    context.bot.send_document(chat_id=update.effective_chat.id, document=file_hash)


def document_handler(update, context):
    user = update.message.from_user
    user_id = user.id
    db_file = str(user_id) + '.db'
    current_folder = database.get_current_directory(db_file)

    full_name = user.full_name
    username = user.username
    chat_id = update.message.chat_id
    file_name = update.message.document.file_name
    file_hash = update.message.document.file_id
    database.register_file(db_file, user_id, chat_id, full_name, username, file_name, file_hash, current_folder)
    print("file_id: " + str(update.message.document.file_id))
    print("file_name: " + str(update.message.document.file_name))
    context.bot.send_message(chat_id=update.effective_chat.id, text='Get file:' + str(update.message.document.file_name))


def create_folder(update, context):
    user = update.message.from_user
    user_id = user.id
    db_file = str(user_id) + '.db'
    current_folder = database.get_current_directory(db_file)
    database.create_folder(db_file, context.args[0], current_folder)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Success')


def enter_folder(update, context):
    user = update.message.from_user
    user_id = user.id
    db_file = str(user_id) + '.db'
    current_folder = database.get_current_directory(db_file)
    parent_folder_id = database.get_directory_info(db_file, current_folder)[0][1]
    if context.args[0] == '..':
        database.change_current_directory(db_file, parent_folder_id)
    else:
        try:
            if not database.get_directory_info(db_file, int(context.args[0])):
                raise ValueError
            database.change_current_directory(db_file, int(context.args[0]))
            context.bot.send_message(chat_id=update.effective_chat.id, text='Finished.')
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Parameter %s is invalid!' % context.args[0])
    list_sub_directory(update, context)


def main(himitsu):
    updater = Updater(token=himitsu)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.document, document_handler))
    dispatcher.add_handler(CommandHandler("help", help_bot))
    dispatcher.add_handler(CommandHandler("la", list_all))
    dispatcher.add_handler(CommandHandler("ls", list_current_directory))
    dispatcher.add_handler(CommandHandler("ld", list_sub_directory))
    dispatcher.add_handler(CommandHandler("cd", enter_folder))
    dispatcher.add_handler(CommandHandler("mkdir", create_folder))
    dispatcher.add_handler(CommandHandler("start", start_callback))
    dispatcher.add_handler(CommandHandler("dl", download_file))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    '''
    proxy_address = 'IF You need proxy'
    os.environ['http_proxy'] = proxy_address
    os.environ['HTTP_PROXY'] = proxy_address
    os.environ['https_proxy'] = proxy_address
    os.environ['HTTPS_PROXY'] = proxy_address
    '''
    bot_token = 'TOKEN HERE'

    main(bot_token)
