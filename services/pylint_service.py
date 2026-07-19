import json
import subprocess


def run_pylint(file_path):

    command = [
        "pylint",
        file_path,
        "--output-format=json"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if not result.stdout:

        return []

    return json.loads(result.stdout)