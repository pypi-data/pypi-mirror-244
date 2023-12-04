from aiohttp import ClientSession, ClientError
class Completion:
    async def create(self, prompt):
        async with ClientSession() as session:
            try:
                async with session.post(
                    "https://us-central1-arched-keyword-306918.cloudfunctions.net/run-inference-1",
                    json={"prompt": prompt},
                ) as resp:
                    resp_json = await resp.json()
            except ClientError as exc:
                raise ClientError("Unable to fetch the response.") from exc
        return resp_json["completion"]
