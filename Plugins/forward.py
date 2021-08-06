import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import asyncio
from pyrogram import filters
from bot import channelforward
from config import Config 
from bot import autocaption
from database.database import *

@channelforward.on_message(filters.channel)
async def forward(c, m):
    # Forwarding the messages to the channel

    for id in Config.CHANNEL:
       from_channel, to_channel = id.split(":")
       if m.chat.id == int(from_channel):
          await m.forward(int(to_channel), as_copy=True)
          print("Forwarded a message from", from_channel, "to", to_channel)
          asyncio.sleep(1)
# =
usercaption_position = Config.CAPTION_POSITION
caption_position = usercaption_position.lower()


@autocaption.on_message(filters.channel & (filters.document | filters.video | filters.audio ) & ~filters.edited, group=-1)
async def editing(bot, message):
      caption_text = await get_caption(Config.ADMIN_ID)
      if caption_text == None:
          caption_text = Config.CAPTION_TEXT
          if not caption_text:
              return
      caption_text = caption_text.caption
      try:
          if (message.document or message.video or message.audio):
             file_caption = f"**{message.caption}**"
      except:
          pass
      try:
          if caption_position == "top":
             await bot.edit_message_caption(
                 chat_id = message.chat.id, 
                 message_id = message.message_id,
                 caption = caption_text + "\n" + file_caption,
                 parse_mode = "markdown"
             )
          elif caption_position == "bottom":
             await bot.edit_message_caption(
                 chat_id = message.chat.id, 
                 message_id = message.message_id,
                 caption = file_caption + "\n" + caption_text,
                 parse_mode = "markdown"
             )
          elif caption_position == "nil":
             await bot.edit_message_caption(
                 chat_id = message.chat.id,
                 message_id = message.message_id,
                 caption = caption_text, 
                 parse_mode = "markdown"
             ) 
      except:
          pass
              
                   
      
