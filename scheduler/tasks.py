# import asyncio
# import json
#
# from celery import shared_task
# from telegram import Bot
# from scheduler.redis_configs import redis_db
#
#
# # async def send():
# #     text = "your alert is triggered\n"
# #     bot = Bot("5515102830:AAFSh_McX1ah0kdpBGDyM40qRmQZtHNEhnc")
# #     # print(user, coins)
# #     # coins = [coin.strip(" ") for coin in coins.split(",")]
# #     # for coin in coins:
# #     #     c = redis_db.get(coin)
# #     #     c = json.loads(c)
# #     #     text += f"{coin} ({c['name']}) => {c['price']}\n"
# #
# #     await bot.send_message(chat_id=1074680699, text=text)
#
# @shared_task
# def send_message(*args, **kwargs):
#     print("hello")
#     # bot = Bot("5515102830:AAFSh_McX1ah0kdpBGDyM40qRmQZtHNEhnc")
#     # bot.send_message(chat_id=1074680699, text="hi")
#     return "hello"