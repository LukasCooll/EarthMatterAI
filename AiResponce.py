import os
from openai import OpenAI
from dotenv import load_dotenv
import ObjRecognition

load_dotenv("File.env")

API_KEY = os.getenv("API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)


def GetPromptAndResponse():
    climate_str = str(ObjRecognition.Climate)

    prompt = f"""
    Analyze the following urban environmental data:
    Green Coverage Index = {ObjRecognition.Green_Index()},
    Traffic Density Index = {ObjRecognition.TrafficIndex()},
    Human Activity Index = {ObjRecognition.HumanDensityIndex()},
    Climate = {climate_str}.

    Provide a concise professional assessment of sustainability and environmental health. 
    Then give recommendations for trees and plants that would grow well in this climate to improve urban greenery.
    """

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}  # <- use the prompt here
        ],
    )

    print(response.choices[0].message.content)