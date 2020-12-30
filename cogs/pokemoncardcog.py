import discord
from discord.ext import commands # Bot Commands Frameworkのインポート
import asyncio
import random

client = discord.Client()

# コグとして用いるクラスを定義。
class MainCog(commands.Cog):
    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def start(self, ctx):
        embed=discord.Embed(title="試合開始", description="先行後攻の決定権を決めます。", color=0xff5c5c)
        embed.set_thumbnail(url="https://www.pokemon-card.com/assets/images/card_images/large/SM11a/036961_T_JAJJIMAN.jpg")
        embed.add_field(name="説明", value="参加する方は🆗リアクションをクリックしてください。(先着二名)", inline=False)
        embed.set_footer(text="p!start 先行後攻の決定権を決めます。")
        msg = await ctx.send(embed=embed) #embed出力
        await msg.add_reaction("❌")
        await msg.add_reaction("🆗")
        def check(react, user):
            return user == ctx.author and (str(react) == "❌" or str(react) == "🔄") and react.message.id == msg.id

        while not client.is_closed(): #タイムアウトするまでリアクション受付を継続

            try:
                user,react = await self.bot.wait_for('reaction_add', check=check, timeout=30.0)

            except asyncio.TimeoutError:
                await msg.clear_reactions()
                await msg.add_reaction('❌')
                return

            else:
                await msg.clear_reactions()
                await msg.add_reaction('❌')

    @commands.command()
    async def coin(self, ctx):
        rasult_coin = [random.randint(1,2)]
        print(rasult_coin[0])
        result_coin_string = ["表　○","裏　×"]
        embed=discord.Embed(title="コイントス", description="１回又は複数回コインを投げます。", color=0xff5c5c)
        embed.set_thumbnail(url="https://www.pokemon-card.com/assets/images/card_images/large/S4a/038826_T_RUMINASUMEIZUNOMORI.jpg")
        embed.add_field(name="1回目", value=result_coin_string[rasult_coin[0]-1], inline=True)
        embed.set_footer(text="p!coin コイントスを行います。")
        msg = await ctx.send(embed=embed) #embed出力
        await msg.add_reaction("❌")
        await msg.add_reaction("🔄")

        def check(react, user):
            return user == ctx.author and (str(react) == "❌" or str(react) == "🔄") and react.message.id == msg.id

        while not client.is_closed(): #タイムアウトするまでリアクション受付を継続

            try:
                user,react = await self.bot.wait_for('reaction_add', check=check, timeout=30.0)

            except asyncio.TimeoutError:
                await msg.clear_reactions()
                await msg.add_reaction('❌')
                return

            else:
                emoji = str(user)

                if emoji == "❌":
                    await msg.clear_reactions()
                    break
                elif emoji == "🔄":
                    rasult_coin.append(random.randint(1,2))
                    print(rasult_coin[1])
                    embed=discord.Embed(title="コイントス", description="１回又は複数回コインを投げます。", color=0xff5c5c)
                    embed.set_thumbnail(url="https://www.pokemon-card.com/assets/images/card_images/large/S4a/038826_T_RUMINASUMEIZUNOMORI.jpg")
                    result_sum = [0,0]
                    for index, item in enumerate(rasult_coin):
                        embed.add_field(name=""+str(index+1)+"回目", value=result_coin_string[item-1], inline=True)
                        if item == 1:
                            result_sum[0] += 1
                        else:
                            result_sum[1] += 1
                    embed.add_field(name="合計", value="表:"+str(result_sum[0])+"　裏:" + str(result_sum[1]), inline=False)
                    embed.set_footer(text="p!coin コイントスを行います。")
                    await msg.edit(embed=embed) #embed出力
                    await msg.clear_reactions()
                    await msg.add_reaction("❌")
                    await msg.add_reaction("🔄")

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.remove_command('help')
    bot.add_cog(MainCog(bot)) # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
