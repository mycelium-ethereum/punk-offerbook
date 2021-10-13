import os
from discord import Webhook, RequestsWebhookAdapter

URL = os.getenv('DISCORD_WEBHOOK')
webhook = Webhook.from_url(URL, adapter=RequestsWebhookAdapter())
