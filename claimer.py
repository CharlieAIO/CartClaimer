import discord
from discord.ext import commands
import pymysql
import asyncio
import random

db_ip = ''
db_user = ''
db_pass = ''
db_name = ''
charset = 'utf8mb4'
cusrorType = pymysql.cursors.DictCursor

#DATABASE
conn = pymysql.connect(db_ip,user=db_user,passwd=db_pass,db=db_name,connect_timeout=30,use_unicode=True,charset=charset, cursorclass=cusrorType)
cursor = conn.cursor(pymysql.cursors.DictCursor)

#Discord Bot
token = ''
Client = discord.Client()
client = commands.Bot(command_prefix="")
client.remove_command("help")

cursor.execute("SELECT * FROM peachyYS350")
result = cursor.fetchall()
for row in result:
    product_name = row["product"]
    product_image = row["image"]

@client.event
async def on_ready():
    channel = client.get_channel(623916436603011072)
    print(f"{client.user.name} Is Ready :)")
    print('-'*20)

    embed = discord.Embed(
        title = '',
        description = '',
        colour = 0xf7c28f
    )
    embed.set_footer(text='CharlieAIO x PeachyPings', icon_url='https://pbs.twimg.com/profile_images/1111057118856130561/13ejj7k0_400x400.png')
    embed.set_author(name='Shopify Cart System Ready')
    await channel.send(embed=embed)

@client.command(pass_context=True)
async def carts(ctx):
    conn = pymysql.connect(db_ip,user=db_user,passwd=db_pass,db=db_name,connect_timeout=30,use_unicode=True,charset=charset, cursorclass=cusrorType)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM peachyYS350")
    result = cursor.fetchall()
    
    channel = client.get_channel(623916436603011072)
    for row in result:
        product_size = row["size"]
        checkout_link = row["checkoutLINK"]
        cart_stat = row["used"]
        if str(cart_stat) == "True":
            pass
        elif str(cart_stat) == "False":
            webhook_name = f'{random.randint(0,9)}{random.randint(0,9)}_emb'
            webhook_name = discord.Embed(
                title = '',
                description = '',
                colour = 0xf7c28f
            )
        
            webhook_name.set_footer(text='CharlieAIO x PeachyPings', icon_url='https://pbs.twimg.com/profile_images/1111057118856130561/13ejj7k0_400x400.png')
            webhook_name.add_field(name='How To Claim?', value='React with 🛒 To Claim Cart')
            webhook_name.add_field(name='Size', value=product_size, inline=False)

            webhook_name.set_author(name='Shopify Cart Ready!')
        
            webhook_name.set_thumbnail(url=product_image)

    
            embd = await channel.send(embed=webhook_name)
            await embd.add_reaction('🛒')
    
    
            def check(reaction, user):
                return not user.bot and str(reaction.emoji) == '🛒' and reaction.message.id == embd.id
    
    
            reaction, user = await client.wait_for('reaction_add',check=check)
            webhook_name = f'{random.randint(0,9)}{random.randint(0,9)}_emb_completed'
            webhook_name = discord.Embed(title='', colour=0xde3756)
            webhook_name.add_field(name='Cart Claimed', value=f'By {user.display_name}')
            webhook_name.set_thumbnail(url=product_image)
            webhook_name.set_footer(text='CharlieAIO x PeachyPings', icon_url='https://pbs.twimg.com/profile_images/1111057118856130561/13ejj7k0_400x400.png')
            await embd.edit(embed=webhook_name)
            webhook_name = discord.Embed(
                title = '',
                description = '',
                colour = 0xf7c28f
            )
            webhook_name.set_author(name='Shopify Cart System')
            webhook_name.add_field(name='Checkout Link Ready!', value=checkout_link)
            webhook_name.set_footer(text='CharlieAIO x PeachyPings', icon_url='https://pbs.twimg.com/profile_images/1111057118856130561/13ejj7k0_400x400.png')        
            await user.send(embed=webhook_name)
    
    
            update_user = f"UPDATE `peachyYS350` SET `used` = 'True' WHERE `checkoutLINK` = '{checkout_link}'"
            cursor.execute(update_user)
            conn.commit()




client.run(token)
