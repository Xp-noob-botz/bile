from datetime import datetime, timedelta
from pytz import timezone
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
import requests
from route import web_server
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
        self.start_time = None

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        self.uptime = Config.BOT_UPTIME
        self.start_time = datetime.now()  # Record the bot's start time
        if Config.WEBHOOK:
            app = web.AppRunner(await web_server())
            await app.setup()
            await web.TCPSite(app, "0.0.0.0", Config.PORT).start()
        print(f"{me.first_name} Is Started.....✨️")
        print(f"ʀᴀᴘᴏ https://github.com/AshutoshGoswami24/Rename-Bot")
        print(f"ʀᴀᴘᴏ ᴄʀᴇᴀᴛᴏʀ https://github.com/AshutoshGoswami24")
        
        if Config.LOG_CHANNEL:
            try:
                await self.send_redeploy_message(me)

                # Schedule redeployment after initial runtime + 90 minutes
                await self.schedule_redeploy()

            except Exception as e:
                print(f"Error sending redeploy message: {str(e)}")
                print("Please Make This Is Admin In Your Log Channel")

    async def send_redeploy_message(self, me):
        try:
            curr = datetime.now(timezone("Asia/Kolkata"))
            date = curr.strftime('%d %B, %Y')
            time = curr.strftime('%I:%M:%S %p')
            await self.send_message(Config.REDEPLOY, f"**{me.mention} Is Deploy Successful!!**\n\n📅 Date : `{date}`\n⏰ Time : `{time}`\n🌐 Timezone : `Asia/Kolkata`\n\n🉐 Version : `v{__version__} (Layer {layer})`</b>")
            await self.send_message(Config.SET_TXT, f"**{me.mention} Is Restarted !!**")
            
        except Exception as e:
            print(f"Error sending redeploy message: {str(e)}")

    async def schedule_redeploy(self):
        try:
            # Calculate redeployment time as start_time + 90 minutes
            redeploy_time = self.start_time + timedelta(minutes=60)
            current_time = datetime.now()

            # Calculate initial delay if bot is started after its redeploy time
            initial_delay = max(redeploy_time - current_time, timedelta())

            # Wait initial delay before redeploying for the first time
            await asyncio.sleep(initial_delay.total_seconds())

            while True:
                # Redeploy the app
                await self.redeploy_app()

                # Wait for 90 minutes before redeploying again
                await asyncio.sleep(60 * 60)

        except Exception as e:
            print(f"Error in redeployment schedule: {str(e)}")

    async def redeploy_app(self):
        try:
            print("Redeploying the app...")
            me = await self.get_me()  # Fetch me again to get the updated object
            await self.send_message(Config.REDEPLOY, f"**{me.mention} Is Redeploying !!**")
            response = requests.post(Config.REDEPLOY_URL)
            if response.status_code == 200:
                print("App redeployed successfully!")
                await self.send_message(Config.REDEPLOY, f"**{me.mention} Is Redeploying successfully!!!**")
            else:
                print(f"Failed to redeploy app. Status code: {response.status_code}")
                await self.send_message(Config.REDEPLOY, f"**{me.mention} Is Redeploying Failed!!!**")

        except Exception as e:
            print(f"Error redeploying app: {str(e)}")

# Instantiate and run the Bot
Bot().run()
