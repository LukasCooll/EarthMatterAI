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
    """
    Generates a dynamic prompt based on environment indices and living situation.
    living_type: "Indoor" or "Outdoor" (passed from Flask)
    """

    climate_str = str(climate)

    # Decide plant recommendation based on living type
    if living_type == "Outdoor":
        plant_recommendation = "Recommend suitable trees, shrubs, and plants that thrive outdoors to enhance urban greenery."
    else:
        plant_recommendation = "Recommend small plants, flowers, and indoor greenery suitable for apartments or small spaces."

    prompt = f"""
    Analyze the following urban environmental data:
    - Green Coverage Index: {green_idx}  green objects(plants,trees...) / total objects count
    - Traffic Density Index: {traffic_idx}  traffic objects(cars,trucks...) / total objects count
    - Human Activity Index: {human_idx} people count / total object count
    - Climate: {climate_str}
    - Living situation: {living_type} settlement

    Provide your answer in the following format:

    Environmental Assessment:
    [short analysis]

    Key Issues:
    [list]

    Plant Recommendations:
    [list]

    Provide a concise professional assessment of sustainability and environmental health in this area.
    Then, {plant_recommendation}
    """

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    result = response.choices[0].message.content
    return result