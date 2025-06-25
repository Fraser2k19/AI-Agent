import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from call_function import call_function, available_functions
from functions.get_files_info import get_files_info


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



system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""




for i in range(20):
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )
    no_more_function_calls = True
    for candidate in response.candidates:
        part = candidate.content.parts[0] if candidate.content.parts else None
        if part and hasattr(part, "function_call") and part.function_call:
            no_more_function_calls = False
            result_message = call_function(part.function_call, verbose="--verbose" in sys.argv)
            messages.append(result_message)
        else:
            messages.append(candidate.content)

    if no_more_function_calls:
        final_part = response.candidates[0].content.parts[0]
        if hasattr(final_part, "text"):
            print(final_part.text)
        else:
            print("[No final answer text found.]")
        break
        

if response.function_calls:
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose="--verbose" in sys.argv)
        if "--verbose" in sys.argv:
            print(f"-> {function_call_result.parts[0].function_response.response}")
else:
    print(response.text)




