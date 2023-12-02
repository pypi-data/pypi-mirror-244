from aiGPT import AsyncClient
from PIL import Image
from io import BytesIO

async def imgen(prompt):
    try:
        resp = await AsyncClient.create_generation("prodia", prompt)
        Image.open(BytesIO(resp)).show()
        print(f"🤖: Image shown.")
    except Exception as e:
        print(f"🤖: {e}")