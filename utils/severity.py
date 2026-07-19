def normalize_severity(tool, severity):
    """
    Convert tool-specific severity levels into
    common severity levels.

    Returns:
        Critical
        High
        Medium
        Low
        Info
    """

    tool = tool.lower()
    severity = str(severity).lower()

    if tool == "pylint":

        mapping = {
            "fatal": "Critical",
            "error": "High",
            "warning": "Medium",
            "refactor": "Low",
            "convention": "Low",
            "info": "Info"
        }

    elif tool == "bandit":

        mapping = {
            "high": "High",
            "medium": "Medium",
            "low": "Low",
            "undefined": "Info"
        }

    elif tool == "radon":

        mapping = {
            "a": "Info",
            "b": "Low",
            "c": "Medium",
            "d": "High",
            "e": "Critical",
            "f": "Critical"
        }

    else:

        mapping = {}

    return mapping.get(severity, "Info")