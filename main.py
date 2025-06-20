import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model_name = 'gemini-2.0-flash-001'
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)



if len(sys.argv) < 2:
    print("no promt provided")
    sys.exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
]

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config=types.GenerateContentConfig(
    tools=[available_functions], 
    system_instruction=system_prompt
),
)

if response.function_calls:
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
else:
    print(response.text)

if "--verbose" in sys.argv:
    print("User prompt:", sys.argv[1])
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)

