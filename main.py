from http.client import RemoteDisconnected
import os, asyncio

from baseAPI.models import FreqList, CreqList, KeyWList, RequestGroup
from discordBot.base import DiscordClient
from utils import is_intable


TOKEN = os.getenv('TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))


bot = DiscordClient(TOKEN)


async def main():
    # START BOT
    await bot.run()
    # MAIN BODY
    try:
        while True:
            row = FreqList.pop()
            if row:
                row += ['']*2
                interval = is_intable(row[2]) or 5

                request_group = RequestGroup(body=row[0], ids_str=row[1])
                for req in request_group.requests:
                    send_req = await bot.send_req(channel_id=CHANNEL_ID, req=req)
                    if send_req:
                        pass
                    else:
                        print('send_req error', row)
                        return
                    await asyncio.sleep(interval)
                CreqList.add(request_group.to_row())
                    
            else:
                await asyncio.sleep(10)
    except KeyboardInterrupt:
        # CLOSE BOT
        await bot.close()
    except RemoteDisconnected:
        print('Retry to connect.')
        return await main()
    except Exception as ex:
        print(ex)
        return await main()


if __name__ == "__main__":
    asyncio.run(main())
    