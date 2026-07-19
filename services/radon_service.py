import json
import subprocess


def run_radon(file_path):
    """
    Returns:
        complexity findings
        maintainability index
        raw metrics
    """

    # --------------------------
    # Cyclomatic Complexity
    # --------------------------

    cc = subprocess.run(
        [
            "radon",
            "cc",
            file_path,
            "-j"
        ],
        capture_output=True,
        text=True
    )

    cc_report = json.loads(
        cc.stdout or "{}"
    )

    findings = []

    for _, values in cc_report.items():

        for item in values:

            findings.append({

                "type": "complexity",

                "message":
                (
                    f"{item['type']} "
                    f"{item['name']} "
                    f"Complexity={item['complexity']}"
                ),

                "rank": item["rank"],

                "line": item["lineno"]

            })

    # --------------------------
    # Maintainability Index
    # --------------------------

    mi = subprocess.run(
        [
            "radon",
            "mi",
            file_path,
            "-j"
        ],
        capture_output=True,
        text=True
    )

    mi_report = json.loads(
        mi.stdout or "{}"
    )

    maintainability = 0

    if file_path in mi_report:

        maintainability = mi_report[file_path]["mi"]

    # --------------------------
    # Raw Metrics
    # --------------------------

    raw = subprocess.run(
        [
            "radon",
            "raw",
            file_path,
            "-j"
        ],
        capture_output=True,
        text=True
    )

    raw_report = json.loads(
        raw.stdout or "{}"
    )

    metrics = {}

    if file_path in raw_report:

        metrics = raw_report[file_path]

    return {

        "findings": findings,

        "mi": maintainability,

        "metrics": metrics

    }