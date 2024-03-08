import discord
from discord import Embed
import asyncio
import random


client = discord.Client(intents=discord.Intents.all())

allow_send_message = True
room_links = {}

random_questions = [
    "**ما هي الأماكن التي ترغب في زيارتها في العطلات القادمة مع العائلة؟**"
]

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    global allow_send_message

    if message.author == client.user:
        return

        room_links[message.channel.id] = reactions

    if message.content.startswith('-send'):
        if allow_send_message:
            mentioned_user = message.mentions[0]
            content = ' '.join(message.content.split()[2:])
            await mentioned_user.send(content)
            sent_message = await message.channel.send(f'تم ارسال الرسالة الى {mentioned_user.mention}')
            await asyncio.sleep(1)
            await message.delete()
            await sent_message.delete()
        else:
            await message.channel.send("عذرا، تم تعطيل إمكانية إرسال الرسائل في هذا الروم.")

    if message.content == '-اوامر':
        admin_commands = [
            ("`-send`", "لأرسال رسالة في الخاص للمستخدم"),
            ("`+room`", "لأنشاء غرفة جديدة في الخادم بسهولة"),
            ("`-room`", "لحذف الغرفة بكل سهولة"),
            ("`-delete`", "لحذف عدد معين من الرسائل من الغرفة"),
            ("`-off`", "لتعطيل امكانية الأرسال في الغرفة"),
            ("`-on`", "لتشغيل امكانية الأرسال في الغرفة"),
            ("`-role`", "لأعطاء رتبة لشخص آخر في الخادم")
        ]

        entertainment_commands = [
            ("`-ct`", "للرد على أسئلة البوت الممتعة")
        ]

        admin_commands_desc = "\n".join([f"🤖  I {command} امر\n❔  I {description}" for command, description in admin_commands])
        entertainment_commands_desc = "\n".join([f"🤖  I {command} امر\n❔  I {description}" for command, description in entertainment_commands])

        embed = discord.Embed(
            title="قائمة الأوامر",
            color=discord.Color.blue()
        )
        embed.add_field(name="**__                          الأوامـــر الأشرافــية                                      __**", value=admin_commands_desc, inline=False)
        embed.add_field(name="**__                            الأوامـــر الـتـرفـيـهـيـة                                  __**", value=entertainment_commands_desc, inline=False)
        sent_message = await message.channel.send(embed=embed)
        await sent_message.add_reaction('<a:heart:1174352342473257161>')

    if message.content.startswith('+room'):
        room_name = ' '.join(message.content.split()[1:])
        guild = message.guild
        if guild:
            new_channel = await guild.create_text_channel(name=room_name)
            await new_channel.send(f'**تــم انــشــاء الــغــرفـــة** {message.author.mention if message.author else "Unknown User"} <a:verfiy:1174721067420483604>')

    if message.content.startswith('-room'):
        if isinstance(message.channel, discord.TextChannel):
            await message.channel.delete()

    if message.content.startswith('-delete'):
        try:
            num_messages = int(message.content.split()[1])
            deleted_messages = 0
            async for msg in message.channel.history(limit=num_messages):
                await msg.delete()
                deleted_messages += 1
            delete_msg = await message.channel.send(f'تــم حــذف {deleted_messages} رســائل <a:board:1172528917840670750>')
            await asyncio.sleep(1)
            await delete_msg.delete()
        except ValueError:
            await message.channel.send("يرجى تقديم عدد صحيح من الرسائل للحذف.")

    if message.content.startswith('-on'):
        allow_send_message = True
        await message.channel.set_permissions(message.guild.default_role, send_messages=True)
        await message.channel.send("**تـم تـمـكـيـن إمـكانـيـة الأرســال فـي هـذي الـغـرفة** <a:verfiy:1174721067420483604>")

    if message.content.startswith('-off'):
        allow_send_message = False
        await message.channel.set_permissions(message.guild.default_role, send_messages=False)
        await message.channel.send("**تـم تـعـطـيـل إمـكانـيـة الأرســال فـي هـذي الـغـرفـة** <a:verfiy:1174721067420483604>")

    if message.content.startswith('-role'):
        try:
            # يجب استخدام الـ mention كمعرف للمستخدم والرتبة
            user_mention, role_mention = message.content.split()[1:3]
            # يتم استخراج المستخدم من الـ mention
            user_id = int(user_mention.strip('<@!>'))
            user = message.guild.get_member(user_id)
            # يتم استخراج الرتبة من الـ mention
            role_id = int(role_mention.strip('<@&>'))
            role = discord.utils.get(message.guild.roles, id=role_id)
            # إعطاء الرتبة للمستخدم المحدد
            await user.add_roles(role)
            await message.channel.send(f"تـم اعـطـاء رتــبــة {role.mention} لـلـمـسـتـخـدم {user.mention} بـنـجـاح <a:verfiy:1174721067420483604>")
        except Exception as e:
            await message.channel.send("حدث خطأ أثناء محاولة إضافة الرتبة. يرجى التأكد من استخدام الصيغة الصحيحة للأمر.")

    if message.content.startswith('-add_line'):
        room_id = message.content.split()[1]
        room_links[message.author.id] = room_id
        await message.channel.send(f"تم تعيين الغرفة رقم {room_id}")

    if message.content.startswith('-server'):
        guild = message.guild
        embed = Embed(
            title=f"معلومات السيرفر: {guild.name}",
            description=f"صورة السيرفر:",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=guild.icon_url)  # إضافة صورة السيرفر
        await message.channel.send(embed=embed)
        await message.channel.send("سس")  # إرسال النص "سس"

    if message.content.startswith('-warn'):
        if len(message.mentions) > 0:
            warned_user = message.mentions[0]
            reason = ' '.join(message.content.split()[2:])
            # إرسال رسالة تأكيد التحذير في القناة العامة
            await message.channel.send(f'تم التحذير عن المستخدم {warned_user.mention}')
            # إرسال رسالة في الخاص للمستخدم المحذر
            embed = Embed(
                title="__**لـقـد تـم تـحـذيـرك <a:678454765721747466:1213525949342290072>**__",
                description=f"{reason}\n\nتم تحذيرك من قبل هذا السيرفر :  **{message.guild.name}**",
                color=discord.Color.gold()
            )
            await warned_user.send(embed=embed)
        else:
            await message.channel.send("يرجى تحديد المستخدم الذي تريد تحذيره.")

    if message.content.startswith('-delete_dm'):
        async for msg in message.author.history(limit=None):
            if msg.type == discord.MessageType.default and msg.author != client.user:
                await msg.delete()
        await message.channel.send("تم حذف جميع الرسائل في الرسائل الخاصة.")

    if message.content.startswith('-ct'):
        # ارسال ايمبد عشوائي من القائمة
        question = random.choice(random_questions)
        embed = discord.Embed(
            title="ســوأل عــشــوائـي / Nital <a:emoji_55:1211541371916259328>",
            description=question,
            color=discord.Color.random()
        )
        await message.channel.send(embed=embed)
        return

@client.event
async def on_raw_reaction_add(payload):
    if payload.channel_id in room_links:
        reactions = room_links[payload.channel_id]
        for reaction in reactions:
            await payload.member.add_reaction(reaction),

# Add your bot token here
client.run('MTIxMzM3OTM5NzczNDg5NTY1OA.GFEs_4.GRYfVWlDkc6qnkp4oUrvDBZh_is_VOLOUSIhVo')
