import json
import subprocess


def run_bandit(file_path):

    command = [
        "bandit",
        "-f",
        "json",
        file_path
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if not result.stdout:
        return []

    report = json.loads(result.stdout)

    return report.get("results", [])