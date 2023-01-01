# This example requires the 'message_content' privileged intent to function.

import discord
import random
import asyncio
import time
from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def main():
  return "Your Bot Is Ready"


def run():
  app.run(host="0.0.0.0", port=8000)


def keep_alive():
  server = Thread(target=run)
  server.start()


keep_alive()


class MyClient(discord.Client):

  async def on_ready(self):
    print(f'Logged in as {self.user} (ID: {self.user.id})')
    print('------')

  async def on_message(self, message):
    # we do not want the bot to reply to itself
    # print(message.author.id) ===> see user id
    if message.author.id == self.user.id:
      return
    if message.content.startswith('$about'):
      await message.channel.send(
        f""""สวัสดีฮ๊าฟ <@{message.author.id}> ผมชื่อ น้องบ๊อกซ์เป็นเพื่อนเล่นของคุณ แต่นี่เป็นแค่ Version DEMO นะของเลยน้อยๆหน่อยนะ คนพัฒนาผมก็เป็นนิสิตแห่งนึงแต่ไม่บอกหรอกว่าที่ไหน แบร่ แต่ถ้าเค้าไม่เหงาเค้าคงไม่เขียนขึ้นมาหรอก เกิดขึ้นได้เพราะความเหงาล้วนๆเลย ToT"""
      )
    if message.content.startswith('$play'):
      await message.channel.send(
        f'สวัสดีงับ <@{message.author.id}> วันนี้อยากเล่นเกมอะไรไหม ? \n เรามีเกมให้เล่นเยอะเลย แต่นี้เป็นเวอร์ชั่น demo เรามีให้เล่นแค่ \n1. ป็อกเด้ง\n2.เกมเดาเลข\n อยากรู้คําสั่งพิมพ์ $help',
        reference=message)
    if message.content.startswith('$help'):
      await message.channel.send(
        '$pok = เกมป๊อกเด้ง ! ! !\n$guess = เกมเดาเลข ! ! !\n$about = เกี่ยวกับบอทตัวนี้',
        reference=message)
    if message.content.startswith('$guess'):
      answer = random.randint(1, 10)
      # print(answer)
      await message.channel.send(
        f'เอาละ <@{message.author.id}> มีโอกาสแค่ 5 ครั้งในการเดานะ ล้มให้ได้ถ้านายแน่จริง'
      )
      for i in range(1, 6):
        time.sleep(1)
        await message.channel.send(f'โอกาสครั้งที่ {i} ')
        await message.channel.send(
          '1 ถึง 10 ไหนเดามาดิ เลขอะไร? ให้เวลา 5 วิ ติ๊กต่อกๆ')

        def is_correct(m):
          return m.author == message.author and m.content.isdigit()

        # print(answer)
        try:
          guess = await self.wait_for('message', check=is_correct,
                                      timeout=5.0)  #รอรับคําตอบ
        except asyncio.TimeoutError:
          return await message.channel.send(
            f'โห่ คิดนานไปหน่อยแพ้แล้วละ ! คําตอบคือ {answer}.',
            reference=message)

        if int(guess.content) == answer:
          await message.channel.send(
            f'เห้ย <@{message.author.id}> เก่งอ่ะยอมแล้ว ! คําตอบคือ {answer}',
            reference=message)
          return
        if i == 5:
          await message.channel.send(
            f'และแล้วผู้ชนะก็คือฉันอีกตามเคย ไว้มาล้มใหม่คราวหน้านะ <@{message.author.id}> ! คําตอบคือ {answer}.',
            reference=message)
        else:
          await message.channel.send(
            f'โห่ เอาหน่อย <@{message.author.id}> ยังไม่ถูกเลย สู้เขา')

    if message.content.startswith('$pok'):
      count_user = 0
      count_bot = 0

      def is_correct(m):
        return m.author == message.author and m.content.isdigit()

      await message.channel.send(
        f'ว่าไงนะ <@{message.author.id}> อยากลองมาดวลกับ Box ปอยเปตคนนี้ก็ไม่บอกมาเริ่มเล่นกันเล้ย ! เราจะดวลกันกี่รอบดี ?'
      )
      round = await self.wait_for('message', check=is_correct)
      await message.channel.send(
        f'เราจะดวลกันทั้งหมด {int(round.content)} รอบนะ ! ! !',
        reference=message)
      time.sleep(1)

      def user_hand():
        user_scr = 0
        user = random.randint(1, 13)
        if user == 11:
          store_user.append("J")
          user_scr += 10
        if user == 12:
          store_user.append("K")
          user_scr += 10
        if user == 13:
          store_user.append("Q")
          user_scr += 10
        if user < 11:
          user_scr += user
          store_user.append(user)
        return user_scr

      def bot_hand():
        bot_scr = 0
        bot = random.randint(1, 13)
        if bot == 11:
          store_bot.append("J")
          bot_scr += 10
        if bot == 12:
          store_bot.append("K")
          bot_scr += 10
        if bot == 13:
          store_user.append("Q")
          bot_scr += 10
        if bot < 11:
          bot_scr += bot
          store_bot.append(bot)
        return bot_scr

      def result(user, bot, store_user, store_bot):
        i = 0
        if len(store_user) == 3:
          if (store_user[i] == "J" or store_user[i] == "K"
              or store_user[i] == "Q") and (
                store_user[i + 1] == "J" or store_user[i + 1] == "K"
                or store_user[i + 1] == "Q") and (store_user[i + 2] == "J"
                                                  or store_user[i + 2] == "K"
                                                  or store_user[i + 2] == "Q"):
            status = 1
            # print("User Win yell")
            return status
          if (store_user[i] == store_user[i + 1] == store_user[i + 2]):
            if user > bot:
              status = 2
              # print("User Win tong")
              return status
        if len(store_bot) == 3:
          if (store_bot[i] == "J" or store_bot[i] == "K" or store_bot[i]
              == "Q") and (store_bot[i + 1] == "J" or store_bot[i + 1] == "K"
                           or store_bot[i + 1] == "Q") and (
                             store_bot[i + 2] == "J" or store_bot[i + 2] == "K"
                             or store_bot[i + 2] == "Q"):
            status = 3
            # print("Bot Win yell")
            return status
          if (store_bot[i] == store_bot[i + 1] == store_bot[i + 2]):
            if bot > user:
              status = 4
              # print("Bot Win tong")
              return status
        if user > bot:
          status = 5
          # print("user win")
          return status
        if bot > user:
          status = 6
          # print("Bot Win")
          return status
        if bot == user:
          status = 7
          # print("Draw")
          return status

      for j in range(int(round.content)):
        store_bot = []
        store_user = []
        user_scr = 0
        bot_scr = 0
        await message.channel.send(
          f"---------------------------------------------")
        time.sleep(1)
        await message.channel.send(f"รอบที่ {j+1} \n", reference=message)
        for i in range(2):
          user_scr += user_hand()
        if user_scr >= 10:
          user_scr = user_scr % 10
        for i in range(2):
          bot_scr += bot_hand()
        if bot_scr >= 10:
          bot_scr = bot_scr % 10
        time.sleep(1)
        await message.channel.send(
          f"<@{message.author.id}> มี {user_scr} แต้มและตอนนี้ถือไพ่ {store_user}",
          reference=message)
        # print(f"user ตอนนี้มี {user_scr} แต้มและตอนนี้ถือไพ่ {store_user}")
        # print(f"bot ตอนนี้มี {bot_scr} แต้มและตอนนี้ถือไพ่ {store_bot}")
        if user_scr == 8 or user_scr == 9:
          if user_scr >= bot_scr:
            time.sleep(1)
            await message.channel.send(f"---สรุปผลการแข่งขันรอบที่ {j+1} !---",
                                       reference=message)
            time.sleep(1)
            await message.channel.send(
              f"เห้ย <@{message.author.id}> ชนะแบบ ป็อกเลยเหรอ",
              reference=message)
            time.sleep(1)
            await message.channel.send(
              f"น้องบ๊อกซ์ ตอนนี้มี {bot_scr} แต้มและตอนนี้ถือไพ่ {store_bot}",
              reference=message)
            count_user += 1
            continue
        if bot_scr == 8 or bot_scr == 9:
          if user_scr <= bot_scr:
            time.sleep(1)
            await message.channel.send(f"---สรุปผลการแข่งขันรอบที่ {j+1} !---",
                                       reference=message)
            time.sleep(1)
            await message.channel.send(
              f"บ๊อกซ์ๆ กับ ป๊อกๆ มันเป็นของคู่กันอยู่แล้ว ! ! ! บ๊อกซ์ได้ {bot_scr} และ ถือ {store_bot}",
              reference=message)
            time.sleep(1)
            await message.channel.send(
              f"<@{message.author.id}> ตอนนี้มี {user_scr} แต้มและตอนนี้ถือไพ่ {store_user}",
              reference=message)
            count_bot += 1
            continue
        time.sleep(1)
        await message.channel.send(
          f'<@{message.author.id}> เอาไพ่เพิ่มไหม 1 เอา หรือ 2 ไม่เอา: ')
        a = await self.wait_for('message', check=is_correct)
        if int(a.content) == 1:
          user_scr += user_hand()
          if user_scr >= 10:
            user_scr = user_scr % 10

        if bot_scr < 5:
          bot_scr += bot_hand()
          if bot_scr >= 10:
            bot_scr = bot_scr % 10

        status = result(user_scr, bot_scr, store_user, store_bot)
        time.sleep(1)
        await message.channel.send(f"---สรุปผลการแข่งขันรอบที่ {j+1} !---",
                                   reference=message)
        time.sleep(1)
        await message.channel.send(
          f"<@{message.author.id}> มี {user_scr} แต้มและตอนนี้ถือไพ่ {store_user}"
        )
        time.sleep(1)
        await message.channel.send(
          f"น้องบ๊อกซ์ ตอนนี้มี {bot_scr} แต้มและตอนนี้ถือไพ่ {store_bot}",
          reference=message)
        # ใช้ Switchcase ได้ นะ แต่พอไปรันบนเซิฟมัน error เลยใช้ if else แทน
        if status == 1:
          time.sleep(1)
          await message.channel.send(
            f"เห้ย <@{message.author.id}> ชนะแบบ ขอบเหลืองเลยเหรอ ! ! !",
            reference=message)
          count_user += 1
        elif status == 2:
          time.sleep(1)
          await message.channel.send(
            f"เห้ย <@{message.author.id}> ชนะแบบ ตองเลยเหรอ ! ! !",
            reference=message)
          count_user += 1
        elif status == 3:
          time.sleep(1)
          await message.channel.send(
            f"ฝีมือป่ะละ น้องบ๊อกซ์ ชนะแบบขอบเหลืองด้วยอ่ะฝีมือไง",
            reference=message)
          count_bot += 1
        elif status == 4:
          time.sleep(1)
          await message.channel.send(
            f"ฝีมือป่ะละ น้องบ๊อกซ์ ชนะแบบตองด้วยอ่ะฝีมือไง",
            reference=message)
          count_bot += 1
        elif status == 5:
          time.sleep(1)
          await message.channel.send(
            f"บ้าจริง น้องบ๊อกซ์ แพ้ <@{message.author.id}> ซะได้ ToT",
            reference=message)
          count_user += 1
        elif status == 6:
          time.sleep(1)
          await message.channel.send(f"เป็นยังไงละ น้องบ๊อกซ์ ชนะใสๆ ^.^",
                                     reference=message)
          count_bot += 1
        elif status == 7:
          time.sleep(1)
          await message.channel.send(
            f"คนเท่ๆ เค้ามักจะเสมอกันอย่างนี้แหละ ! ! !", reference=message)
          count_bot += 1
          count_user += 1
    time.sleep(1)
    await message.channel.send(
      f"สรุปผล <@{message.author.id}> ได้ {count_user} แต้ม น้องบ๊อกซ์ {count_bot} แต้ม สนุกมากๆเลยไว้มาเล่นกันใหม่นะ",
      reference=message)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(
  'TOKEN HERE')
