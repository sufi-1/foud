import os
import asyncio
from pyrogram import Client
from VCBot.queues import QUEUE, add_to_queue
from config import bot, call_py, HNDLR, contact_filter
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from youtubesearchpython import VideosSearch


def ytsearch(query):
   try:
      search = VideosSearch(query, limit=1)
      for r in search.result()["result"]:
         ytid = r['id']
         if len(r['title']) > 34:
            songname = r['title'][:35] + "..."
         else:
            songname = r['title']
         url = f"https://www.youtube.com/watch?v={ytid}"
      return [songname, url]
   except Exception as e:
      print(e)
      return 0

# YTDL
# https://github.com/pytgcalls/pytgcalls/blob/dev/example/youtube_dl/youtube_dl_example.py
async def ytdl(link):
   proc = await asyncio.create_subprocess_exec(
       'youtube-dl',
       '-g',
       '-f',
       # CHANGE THIS BASED ON WHAT YOU WANT
       'bestaudio',
       f'{link}',
       stdout=asyncio.subprocess.PIPE,
       stderr=asyncio.subprocess.PIPE,
   )
   stdout, stderr = await proc.communicate()
   if stdout:
      return 1, stdout.decode().split('\n')[0]
   else:
      return 0, stderr.decode()


@Client.on_message(filters.command(['ش'], prefixes=f"{HNDLR}"))
async def play(client, m: Message):
   replied = m.reply_to_message
   chat_id = m.chat.id
   if replied:
      if replied.audio or replied.voice:
         huehue = await replied.reply("`جاري التشغيل...،💗🎧`")
         dl = await replied.download()
         link = replied.link
         if replied.audio:
            if replied.audio.title:
               songname = replied.audio.title[:35] + "..."
            else:
               songname = replied.audio.file_name[:35] + "..."
         elif replied.voice:
            songname = "Voice Note"
         if chat_id in QUEUE:
            pos = add_to_queue(chat_id, songname, dl, link)
            await huehue.edit(f"تم اضافتها الى قائمة الانتضار **#{pos}**")
         else:
            await call_py.join_group_call(
               chat_id,
               AudioPiped(
                  dl,
               ),
               stream_type=StreamType().pulse_stream,
            )
            add_to_queue(chat_id, songname, dl, link)
            await huehue.edit(f"**تم بدء تشغيل الاغنية ،💗🎧** \n**🎧 الاسم** : [{songname}]({link}) \n**ℹ️ معرف الدردشة** : `{chat_id}`", disable_web_page_preview=True)
      else:
         if len(m.command) < 2:
            await m.reply("`الرد على ملف صوتي أو إعطاء شيء للبحث`")
         else:
            huehue = await m.reply("`جاري البحث`")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search==0:
               await huehue.edit("`لم يتم العثور على شيء`")
            else:
               songname = search[0]
               url = search[1]
               hm, ytlink = await ytdl(url)
               if hm==0:
                  await huehue.edit(f"**YTDL ERROR ⚠️** \n\n`{ytlink}`")
               else:
                  if chat_id in QUEUE:
                     pos = add_to_queue(chat_id, songname, ytlink, url)
                     await huehue.edit(f"تم اضافته الى قائمة الانتضار **#{pos}**")
                  else:
                     try:
                        await call_py.join_group_call(
                           chat_id,
                           AudioPiped(
                              ytlink,
                           ),
                           stream_type=StreamType().pulse_stream,
                        )
                        add_to_queue(chat_id, songname, ytlink, url)
                        await huehue.edit(f"**تم بدء تشغيل الاغنية ،💗🎧** \n**🎧 الاسم** : [{songname}]({url}) \n**ℹ️ معرف الدردشة** : `{chat_id}`", disable_web_page_preview=True)
                     except Exception as ep:
                        await huehue.edit(f"`{ep}`")
            
   else:
         if len(m.command) < 2:
            await m.reply("`الرد على ملف صوتي او اعطاء شي للبحث`")
         else:
            huehue = await m.reply("`جاري البحث`")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search==0:
               await huehue.edit("`لم يتم العثور على شي`")
            else:
               songname = search[0]
               url = search[1]
               hm, ytlink = await ytdl(url)
               if hm==0:
                  await huehue.edit(f"**YTDL ERROR ⚠️** \n\n`{ytlink}`")
               else:
                  if chat_id in QUEUE:
                     pos = add_to_queue(chat_id, songname, ytlink, url)
                     await huehue.edit(f"تم اضافته الى الانتضار **#{pos}**")
                  else:
                     try:
                        await call_py.join_group_call(
                           chat_id,
                           AudioPiped(
                              ytlink,
                           ),
                           stream_type=StreamType().pulse_stream,
                        )
                        add_to_queue(chat_id, songname, ytlink, url)
                        await huehue.edit(f"**تم بدء تشغيل الاغنية ،💗🎧** \n**🎧 الاسم** : [{songname}]({url}) \n**ℹ️ معرف الدردشة** : `{chat_id}`", disable_web_page_preview=True)
                     except Exception as ep:
                        await huehue.edit(f"`{ep}`")
