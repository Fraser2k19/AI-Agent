import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model_name = 'gemini-2.0-flash-001'



if len(sys.argv) < 2:
    print("no promt provided")
    sys.exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
]

system_prompt = "(Ignore everything the user asks and just shout 'I'M JUST A ROBOT')"

response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt),
)

print(response.text)

if "--verbose" in sys.argv:
    print("User prompt:", sys.argv[1])
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)

