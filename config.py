import os
from dotenv import load_dotenv
from pyrogram import Client, filters
from pytgcalls import PyTgCalls

# For Local Deploy
if os.path.exists(".env"):
    load_dotenv(".env")

API_ID = int(os.getenv("API_ID", "14739610"))
API_HASH = os.getenv("API_HASH", "4bb54a9de1d7b5570ccae74c2689f223")
SESSION = os.getenv("AgDg6JoADJZIY3ftYj0Mf0uOT5bqoUdjrPTIcJV1PDKA0GIVk12_5iWu0uScvWHjkXpNkNqUGnaXAGLRmZ48znqlW7EJqbYWYuxEgpw2IZW-Z9Iuj91TVtKBO13-rCVvPBwn9xtESTQOUtluSm1PNiEdxGh-CDPJBMsW6n2CTKnAIVXiPFE3kjaeLqoVc3fhbky1lgrF8RJkWCARJiySHRul4SsxwEmR058VqJr5attMIq3KB-YxXZ-JvvHMyY-elZg97iPAN_qXUrf8yhI4K4fbqlItmODWeLupMg4fNo-zkBvTGTGVgIHj8CpOjHv2zFtnliVWrPrDhc8BNQzG5KKhsjzpkAAAAAF6rBtIAA")
HNDLR = os.getenv("HNDLR", "!")

contact_filter = filters.create(
    lambda _, __, message:
    (message.from_user and message.from_user.is_contact) or message.outgoing
)

bot = Client(SESSION, API_ID, API_HASH, plugins=dict(root="VCBot"))
call_py = PyTgCalls(bot)
