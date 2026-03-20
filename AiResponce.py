import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("File.env")

API_KEY = os.getenv("API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)


def GetPromptAndResponse(green_idx, traffic_idx, human_idx, climate, living_type):

    climate_str = str(climate)

    if living_type == "Outdoor":
        plant_recommendation = "Recommend suitable trees, shrubs, and plants that thrive outdoors to enhance urban greenery."
    else:
        plant_recommendation = "Recommend small plants, flowers, and indoor greenery suitable for apartments or small spaces."

    if living_type == "Indoor":
        traffic_idx = 0

    prompt = f"""
    You are an environmental analysis AI. You MUST strictly base your analysis ONLY on the provided numerical indices.

    IMPORTANT RULES:
    - If Traffic Density Index is 0, DO NOT mention traffic, vehicles, or road pollution, HOWEVER! IF TRAFFIC INDEX OR ANY OTHER INDEX IS < 0, THAN DISCUSS ABOUT IT
    - If Green Coverage Index is low (< 0.3), mention lack of greenery.
    - If Human Activity Index is high (> 0.5), mention crowding.
    - If any index is 0, DO NOT assume its presence.

    SPECIAL RULE:
    - If Living situation is Indoor, focus ONLY on indoor environmental factors (air quality, space, plants).
    - DO NOT mention roads, traffic, or outdoor pollution for Indoor environments.

    DATA:
    - Green Coverage Index: {green_idx}
    - Traffic Density Index: {traffic_idx}
    - Human Activity Index: {human_idx}
    - Climate: {climate_str}
    - Living situation: {living_type} settlement

    Provide your answer in the following format:

    Environmental Assessment:
    [text]

    Key Issues:
    [list]

    Plant Recommendations:
    [list]

    Then, {plant_recommendation}
    """

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    result = response.choices[0].message.content
    return result