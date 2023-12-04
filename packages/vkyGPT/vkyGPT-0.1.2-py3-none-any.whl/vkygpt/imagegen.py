from vkygpt import AsyncClient
from PIL import Image
from io import BytesIO
import os

async def imgen(prompt):
    print("🤖: Generating Image.....")
    try:
        resp = await AsyncClient.create_generation("prodia", prompt)
        generated_image = Image.open(BytesIO(resp))
        generated_image.show()
        save_image = input("Do you want to save the generated image? (yes/no): ").lower()

        if save_image == "yes" or save_image == 'y':
            downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            save_path = os.path.join(downloads_folder, "generated_image.png")
            generated_image.save(save_path)
            print(f"🤖: Image saved successfully at {save_path}")
        else:
            print("🤖: Image not saved.")

    except Exception as e:
        print(f"🤖: {e}")