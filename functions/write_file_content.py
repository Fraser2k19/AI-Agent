from google.genai import types

import os

def write_file(working_directory, file_path, content):
    try:
        abs_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not abs_path.startswith(os.path.abspath(working_directory)):
            return f"Error: Access to {file_path} is outside the working directory."
        with open(abs_path, 'w') as f:
            f.write(content)
        return f"File {file_path} written successfully."
    except Exception as e:
        return f"Error writing to file: {e}"



schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="To know which file to write to"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the content of the file"
            )
        },
    ),
)
