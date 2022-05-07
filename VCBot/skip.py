from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from config import bot, call_py, HNDLR, contact_filter
from VCBot.handlers import skip_current_song, skip_item
from VCBot.queues import QUEUE, clear_queue

@Client.on_message(contact_filter & filters.command(['تخطي'], prefixes=f"{HNDLR}"))
async def skip(client, m: Message):
   chat_id = m.chat.id
   if len(m.command) < 2:
      op = await skip_current_song(chat_id)
      if op==0:
         await m.reply("`ماكو شي مشتغل حبي`")
      elif op==1:
         await m.reply("`قائمة الانتضار فارغة ، تم مغادرة الدردشة الصوتية...`")
      else:
         await m.reply(f"**ابشر عيني المطور** \n**🎧 الان يتخطي** - [{op[0]}]({op[1]})", disable_web_page_preview=True)
   else:
      skip = m.text.split(None, 1)[1]
      OP = "**Removed the following songs from Queue:-**"
      if chat_id in QUEUE:
         items = [int(x) for x in skip.split(" ") if x.isdigit()]
         items.sort(reverse=True)
         for x in items:
            if x==0:
               pass
            else:
               hm = await skip_item(chat_id, x)
               if hm==0:
                  pass
               else:
                  OP = OP + "\n" + f"**#{x}** - {hm}"
         await m.reply(OP)        
      
@Client.on_message(contact_filter & filters.command(['ايقاف', 'كافي'], prefixes=f"{HNDLR}"))
async def stop(client, m: Message):
   chat_id = m.chat.id
   if chat_id in QUEUE:
      try:
         await call_py.leave_group_call(chat_id)
         clear_queue(chat_id)
         await m.reply("**اهلين عيني المطور ابشر تم الايقاف ⏹️**")
      except Exception as e:
         await m.reply(f"**ERROR** \n`{e}`")
   else:
      await m.reply("`لايوجد شي قيد التشغيل`")
   
@Client.on_message(contact_filter & filters.command(['مؤقت'], prefixes=f"{HNDLR}"))
async def pause(client, m: Message):
   chat_id = m.chat.id
   if chat_id in QUEUE:
      try:
         await call_py.pause_stream(chat_id)
         await m.reply("**تم الإيقاف ⏸️**")
      except Exception as e:
         await m.reply(f"**ERROR** \n`{e}`")
   else:
      await m.reply("`ماكو شي مشتغل`")
      
@Client.on_message(contact_filter & filters.command(['استمرار'], prefixes=f"{HNDLR}"))
async def resume(client, m: Message):
   chat_id = m.chat.id
   if chat_id in QUEUE:
      try:
         await call_py.resume_stream(chat_id)
         await m.reply("**تم الاستمرار ▶**")
      except Exception as e:
         await m.reply(f"**ERROR** \n`{e}`")
   else:
      await m.reply("`لايوجد شي قيد التشغيل`")
