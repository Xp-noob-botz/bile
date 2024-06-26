from datetime import datetime
from pytz import timezone
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
from route import web_server
import requests
import asyncio

class Bot(Client):

    def __init__(self):
        super().__init__(
            name="renamer",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username  
        self.uptime = Config.BOT_UPTIME     
        if Config.WEBHOOK:
            app = web.AppRunner(await web_server())
            await app.setup()       
            await web.TCPSite(app, "0.0.0.0", Config.PORT).start()     
        print(f"{me.first_name} Is Started.....✨️")
        print(f"ʀᴀᴘᴏ https://github.com/AshutoshGoswami24/Rename-Bot")
        print(f"ʀᴀᴘᴏ ᴄʀᴇᴀᴛᴏʀ https://github.com/AshutoshGoswami24")
        
        if Config.LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(Config.REDEPLOY, f"**{me.mention} Is Restarted !!**\n\n📅 Date : `{date}`\n⏰ Time : `{time}`\n🌐 Timezone : `Asia/Kolkata`\n\n🉐 Version : `v{__version__} (Layer {layer})`</b>")
                await self.send_message(Config.SET_TXT, f"**{me.mention} Is Restarted !!**\n\n📅 Date : `{date}`\n⏰ Time : `{time}`\n🌐 Timezone : `Asia/Kolkata`\n\n🉐 Version : `v{__version__} (Layer {layer})`</b>")
                
                # Add redeployment after 90 minutes
                await self.schedule_redeploy()

            except Exception as e:
                print(f"Error sending redeploy message: {str(e)}")
                print("Please Make This Is Admin In Your Log Channel")

    async def schedule_redeploy(self):
        # Function to schedule redeployment after 90 minutes
        while True:
            try:
                await asyncio.sleep(5400)  # Sleep for 90 minutes (90 * 60 = 5400 seconds)
                await self.redeploy_app()

            except Exception as e:
                print(f"Error in redeployment schedule: {str(e)}")

    async def redeploy_app(self):
        try:
            print("Redeploying the app...")
            await self.send_message(Config.REDEPLOY, f"**{me.mention} Is Redeploying !!`</b>")
            response = requests.post(Config.REDEPLOY_URL)
            if response.status_code == 200:
                print("App redeployed successfully!")
                await self.send_message(Config.REDEPLOY, f"**{me.mention} Is Redeploying successfully!!!`</b>")
            else:
                print(f"Failed to redeploy app. Status code: {response.status_code}")
                await self.send_message(Config.REDEPLOY, f"**{me.mention} Is Redeploying Failed!!!`</b>")

        except Exception as e:
            print(f"Error redeploying app: {str(e)}")

# Instantiate and run the Bot
Bot().run()
