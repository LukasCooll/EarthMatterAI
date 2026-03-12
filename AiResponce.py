import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("File.env")

API_KEY = os.getenv("API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

def InOutDoor():
    while True:
        InOut = input("Do you live in an Indoor settlement (apartment/block) or Outdoor settlement (private house)? (Indoor/Outdoor): ").strip().capitalize()
        if InOut in ["Indoor", "Outdoor"]:
            return InOut
        else:
            print("Please enter either 'Indoor' or 'Outdoor'.")

def GetPromptAndResponse(green_idx, traffic_idx, human_idx, climate):
    """
    Generates a dynamic prompt based on environment indices and living situation.
    """
    living_type = InOutDoor()
    climate_str = str(climate)

    # Dynamic recommendations based on indoor/outdoor
    if living_type == "Outdoor":
        plant_recommendation = "Recommend suitable trees, shrubs, and plants that thrive outdoors to enhance urban greenery."
    else:
        plant_recommendation = "Recommend small plants, flowers, and indoor greenery suitable for apartments or small spaces."

    prompt = f"""
    Analyze the following urban environmental data:
    - Green Coverage Index: {green_idx}
    - Traffic Density Index: {traffic_idx}
    - Human Activity Index: {human_idx}
    - Climate: {climate_str}
    - Living situation: {living_type} settlement

    Provide a concise professional assessment of sustainability and environmental health in this area.
    Then, {plant_recommendation}
    """

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    result = response.choices[0].message.content
    print(result)
    return result
