import os
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        abs_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not abs_path.startswith(os.path.abspath(working_directory)):
            return f"Error: Access to {file_path} is outside the working directory."
        with open(abs_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file you want to read."
            ),
        },
    ),
)

