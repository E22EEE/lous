from pyrogram import Client as app, filters
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
from kvsqlite.sync import Client

db = Client("data.sqlite", 'fuck')

@app.on_callback_query(filters.regex("^invite$"))
async def invte_call(app, query):
    keys = mk(
        [
            [btn(text='مشاركة رابط الدعوة', callback_data='sharelink'), btn(text='هدية يومية', callback_data='dailygift')],
            [btn(text='تسليم ارقام', user_id=5108562302)],
            [btn(text='رجوع', callback_data='back_home')],
        ]
    )
    rk = """
مرحبا بك في خدمات لاين ⦅ تجميع الرصيد ⦆ 
هنالك ثلاث طرق لتجميع الرصيد ✰
 1 -  رابط الدعوة ⥋ 
 2 - تسليم ارقام تليجرام للمطور 
3 - الهدية اليومية 🎁
    """
    await query.edit_message_text(rk, reply_markup= keys)
@app.on_callback_query(filters.regex("^account$"), group=2)
async def acc(app, query):
    keys = mk(
        [
            [btn('تواصل', user_id=1354518673)],
            [btn('رجوع', 'back_home')]
        ]
    )
    info = db.get(f"user_{query.from_user.id}")
    if info:
        coins = info['coins']
        users = len(info['users'])
        prem = 'مدفوع' if info['premium'] == True else 'مجاني'
        rk = f"""
⥳ معلومات حسابك 
⥃ رصيد حسابك الان ⤶ USD {coins}
⥃ عدد مشاركتك لرابط الدعوه ⤶ {users}
⥃ نوع اشتراكك الان ⤶ {prem}
———
        """
        await query.edit_message_text(rk, reply_markup=keys)
    else:
        return
@app.on_callback_query(filters.regex("^buy$"))
async def b(app, query):
    rk  = """
⥃ لشراء الرصيد من بوت الخدمات 
 ➥ 5k ⥂ 20.000 USD                                     
➥ 10k ⥂ 40.000 USD                       
➥ 15k ⥂ 30.000 USD                   
➥ 30k ⥂ 50.000 USD                   
⥈⥈⥈⥈⥈⥈⥈⥈⥈⥈⥈⥈⥈⥈⥈⥈⥈⥈
اسعار الاشتراكات الـ داخل البوت 
⥳ اشتراك لمدة 7 ايام ⤶ 1$ | 4k
 ⥳ اشتراك لمدة 15 ايام ⤶ 4$ | 20k
———————————————————
⤂ طرق الدفع 
نقاط | رصيد | كاش 
    """
    keys = mk(
        [
            [btn(text='تواصل مع المطور', user_id=1354518673)],
            [btn('رجوع', 'back_home')]
        ]
    )
    await query.edit_message_text(rk, reply_markup=keys)
@app.on_callback_query(filters.regex("^trans$"))
async def transs(app, query):
    user_info = db.get(f"user_{query.from_user.id}")
    await app.delete_messages(query.message.chat.id, query.message.id)
    ask1 = await app.ask(query.from_user.id,"⤾ قم بارسال ⦗𝚒𝚍 ⦘ العضو المراد تحويل النقاط اليه ♯", filters.user(query.from_user.id))
    try:
        ids = int(ask1.text)
    except:
        await ask1.reply("تأكد يكون رقم!!، عيد العملية..")
        return
    if not db.exists(f'user_{ids}'):
        keys = mk(
        [
            [btn('رجوع', 'back_home')]
        ]
    )
        await ask1.reply("عذراً، هذا الايدي مو موجود ضمن بياناتنا", reply_markup=keys)
        return
    else:
        keys = mk(
        [
            [btn('رجوع', 'back_home')]
        ]
    )
        ask2 = await app.ask(query.from_user.id,"ارسل المبلغ الي تبي تحوله ?", filters.user(query.from_user.id))
        try:
            amount = int(ask2.text)
        except:
            await ask2.reply("تاكد يكون رقم، عيد العملية!")
            return
        if amount <1:
            await ask2.reply("المبلغ جدا صغير!!", reply_markup=keys)
            return
        if amount >= int(user_info['coins']):
            await ask2.reply("المبلغ كلش جبير، او يساوي مبلغ حسابك. او معندك ياه. قلله.",reply_markup=keys)
        else:
            to_user = db.get(f"user_{ids}")
            to_user['coins'] = int(to_user['coins']) + int(amount)
            user_info['coins'] = int(user_info['coins']) - int(amount)
            db.set(f"user_{ids}", to_user)
            db.set(f"user_{query.from_user.id}", user_info)
            await app.send_message(chat_id=ids, text=f"وصلك حوالة..\nالمبلغ: {amount} دولار .\nمن : {query.from_user.mention} | {query.from_user.id} .\nرصيدك هسه: {to_user['coins']} .")
            await ask2.reply(f"تمت عملية التحويل!!\nالمبلغ: {amount} دولار .\nمن : {query.from_user.mention} | {query.from_user.id} .\nالى : {ids} .\nرصيدك هسه: {user_info['coins']} ", reply_markup=keys)
            return
@app.on_callback_query(filters.regex("^service$"))
async def service(app, query):
    keys = mk(
        [
            [btn(text='⦗ خدمات الرشق الـ ᴠɪᴘ ⦘', callback_data='vips'), btn(text='⦗خدمات الرشق المجانيه', callback_data='frees')],
            [btn(text='رجوع', callback_data='back_home')],
        ]
    )
    rk = """
⥃ مرحبا بك عزيزي في بوت لاين  خدمات ♯ 
هنالك نوعين من الخدمات العادي و الـ المدفوع ✰
    """
    await query.edit_message_text(rk, reply_markup=keys)
    return