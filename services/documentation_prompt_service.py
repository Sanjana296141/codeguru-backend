def build_documentation_prompt(project_name):

    return f"""
You are a Senior Python Technical Writer.

Project:

{project_name}

Generate:

# Module Documentation

# Class Documentation

# Function Documentation

IMPORTANT

- Never invent functions.
- Never invent classes.
- Never invent parameters.
- Never invent return values.
- Never invent examples.
- Never invent relationships.
- If information is unavailable write:

Not Available

Use Markdown.
"""