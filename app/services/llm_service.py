import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

import json

async def generate_summary(diff_data: dict) -> str:
    """Generate a structured AI summary of changes using AsyncOpenAI."""
    if not os.getenv("OPENAI_API_KEY"):
        return json.dumps({"error": "OpenAI API Key not configured"})

    added_text = diff_data.get("added", "")
    removed_text = diff_data.get("removed", "")

    if not added_text and not removed_text:
        return json.dumps({"message": "No significant strategic changes detected."})

    # Truncate to avoid token limits
    max_len = 3000
    added_text = added_text[:max_len]
    removed_text = removed_text[:max_len]
    
    prompt = f"""
    You are a competitive intelligence analyst.
    Compare previous and new version of a SaaS website page.

    Ignore:
    - navigation elements
    - footer links
    - timestamps
    - minor numeric changes
    - ordering changes
    - copyright updates

    Focus on:
    - pricing updates
    - feature additions or removals
    - product launches
    - positioning or messaging changes
    - policy changes

    Return a JSON object with the following keys:
    - pricing (list of strings)
    - features (list of strings)
    - positioning (list of strings)
    - strategy (list of strings, 1-2 lines on implications)

    If no meaningful change in a category, return an empty list.
    If no meaningful strategic changes at all, ensure all lists are empty or provide a clear message.

    Changes:
    [ADDED CONTENT]:
    {added_text}

    [REMOVED CONTENT]:
    {removed_text}
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo-1106", # supports json_object
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return json.dumps({"error": f"Error generating summary: {str(e)}"})
