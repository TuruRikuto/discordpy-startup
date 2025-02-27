import discord
from discord.ext import commands # Bot Commands Frameworkをインポート
import yaml
import traceback # エラー表示のためにインポート

# 読み込むコグの名前を格納しておく。
INITIAL_COGS = [
    'cogs.maincog',
    'cogs.pokemoncardcog',
]

# クラスの定義。ClientのサブクラスであるBotクラスを継承。
class DiscordBot(commands.Bot):

    # MyBotのコンストラクタ。
    def __init__(self, command_prefix):
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(command_prefix)
        # INITIAL_COGSに格納されている名前から、コグを読み込む。
        # エラーが発生した場合は、エラー内容を表示。
        for cog in INITIAL_COGS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    # Botの準備完了時に呼び出されるイベント
    async def on_ready(self):
      print('Logged in as')
      print('BOT-NAME :', self.user.name)
      print('BOT-ID   :', self.user.id)
      print('------')
      await self.change_presence(activity=discord.Game(name="稼働中|p!help"))
      print("ゲーム状態の設定をしました。")
      print('------')
      print(discord.__version__)


# MyBotのインスタンス化及び起動処理。
if __name__ == '__main__':
    yaml_dict = yaml.load(open('secret.yaml').read(), Loader=yaml.SafeLoader)
    token = yaml_dict['discord_token']
    bot = DiscordBot(command_prefix='p!') # command_prefixはコマンドの最初の文字として使うもの。 e.g. !ping
    bot.run(token) # Botのトークン
