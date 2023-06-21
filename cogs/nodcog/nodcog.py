import discord
import random
from collections import Counter, OrderedDict
from redbot.core import commands, hybrid_commands
from redbot.core.bot import Red


class NodCog(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.kyle = 850206173873700914
        self.new_order_id = 1005754173192679476
        self.chat_id = 1114908888685359145
        self.office_chat_id = 1114821671224881153
        self.war_room_id = 1033049367118106664
        self.office_members = []

    @property
    def new_order(self):
        for g in self.bot.guilds:
            if g.id == self.new_order_id:
                return g

    @property
    def chat(self):
        return self.bot.get_channel(self.chat_id)

    @property
    def war_room(self):
        return self.bot.get_channel(self.war_room_id)

    @commands.command()
    async def test(self):
        self.new_order.get_channel(self.chat_id).fetch_message()

    async def get_nod_member(self, m_id):
        m = await self.new_order.fetch_member(m_id)
        if not m:
            return None
        return m

    def update_office(self, member, join):
        if join:
            if member in self.office_members:
                return f"<@{member.id}> 이미 입실 처리 되었습니다."

            self.office_members.append(member)
            return f"<@{member.id}> 입실 ✅"

        if member not in self.office_members:
            return f"<@{member.id}> 입실 처리 되지 않았습니다."

        self.office_members.remove(member)
        return f"<@{member.id}> 퇴실 ✅"

    @commands.command(aliases=["출근", "입실"])
    async def office_in(self, ctx, *args):
        if ctx.channel.id != self.office_chat_id:
            await ctx.send(f"<#{self.office_chat_id}> 채널을 이용해주세요.")
            return

        if not args:
            await ctx.send(self.update_office(ctx.author, join=True))
            return

        args = "".join(args).replace("<@", "").split(">")
        args = args.remove("")
        res = []
        for arg in args:
            member = await self.get_nod_member(arg[2:-1])
            res.append(self.update_office(member, join=True))
            print(res)

        await ctx.send("\n".join(res))

    @commands.command(aliases=["퇴근", "퇴실"])
    async def office_out(self, ctx, *args):
        if ctx.channel.id != self.office_chat_id:
            await ctx.send(f"<#{self.office_chat_id}> 채널을 이용해주세요.")
            return

        if args and args[0] == "all":
            self.office_members = []
            await ctx.send("전원 퇴실 처리 되었습니다.")
            return

        if not args:
            await ctx.send(self.update_office(ctx.author, join=False))
            return

        args = "".join(args).replace("<@", "").split(">")
        args = args.remove("")
        res = []
        for arg in args:
            member = await self.get_nod_member(arg[2:-1])
            res.append(self.update_office(member, join=False))

        await ctx.send("\n".join(res))

    @commands.command(aliases=["사무실"])
    async def office(self, ctx):
        if ctx.channel.id != self.office_chat_id:
            await ctx.send(f"<#{self.office_chat_id}> 채널을 이용해주세요.")
            return

        if not self.office_members:
            await ctx.send("비어있음.")
            return

        await ctx.send(
            "```\n"
            + f"총 {len(self.office_members)}명\n"
            + "\n".join(m.display_name for m in self.office_members)
            + "```"
        )

    @commands.command(aliases=["@사무실"])
    async def mention_office_members(self, ctx):
        await ctx.send(" ".join(f"<@{m.id}>" for m in self.office_members))

    @app_commands.command(name="테스트")
    async def test(self, ctx):
        await ctx.send("hello")

    @commands.command(aliases=["성공사례"])
    async def success(self, ctx, top: int = None):
        temp = await ctx.send(f"계산중... <@{ctx.author.id}>")

        channel = self.bot.get_channel(1006180412806152283)
        history = channel.history(limit=None, oldest_first=True)
        msgs = [msg async for msg in history]

        authors = []
        for i, msg in enumerate(msgs):
            if msg.author.bot:
                continue
            author = msg.author.display_name
            if i == 0 or authors[-1] != author:
                authors.append(author)

        counter = Counter(authors).most_common(top)
        await temp.delete()
        await ctx.send(
            "```\n" + "\n".join(f"{v}건\t{k}" for k, v in counter) + "```"
        )

    @commands.command(aliases=["나이통계", "나이"])
    async def age(self, ctx):
        users = [m for m in self.new_order.members if not m.bot]
        nicks = [u.display_name for u in users]
        splits = [n.split("/") for n in nicks]
        ages = [s[1].strip() for s in splits if len(s) >= 2] + ["31"]  # 카일형님
        counter = Counter(ages).most_common()
        await ctx.send(
            "```\n" + "\n".join(f"{k}살\t{v}명" for k, v in counter) + "```"
        )

    @commands.command()
    async def roles(self, ctx):
        roles = self.new_order.roles
        count = {role.name: len(role.members) for role in roles}
        count = OrderedDict(sorted(count.items()))
        await ctx.send(
            "```\n" + "\n".join(f"{k:25}{v}명" for k, v in count.items()) + "```"
        )

    @commands.command(aliases=["찬송가"])
    async def hymn(self, ctx):
        homies = ["할것", "절대", "진인사대천명"]
        audio = self.bot.get_cog("Audio")
        await audio.command_play(ctx, query=f"호미들 {random.choice(homies)}")

    @commands.command(aliases=["공지방"])
    async def notice(self, ctx):
        await ctx.send(
            "@everyone 공지방 이동했습니다."
            + " 다들 <#1017008474942611476> 게시판 확인 후 입장해주세요.",
            allowed_mentions=discord.AllowedMentions.all(),
        )

    @commands.command(aliases=["초심자", "뉴비"])
    async def newbie(self, ctx):
        await ctx.send(
            "> ***필수영상***\n"
            + "> https://discord.com/channels/1005754173192679476/1017008474942611476/1112734740177490011\n"
            + "\n"
            + "> ***뉴오더 사용법***\n"
            + "> <#1017828946944999575>\n"
        )

    # @commands.command(aliases=["주온아"])
    async def juon(self, ctx):
        await ctx.send("자라")

    @commands.command(aliases=["하면"])
    async def do(self, ctx):
        await ctx.send("된다")

    @commands.command(aliases=["자면"])
    async def sleep(self, ctx):
        await ctx.send("안된다")

    @commands.command(aliases=["잠언", "잠", "그만자", "일어나"])
    async def wake_up(self, ctx):
        await ctx.send(
            "```\n"
            + "9   게으른 자여\n"
            + "    네가 어느 때까지 눕겠느냐\n"
            + "    네가 어느 때에 잠이 깨어 일어나겠느냐\n"
            + "10  좀더 자자, 좀더 졸자,\n"
            + "    손을 모으고 좀더 눕자 하면\n"
            + "11  네 빈궁이 강도 같이 오며\n"
            + "    네 곤핍이 군사 같이 이르리라\n"
            + "```"
        )

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.guild.id != self.new_order_id:
            return

        if member.id != self.kyle:
            return
        if before.channel and before.channel.id == self.war_room_id:
            return
        if not after.channel or after.channel.id != self.war_room_id:
            return

        await self.chat.send(
            f"@everyone <@{self.kyle}> entered the <#{self.war_room_id}>",
            allowed_mentions=discord.AllowedMentions.all(),
        )
