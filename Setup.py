import discord
from discord.ext import commands
import sqlite3
import random

bot = commands.Bot(command_prefix='!')
conn = sqlite3.connect('NewData.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS heroes(hero_id INTEGER PRIMARY KEY, hero_name TEXT, 
hero_class TEXT, hero_attack TEXT, hero_health TEXT, strength TEXT, intelligence TEXT, dexterity TEXT,
charisma TEXT, luck TEXT, level TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS monsters(monster_id INTEGER PRIMARY KEY, monster_name TEXT, 
monster_attack TEXT, monster_health TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS stories(text_id INTEGER PRIMARY KEY, story_name TEXT, 
story TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS classes(class_id INTEGER PRIMARY KEY, class_name TEXT,
class_info TEXT)''')


@bot.event
async def on_ready():
    print("Bot is ready")


@bot.event
async def on_member_join(member):
    print(f'{member} has joined a server')


@bot.event
async def on_member_remove(member):
    print(f'{member} has left a server')


@bot.command(manage_messages=True)
async def delete(ctx, *, amount: int = None):
    try:
        if amount is None:
            await ctx.send("Please, input a number")
        else:
            await ctx.channel.purge(limit=amount)
            await ctx.send(f'I have deleted {amount} messages by the order of {ctx.author.mention}')
    except ValueError:
        await ctx.send('Please, try again')


@bot.command()
async def Hero(ctx):
    await ctx.send("Let's try to create a new hero. Firstly, do you want to use extended hero customization"
                   "or default (with specs/name/etc.)? If you want extended - enter the word EX in chat "
                   "and for default the word DEF in chat.")
    player_choice = await bot.wait_for('message')
    player_input = player_choice.content
    if player_input == "EX":
        print("Extended customization")
        await ctx.send("Let's try to create a new hero with extended customization. Please, enter his parameters like "
                       "this: "
                       "Name, class, start damage, start health, start strength, start intelligence, start dexterity, "
                       "start charisma, start luck and start level")
        player = await bot.wait_for('message')
        player_input = player.content.split(", ")
        print(str(player_input))
        with conn:
            cursor.execute("INSERT INTO heroes(hero_name, hero_class, hero_attack, hero_health, strength, "
                           "intelligence, "
                           "dexterity, charisma, luck, level) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (player_input[0], player_input[1],
                            player_input[2], player_input[3], player_input[4], player_input[5], player_input[6],
                            player_input[7], player_input[8], player_input[9]))
    if player_input == "DEF":
        print("Default customization")
        await ctx.send("Let's try to create new hero with default customization. Please his parameters like this:"
                       "Name, start strength, start intelligence, start dexterity, start charisma, start luck")
        player = await bot.wait_for('message')
        player_input = player.content.split(", ")
        default_damage = 10
        default_health = 100
        default_level = 1
        print(str(player_input))
        await ctx.send("And here is the list of possible classes: ")
        with conn:
            cursor.execute("SELECT class_id, class_name FROM classes")
            class_list = cursor.fetchall()
        for class_info in class_list:
            print(', '.join(map(str, class_info)))
            await ctx.send(', '.join(map(str, class_info)))
        await ctx.send("Please, select the id of the class for your hero.")
        player_class = await bot.wait_for('message')
        class_input = player_class.content
        with conn:
            cursor.execute("SELECT class_name FROM classes WHERE class_id=(?)", class_input)
            selected_class = cursor.fetchall()
        for class_info in selected_class:
            await ctx.send(' '.join(map(str, class_info)) + " have been chosen")
            class_table = ' '.join(map(str, class_info))
            with conn:
                cursor.execute("INSERT INTO heroes(hero_name, hero_class, strength, intelligence, dexterity, charisma, "
                               "luck, hero_attack, hero_health, level) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (player_input[0], str(class_table), player_input[1], player_input[2],
                                player_input[3], player_input[4], player_input[5], default_damage, default_health,
                                default_level))


@bot.command()
async def MobCreate(ctx):
    await ctx.send("To create a new mob you need to enter his parameters like this:"
                   "Name, start damage, start health")
    gm = await bot.wait_for('message')
    gm_input = gm.content.split(", ")
    print(str(gm_input))
    with conn:
        cursor.execute("INSERT INTO monsters(monster_name, monster_attack, monster_health) VALUES (?, ?, ?)",
                       (gm_input[0], gm_input[1], gm_input[2]))


@bot.command()
async def CreateClass(ctx):
    await ctx.send("Let's create a new class. For now just enter its name.")
    gm = await bot.wait_for('message')
    gm_class_name = gm.content
    print(str(gm_class_name))
    await ctx.send("And now enter an information you want players to see about this class.")
    gm2 = await bot.wait_for('message')
    gm_class_info = gm2.content
    print(str(gm_class_info))
    with conn:
        cursor.execute("INSERT INTO classes(class_name, class_info) VALUES (?, ?)",
                       (gm_class_name, gm_class_info))


@bot.command()
async def clean(ctx):
    await ctx.send("The column have been cleaned")
    cursor.execute('DELETE FROM heroes')
    conn.commit()


@bot.command()
async def HeroList(ctx):
    with conn:
        cursor.execute("SELECT hero_id, hero_name, hero_class FROM heroes")
        hero_list = cursor.fetchall()

    for hero_info in hero_list:
        print(', '.join(map(str, hero_info)))
        await ctx.send(', '.join(map(str, hero_info)))


@bot.command()
async def MonsterList(ctx):
    with conn:
        cursor.execute("SELECT monster_id, monster_name FROM monsters")
        monster_list = cursor.fetchall()

    for monster_info in monster_list:
        print(', '.join(map(str, monster_info)))
        await ctx.send(', '.join(map(str, monster_info)))


@bot.command()
async def HeroDelete(ctx):
    await ctx.send("Please, enter the id of the hero you want to delete")
    player = await bot.wait_for('message')
    hero_delete = player.content

    with conn:
        cursor.execute("SELECT hero_name, hero_class FROM heroes WHERE hero_id=(?)", hero_delete)
        send_deleted_hero = cursor.fetchall()

        for hero_info in send_deleted_hero:
            await ctx.send(' '.join(map(str, hero_info)) + " have been deleted")

    with conn:
        cursor.execute("DELETE FROM heroes WHERE hero_id=(?)", hero_delete)
        conn.commit()


@bot.command()
async def AddStory(ctx):
    await ctx.send("Testing story editor")
    gm = await bot.wait_for('message')
    gm_story = gm.content.split(", ")

    with conn:
        cursor.execute("INSERT INTO stories(story_name, story) VALUES (?,?)", (gm_story[0], gm_story[1]))

    cursor.execute("SELECT story_name, story FROM stories")
    story_list = cursor.fetchall()

    for story_info in story_list:
        print(', '.join(map(str, story_info)))
        await ctx.send(', '.join(map(str, story_info)))


@bot.command()
async def Battle(ctx):
    await ctx.send("This regime is currently in test mode, so please, be patient")
    await ctx.send("Firstly, let's choose the hero to attack. To do it - choose hero id")

    player = await bot.wait_for('message')
    hero_battle = player.content

    with conn:
        cursor.execute("SELECT hero_name, hero_class FROM heroes WHERE hero_id=(?)", hero_battle)
        send_hero = cursor.fetchall()

    await ctx.send("And now choose the id of the monster you want to fight your hero")
    mob = await bot.wait_for('message')
    mob_battle = mob.content

    with conn:
        cursor.execute("SELECT monster_name FROM monsters WHERE monster_id=(?)", mob_battle)
        send_mob = cursor.fetchall()

    await ctx.send(' '.join(map(str, send_hero)) + " vs " + ' '.join(map(str, send_mob)))

    with conn:
        cursor.execute("Update monsters set monster_health = (select hero_attack from heroes "
                       "where hero_id = ?) - monster_health WHERE monster_id=?""", (mob_battle, hero_battle))
        conn.commit()


bot.run('Your_token')
