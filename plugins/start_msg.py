from pyrogram import Client as app, filters
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from kvsqlite.sync import Client

db = Client("data.sqlite", 'fuck')

@app.on_message(filters.private & filters.regex("^/start$"), group=1)
async def startm(app, msg):
    user_id = msg.from_user.id
    if db.get("ban_list") is None:
        db.set('ban_list', [])
        pass
    if user_id in db.get("ban_list"):
        return
    if db.exists(f"user_{user_id}"):
        coin = db.get(f'user_{user_id}')['coins']
        keys = mk(
        [
            [btn(text='عدد نقاطك: {:,} USD'.format(coin), callback_data='lol')],
            [btn(text='⦅ الخدمات ⦆', callback_data='service')],
            [btn(text='⦅ تجميع نقاط ⦆', callback_data='invite'), btn(text='⦅ شراء النقاط ⦆', callback_data='buy')],
            [btn(text='⦅ معلومات  ⦆', callback_data='account'), btn(text='⦅ تحويل ⦆', callback_data='trans')],
            [btn(text='قناة البوت', url='https://t.me/LINE1_SERVICES')]
        ]
    )
        rk = f'''
⥃ مرحبا بك عزيزي في بوت لاين طلباتكم الخدمات ♯ 
هنالك نوعين من الخدمات العادي و الـ مدفوع ✰
⥃ البوت يتميز بسرعة تنفيذ الطلبات ⥉
الـ 𝚒𝚍 الخاص بك ⥃ {msg.from_user.id}
        '''
        await app.send_message(msg.from_user.id,rk, reply_markup=keys)
    else:
        info = {'coins': 0 , 'id': user_id, 'premium': False, 'admin': False, "phone":[], "users":[], "date":str(time.time())}
        db.set(f'user_{user_id}', info)
        await app.send_message(chat_id=1354518673,text=f"عضو جديد فات للبوت!!\n{msg.from_user.mention} .\nايدي: {msg.from_user.id} .")
        
        coin = db.get(f'user_{user_id}')['coins']
        keys = mk(
        [
            [btn(text='نقاطك: :,{} USD'.format(coin), callback_data='none')],
            [btn(text='الخدمات', callback_data='service')],
            [btn(text='تجميع نقاط', callback_data='invite'), btn(text='شراء نقاط', callback_data='buy')],
            [btn(text='معلومات حسابك', callback_data='account'), btn(text='تحويل ', callback_data='trans')],
            [btn(text='قناة البوت', url='https://t.me/LINE1_SERVICES')]
        ]
    )
        rk =f'''
⥃ مرحبا بك عزيزي في بوت لاين خدمات تيليجرام ♯
هنالك نوعين من الخدمات العادي و الـ مدفوع ✰
⥃ البوت يتميز بسرعة تنفيذ الطلبات ⥉
الـ 𝚒𝚍 الخاص بك ⥃ {msg.from_user.id}
        '''
        await app.send_message(msg.from_user.id,rk, reply_markup=keys)
