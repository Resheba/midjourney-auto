import dataclasses, asyncio
from discord import Client


@dataclasses.dataclass
class DiscordClient:
    token: str

    def __post_init__(self):
        self.client = Client()

    async def run(self) -> None:
        asyncio.ensure_future(self.client.start(self.token))
        await self.wait_run()
    
    async def wait_run(self, timeout: int = 2):
        if not self.client.user:
            print('Try to connect...')
            await asyncio.sleep(timeout)
            return await self.wait_run(timeout)
        print('Connected.')
    
    async def close(self):
        await self.client.close()

    async def send_req(self, req: str, channel_id: int) -> bool:
        channel = self.client.get_channel(channel_id)
        print(channel)
        if channel:
            async for command in channel.slash_commands(query='i'):
                if command.name == 'imagine':
                    #await channel.send('/imagine ' + req, )
                    await command(prompt=req)
                    return True
        return False
    