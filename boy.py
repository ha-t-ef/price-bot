import asyncio
import requests
from telegram import Bot
from telegram.constants import ParseMode
from datetime import datetime
from httpx import Timeout, AsyncClient
from tenacity import retry, stop_after_attempt, wait_fixed

# اطلاعات بات
BOT_TOKEN = '6996544472:AAH1b8OY4EK8vTvdYy_JFJJe-8fTAyo9z70'
CHANNEL_ID = '-1002152863805'  # یا اگر یوزرنیم کانال داری، مثلا: '@MyCryptoChannel'

bot = Bot(token=BOT_TOKEN)

# تنظیم تایم‌اوت برای درخواست‌ها
timeout = Timeout(10.0)  # تایم‌اوت 10 ثانیه

# تابع ارسال مجدد با Retry
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def send_message_with_retry(price_text):
    await bot.send_message(chat_id=CHANNEL_ID, text=price_text, parse_mode=ParseMode.HTML)

# دریافت قیمت USDT
async def get_usdt_price():
    url = 'https://api.bitpin.ir/api/v1/mkt/tickers/'
    try:
        response = requests.get(url)
        data = response.json()

        for market in data:
            if market['symbol'] == 'USDT_IRT':
                price = float(market['price'])
                now = datetime.now().strftime("%H:%M")
                price_10 = price * 10
                price_100 = price * 100

                message = f"""
💸 قیمت لحظه‌ای تتر: {price:,.0f} تومان
🔟 قیمت ۱۰ تتر: {price_10:,.0f} تومان
💯 قیمت ۱۰۰ تتر: {price_100:,.0f} تومان
🕒 ساعت: {now}
📢 @priceeee8
Hotellry❤
                """.strip()
                return message
        return "❌ بازار USDT_IRT پیدا نشد."
    except Exception as e:
        return f"⚠️ خطا در دریافت قیمت: {e}"

# حلقه ارسال قیمت
async def send_price_loop():
    while True:
        price_text = await get_usdt_price()
        await send_message_with_retry(price_text)  # ارسال پیام با Retry
        await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(send_price_loop())
