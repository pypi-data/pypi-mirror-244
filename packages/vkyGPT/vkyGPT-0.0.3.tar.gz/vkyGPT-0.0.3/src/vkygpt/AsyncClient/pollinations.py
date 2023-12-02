from random import randint
from aiohttp import ClientSession, ClientError


class Generation:
    async def create(self, prompt):
        try:
            async with ClientSession() as session:
                async with session.get(
                    url=f"https://image.pollinations.ai/prompt/{prompt}{randint(1, 10000)}",
                    timeout=30,
                ) as resp:
                    return await resp.content.read()
        except ClientError as exc:
            raise ClientError("Unable to fetch the response.") from exc
