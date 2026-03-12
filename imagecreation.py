from openai import OpenAI
import base64
import os

def CreateIMG(imgpath, Res):
    client = OpenAI(api_key=os.getenv("IMAGEAPI_KEY"))

    with open(imgpath, "rb") as image_file:
        response = client.images.edit(
            model="gpt-image-1",
            image=("image.png", image_file, "image/png"),
            prompt=f"Change the photo to make it greener based on this response: {Res}",
        )

    img_data = response.data[0].b64_json

    with open("editedphoto.png", "wb") as out:
        out.write(base64.b64decode(img_data))
    print("Saved as editedphoto.png")