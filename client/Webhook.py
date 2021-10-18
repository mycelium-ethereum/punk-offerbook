import os
from discord import Webhook, RequestsWebhookAdapter

URL = os.getenv('DISCORD_WEBHOOK')
if URL is not None: webhook = Webhook.from_url(URL, adapter=RequestsWebhookAdapter())
else: webhook = None