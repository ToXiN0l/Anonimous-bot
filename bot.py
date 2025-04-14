import telebot
import pandas as pd
import os
import random as rnd
from datetime import datetime
from telebot import types 
from dadata import Dadata


API_TOKEN = '7843426795:AAFGnULnWuYkOIYF5xge-_wXtO7d53H8yHw'
token = "093d35675f0d2c27f02284067e18d467849433fb"
dadata = Dadata(token)
NAMES = [
    "Александр", "Саша" "Анастасия", "Настя", "Максим", "Мария", "Маша" "Дмитрий", "Дима", "Екатерина", "Катя",
    "Иван", "Ваня", "Ольга", "Оля" "Сергей", "Сережа", "Серёжа" "Наталья", "Наташа", "Артем", "Анна", "Аня",
    "Егор", "Татьяна", "Таня" "Даниил", "Даня", "Данил", "Елена", "Лена", "Павел", "Паша", "Виктория", "Вика",
    "Роман", "Рома", "Светлана", "Света", "Алексей", "Леша", "Лёша", "Ксения", "Ксюша", "Никита", "Юлия", "Юля",
    "Ирина", "Ира", "Станислав", "Стас", "Дарья", "Даша", "Григорий", "Гриша", "Евгения", "Женя",
    "Владимир", "Вова", "Людмила", "Люда", "Константин", "Костя", "Олеся", "Федор", "Федя",
    "Вероника", "Андрей", "Зоя", "Семен", "Сеня", "Алёна", "Алена",
    "Тимофей", "Маргарита", "Рита", "Арсений", "Полина", "Валентин", "Валя",
    "Кирилл", "Лилия", "Лиля", "Ярослав", "Ярик", "София", "Соня", "Софа", "Виктор", "Витя",
    "Радмила", "Валерия", "Лера", "Георгий", "Нина", "Степан", "Степа", "Стёпа", "Игорь", "Радмир", "Денис", 
    "Дмитрий", "Дима"
]
phones_dict = {"+7":"Россия"}
data = None
selected_columns = {}
name_of_file = ''


def personalyze_name(data, degree, flag):
    #имя, фамилия

    for i in range(len(data)):
        if degree == 'Средняя' or degree == "Высокая":
            data.loc[i, flag] = f'Пользователь {i + 1}'
        elif degree == 'Низкая':
            mark = True
            for name in NAMES:
                if name in data.loc[i, flag]:
                    data.loc[i, flag] = name
                    mark = False
                    break
            if mark:
                data.loc[i, flag] = f'Пользователь {i + 1}'
        

    return data


def personalyze_birthday(data, degree, flag):
    for i in range(len(data)):
        cell = data.loc[i, flag].split('.')
        year = int(cell[2])
        month = str(rnd.randint(1, 12))
        day = str(rnd.randint(1, 31))
        month = '0' * (2 - len(month)) + month
        day = '0' * (2 - len(day)) + day
        if degree == 'Низкая':
            data.loc[i, flag] = '.'.join([day, month, str(year)])
        elif degree == 'Средняя':
            current_year = datetime.now().year
            if year + 2 < current_year:
                if year < 14:
                    if year + 2 < 14:
                        year = rnd.choice([year - 2, year + 2])
                    else:
                        year = year - 2
                elif 14 <= year < 18:
                    if year + 2 < 18:
                        if year - 2 >= 14:
                            year = rnd.choice([year - 2, year + 2])
                        else:
                            year = year + 2
                    else:
                        year = year - 2
                else:
                    if year - 2 >= 18:
                        year = rnd.choice([year - 2, year + 2])
                    else:
                        year = year + 2
            else:
                year = year - 2
            
            data.loc[i, flag] = '.'.join([day, month, str(year)])
        elif degree == 'Высокая':
            year = year - year % 10
            data.loc[i, flag] = str(year) + '-е'

    return data



def personalyze_mail(data, degree, flag):
    for i in range(len(data)):
        cell = data.loc[i, flag]
        ind = cell.find('@')
        if degree == 'Низкая':
            data.loc[i, flag] = 'X' * len(cell[:ind]) + '@' + 'X' * len(cell[ind + 1:])
        elif degree == 'Средняя' or degree == "Высокая":
            data.loc[i, flag] = 'X' * len(cell[:ind]) + '@' + cell[ind + 1:]

    return data
    

def personalyze_passport(data, degree, flag):
    for i in range(len(data)):
        cell = data.loc[i, flag]
        series = cell.split()[0]
        number = cell.split()[1]
        current_year = datetime.now().year
        mas = [num % 100 for num in range((current_year + 1) % 100)].extend([97, 98, 99])
        if degree == 'Низкая':
            number = rnd.randint(100000, 999999)
        elif degree == 'Средняя':
            series = series[:2] + '0' * (2 - len(str(rnd.randint(mas)))) + str(rnd.randint(mas))
        elif degree == 'Высокая':
            series = '0' * (len(str(rnd.randint([num for num in range(1, 100)])))) + '0' * (2 - len(str(rnd.randint(mas)))) + str(rnd.randint(mas))
        data.loc[i, flag] = series + ' ' + str(number)

    return data
 

def personalyze_phone(data, degree, flag):
    for i in range(len(data)):
        if degree == 'Низкая':
            obj = list(obj)
            for x in range(7, len(obj) - 2):
                if obj[x] in "+() -":
                    continue
                else:
                    obj[x] = "*"
            data.loc[i, flag] = "".join(obj)
        elif degree == 'Средняя': 
            pass # будем менять номер на провайдера  (пока хз как сделать)
        elif degree == 'Высокая':
            data.loc[i, flag] = phones_dict[obj[:2]]

    return data


def personalyze_address(data, degree, flag):
    print('personalyzing')
    for i in range(len(data)):
        info = dadata.suggest("address", data.loc[i, flag])
        
        if degree == 'Низкая': 
            ukazateli = ["region_with_type", "federal_district", 'postal_code']
        elif degree == 'Средняя': 
            ukazateli =["region_with_type"]
        elif degree == 'Высокая': 
            ukazateli = ["country"]
        new_address = [info[0]["data"][j] for j in ukazateli] 
        for j in range(len(new_address)):
            if new_address[j] == None:
                new_address[j]="missing"
        data.loc[i, flag] = " ".join(new_address)
    return data


def personalyze_telegram_name(data, degree, flag):
    for i in range(len(data)):
        if degree == 'Низкая':
            pass
        if degree == 'Средняя':
            obj = list(obj)
            rnd.shuffle(obj)
            data.loc[i, flag]  = "".join(obj)
        if degree == 'Высокая':
            obj = list(obj)
            for j in range(len(obj)):
                    if str(obj[j]).isdigit() == True: obj[j] = "1"
                    elif str(obj[j]) != str(obj[j]).upper(): obj[j] = "a"
                    else:obj[j] = "A"
            data.loc[i, flag] = "".join(obj)
    
    return data


def personalyze_SNILS(data, degree, flag):
    for i in range(len(data)):
        data.loc[i, flag] = 'X' * 9 + ' ' + 'XX'

    return data


# Инициализация бота

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Как пользоваться ботом?\n-Во-первых, нужно отправить сюда csv-файл с данными\n"
    "-Во-вторых, нужно выбрать столбцы, которые нужно обезличить\n-В-третьих, нужно выбрать степень обезличивания (где низкая - малая степень " \
    "обезличивания, достаточно понятно, о ком речь; средняя - о человеке тяжело будет восстановить информацию; высокая - полная анонимность)\n"
    "*Если будут выбраны все столбцы, бот автоматически завершит процесс выбора требуемых столбцов\n"
    "*По команде /test_table Вы сможете получить базу данных, чтобы опробовать функционал бота")


@bot.message_handler(commands=['test_table'])
def handle_table(message):
    try:
        # Replace 'path/to/your/test_table.csv' with the actual path to your CSV file
        with open('/Users/matveygashenko/workshop/Пробная база данных.csv', 'rb') as file:
            bot.send_document(message.chat.id, file)
            bot.send_message(message.chat.id, "Теперь Вы можете ознакомиться с данными, и для дальнейшей работы отправьте нам её обратно")
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл test_table.csv не найден.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при отправке файла: {e}")


@bot.message_handler(content_types=['document'])
def handle_document(message):
    global data, selected_columns, name_of_file
    # Проверяем, что файл - это CSV
    if message.document.mime_type == 'text/csv':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        name_of_file = message.document.file_name
        
        with open('temp_db.csv', 'wb') as temp_file:
            temp_file.write(downloaded_file)

        # Обрабатываем CSV-файл
        try:
            data = pd.read_csv('temp_db.csv', delimiter=';')
            data.columns = ['_'.join(elem.split()).lower() for elem in data.columns]
            selected_columns = {}
            send_columns(message, data)
            
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка при обработке файла: {str(e)}")
        finally:
            # Удаляем временные файлы
            os.remove('temp_db.csv')
    else:
        bot.send_message(message.chat.id, "Пожалуйста, отправьте файл в формате CSV.")

def send_columns(message, data):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(i) for i in data.columns]
    # buttons.append(types.KeyboardButton("Все столбцы")) 
    buttons.append(types.KeyboardButton("ꜜDONEꜜ"))  # Add a "Done" button
    markup.add(*buttons)
    msg = bot.send_message(
        message.chat.id,
        "Выберите столбцы, которые хотите обезличить (нажмите 'ꜜDONEꜜ', когда закончите):",
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, handle_column_selection)



def handle_column_selection(message):
    global data, selected_columns

    if data is None:
        bot.send_message(message.chat.id, "Сначала отправьте CSV-файл.")
        return
    
    if message.text == "ꜜDONEꜜ":
        if not selected_columns:
            bot.send_message(message.chat.id, "Вы не выбрали ни одного столбца.")
        else:
            ANON(message, data, selected_columns)
            selected_columns = {}
        return
    

    if message.text in data.columns:
        if message.text not in selected_columns:
            selected_columns[message.text] = ''
            bot.send_message(message.chat.id, f"Столбец '{message.text}' добавлен к выбранным.")
            send_degree_selection(message, message.text)  # ask user about degree for selected title
        else:
            bot.send_message(message.chat.id, f"Столбец '{message.text}' уже был выбран.")
        # Keep asking for more selections
            send_columns(message, data)

    elif message.text not in data.columns and message.text != 'ꜜDONEꜜ':
        bot.send_message(message.chat.id, "Пожалуйста, выберите столбец из предложенных.")
        send_columns(message, data)

    if not selected_columns:
        send_columns(message, data)
    elif len(selected_columns) == len(data.columns) or message.text == 'ꜜDONEꜜ':
        for key in selected_columns.keys():
          if selected_columns[key] == '':
            bot.send_message(message.chat.id, f"Сначала нужно выбрать категорию для столбца {key}")
            return
          
        ANON(message, data, selected_columns)


def send_degree_selection(message, column_name):
    """Sends buttons for selecting the degree for a specific column."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    mas = ['Низкая', 'Средняя', 'Высокая']
    buttons = [types.KeyboardButton(i) for i in mas]
    markup.add(*buttons)
    msg = bot.send_message(
        message.chat.id,
        f"Выберите категорию (низкая, средняя или высокая) для столбца '{column_name}':",
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, handle_degree_selection, column_name)


def handle_degree_selection(message, column_name):
    """Handles the user's choice of degree for a specific column."""
    global selected_columns

    if not (message.text.isdigit()) and message.text in ['Низкая', 'Средняя', 'Высокая']:
        selected_columns[column_name] = message.text
        bot.send_message(message.chat.id, f"Выбрана категория {message.text} для столбца '{column_name}'.")
        if len(selected_columns) == len(data.columns):
          for key in selected_columns.keys():
            if selected_columns[key] == '':
              bot.send_message(message.chat.id, f"Сначала нужно выбрать категорию для столбца {key}")
              return
          ANON(message, data, selected_columns)
          return
        send_columns(message, data)

    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите низкая, средняя или ыысокая.")
        send_degree_selection(message, column_name)


def ANON(message, data, selected_columns):
    for name_of_column in selected_columns:
        if name_of_column.lower() == 'фио' or name_of_column.lower().find("имя") != -1 or name_of_column.lower().find('фамилия') != -1 or name_of_column.lower().find('отчество') != -1:
            data = personalyze_name(data, selected_columns[name_of_column], name_of_column)

        elif name_of_column == 'дата_рождения' or name_of_column.lower().find('рожд') != -1:
            data = personalyze_birthday(data, selected_columns[name_of_column], name_of_column)

        elif name_of_column == 'почта' or name_of_column.find('почт') != -1:
            data = personalyze_mail(data, selected_columns[name_of_column], name_of_column)

        elif name_of_column == 'снилс':
            data = personalyze_SNILS(data, selected_columns[name_of_column], name_of_column)

        elif name_of_column == 'паспорт' or name_of_column.find('пасп') != -1:
            data = personalyze_passport(data, selected_columns[name_of_column], name_of_column)

        elif name_of_column == 'телефон' or name_of_column.find("номер") != -1:
            personalyze_phone(data, selected_columns[name_of_column], name_of_column)

        elif name_of_column == 'адрес' or name_of_column == 'место_проживания':
            personalyze_address(data, selected_columns[name_of_column], name_of_column)
        
        elif name_of_column == 'ник_в_телеграмме':
            data = personalyze_telegram_name(data, selected_columns[name_of_column], name_of_column)
        
        else:
            pass
    
    data.to_csv(name_of_file, index=False)

    # Возвращаем файл пользователю
    with open(name_of_file, 'rb') as out_db:
        bot.send_document(message.chat.id, out_db)
    
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Вот ваш CSV-файл.', reply_markup = markup)

# Запуск бота
if __name__ == '__main__':
    print("Bot is running...")
    bot.polling(none_stop=True)