import telebot
from telebot import types
import requests
import pyautogui as pag
import pyperclip
import os
import time
from config import TOKEN, CHAT_ID
client = telebot.TeleBot(TOKEN)

##############################

#################################
class Logs():
    def printl(self,text):
        print(text)

log = Logs()
#################################

requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=Online")
print('Online')
x = 0 #корды мышек, по умолчанию 0, далее мы возьмем их из позиции текущей и прибавим к ним еще корды
y = 0 #


@client.message_handler(commands=['start']) #
def start(message): #добавляет кнопки в меню, каждая кнопка ответсвенна за свою команду
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton()

    item = button('/scr') 
    item2 = button('/p') 
    item3 = button('/l') 
    item4 = button('/r') 
    item5 = button('/ll') 
    item6 = button('/write') 
    item7 = button('/drag') 
    item8 = button('/ent') 
    item9 = button('/b') 
    item10 = button('/knopka')
    
    rmk.add(item, item2, item3, item4, item5, item6, item7, item8, item9, item10) #+ кнопки делаем

    client.send_message(message.chat.id, 'ку', reply_markup=rmk)


# команда scr делает скриншот экрана
@client.message_handler(commands=['scr']) 
def scr(message):
    pag.hotkey('shift', 'prntscrn') #сочитание клавиш для скриншота 
    time.sleep(1) #чтобы не забагалось
    try:# на всяки случай try
        with open('Screenshot_1.png', 'rb') as img: #  открываем файл со скришотом и даем сразу переменную img   
            client.send_photo(message.chat.id, img) #отправляем фото
        time.sleep(1) #чтобы не сломалось
        os.remove('Screenshot_1.png')  #удаляем его
    except:
        client.send_message(message.chat.id, 'Error') #если ошибка, то пишем челу еррор

#для передвижения мышки
@client.message_handler(commands=['p']) 
def pos_x(message):
    msg = client.send_message(message.chat.id, 'Введите координату по Х') #спрашиваем корды
    client.register_next_step_handler(msg, pos_y) #переходим на след функцию

def pos_y(message): 
    global x
    try:
        x = pag.position().x #тут мы прибавляем к нашему текущему положению мышки + еще корды
        x += int(message.text)
    except:
        client.send_message(message.chat.id,'Error X')  
    #запрашиваем корды у
    msg = client.send_message(message.chat.id, 'Введите координату по Y') 
    client.register_next_step_handler(msg, next_step)

def next_step(message):
    global y
    try:
        #тоже самое, что и с х
        y = pag.position().y
        y += int(message.text)
    except:
        client.send_message(message.chat.id,'Error Y')
    log.printl((x, y))

    try:
        pag.moveTo(int(x), int(y), duration=1) #двигаем мышку по кордам
        #если у нас мышка стоит на кордах 1000, 0 (x,y), то мы добавляем к этим кордам, например, еще + 20 по х
        #и становится  1020, 0.
    except:
        client.send_message(message.chat.id, 'Error move')



#оффает пк, кстати имба, если ты забыл оффнуть пк, а идти лень
@client.message_handler(commands=['offpc']) 
def offpc(message):
    client.send_message(message.chat.id, 'Выключаю...')
    os.system('shutdown -s -t 30')

#нажимает левую кнопку мыши
@client.message_handler(commands=['l']) #
def l(message):
    pag.click()
    client.send_message(message.chat.id, 'Left')

#нажимает правую кнопку мыши
@client.message_handler(commands=['r']) #
def r(message):
    pag.click(button='right')
    client.send_message(message.chat.id, 'Right')

#два раза нажимает на лкм(дабл клик)
@client.message_handler(commands=['ll']) #
def ll(message):
    pag.doubleClick()
    client.send_message(message.chat.id, 'Double Left')


#печатает любое сообщение, которое мы введем(не печатает в той программе, которая от имени админа)
@client.message_handler(commands=['write']) #
def write(message):
    msg = client.send_message(message.chat.id, 'Введите текст, который напечатает')
    client.register_next_step_handler(msg, next_write)


#печатаем
def next_write(message):
    msg_text = message.text
    log.printl(msg_text)
    pyperclip.copy(str(msg_text))
    time.sleep(0.2)
    pag.click()
    time.sleep(0.2)
    pag.hotkey('ctrl', 'v')
    log.printl('True')


#крутим колеса вверх или вниз
@client.message_handler(commands=['drag']) #
def drag(message):
    msg = client.send_message(message.chat.id, 'Выберите действие: "Вниз - В" или "Вверх - Вв"')
    client.register_next_step_handler(msg, next_drag)

def next_drag(message):
    text_msg = message.text
    try:
        if str(text_msg) == 'Вв':
            pag.scroll(600)
        elif str(text_msg) == 'В':
            pag.scroll(-600)
    except:
        client.send_message(message.chat.id, 'Error scroll')

#нажимаем ентер
@client.message_handler(commands=['ent']) #
def ent(message):
    client.send_message(message.chat.id, 'Enter')
    pag.press('enter')


#нажимаем бекспейс(стереть)
@client.message_handler(commands=['b'])
def b(message):
    client.send_message(message.chat.id, 'True backspace')
    pag.press('backspace')


#нажимает абсолютно любую кнопку, которую мы введем
@client.message_handler(commands=['knopka'])
def kn(message):
    msg_knop = client.send_message(message.chat.id, 'Введите название кнопки')
    client.register_next_step_handler(msg_knop, next_msg)

def next_msg(message):
    text_m = message.text
    try:
        pag.press(f'{text_m}')
        log.printl('True')
    except:
        client.send_message(message.chat.id, 'Error press button')   
client.polling(none_stop=True)






