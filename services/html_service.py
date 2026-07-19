import os

from models.ai_review import AIReview
from models.documentation import Documentation


def generate_html(review, findings):

    reports_folder = "reports"

    os.makedirs(
        reports_folder,
        exist_ok=True
    )

    filename = f"review_{review.id}.html"

    filepath = os.path.join(
        reports_folder,
        filename
    )

    # ---------------------------------
    # Load AI Review
    # ---------------------------------

    ai_review = AIReview.query.filter_by(
        review_id=review.id
    ).first()

    ai_section = ""

    if ai_review:

        ai_content = (
            ai_review.ai_response
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br>")
        )

        ai_section = f"""
<h2>AI Code Review</h2>

<p><b>Model:</b> {ai_review.model_used}</p>

<div style="
background:#f5f5f5;
border:1px solid #cccccc;
padding:20px;
border-radius:8px;
line-height:1.7;
white-space:pre-wrap;
margin-bottom:25px;
">

{ai_content}

</div>
"""

    # ---------------------------------
    # Load Documentation
    # ---------------------------------

    documentation = Documentation.query.filter_by(
        review_id=review.id
    ).first()

    documentation_section = ""

    if documentation:

        documentation_content = (
            documentation.documentation
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br>")
        )

        documentation_section = f"""
<h2>Documentation</h2>

<p><b>Model:</b> {documentation.model_used}</p>

<div style="
background:#eef8ff;
border:1px solid #7fbfff;
padding:20px;
border-radius:8px;
line-height:1.7;
white-space:pre-wrap;
margin-bottom:25px;
">

{documentation_content}

</div>
"""

    html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>CodeGuru Report</title>

<style>

body {{
    font-family: Arial, sans-serif;
    margin:40px;
}}

table {{
    border-collapse: collapse;
    width:100%;
}}

table,
th,
td {{
    border:1px solid black;
}}

th,
td {{
    padding:10px;
}}

h1 {{
    color:#2c3e50;
}}

</style>

</head>

<body>

<h1>CodeGuru Review Report</h1>

<h2>Project</h2>

<p><b>Name:</b> {review.project.project_name}</p>

<p><b>Score:</b> {review.review_score}</p>

<p><b>Summary:</b> {review.summary}</p>

<h2>Metrics</h2>

<ul>

<li>Maintainability Index : {review.maintainability_index}</li>

<li>LOC : {review.loc}</li>

<li>SLOC : {review.sloc}</li>

<li>LLOC : {review.lloc}</li>

<li>Comments : {review.comments}</li>

<li>Blank : {review.blank}</li>

</ul>

{ai_section}

{documentation_section}

<h2>Findings</h2>

<table>

<tr>

<th>Tool</th>

<th>Severity</th>

<th>Line</th>

<th>Issue</th>

</tr>
"""

    for finding in findings:

        html += f"""
<tr>

<td>{finding.tool}</td>

<td>{finding.severity}</td>

<td>{finding.line_number}</td>

<td>{finding.issue}</td>

</tr>
"""

    html += """
</table>

</body>

</html>
"""

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(html)

    return filepath