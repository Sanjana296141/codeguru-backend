import os

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer

from models.ai_review import AIReview
from models.documentation import Documentation


def generate_pdf(review, findings):

    reports_folder = "reports"

    os.makedirs(
        reports_folder,
        exist_ok=True
    )

    filename = f"review_{review.id}.pdf"

    filepath = os.path.join(
        reports_folder,
        filename
    )

    document = SimpleDocTemplate(filepath)

    styles = getSampleStyleSheet()

    story = []

    # -----------------------------
    # Title
    # -----------------------------

    story.append(
        Paragraph(
            "<b>CodeGuru Review Report</b>",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # -----------------------------
    # Project
    # -----------------------------

    story.append(
        Paragraph(
            f"<b>Project:</b> {review.project.project_name}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Score:</b> {review.review_score}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Summary:</b> {review.summary}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # -----------------------------
    # Metrics
    # -----------------------------

    story.append(
        Paragraph(
            "<b>Metrics</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Maintainability Index : {review.maintainability_index}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"LOC : {review.loc}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"SLOC : {review.sloc}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"LLOC : {review.lloc}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Comments : {review.comments}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Blank Lines : {review.blank}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # -----------------------------
    # AI REVIEW
    # -----------------------------

    ai_review = AIReview.query.filter_by(
        review_id=review.id
    ).first()

    if ai_review:

        story.append(
            Paragraph(
                "<b>AI Code Review</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Spacer(1, 10)
        )

        paragraphs = ai_review.ai_response.split("\n")

        for line in paragraphs:

            if line.strip():

                safe_line = (
                    line
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                )

                story.append(
                    Paragraph(
                        safe_line,
                        styles["Normal"]
                    )
                )

        story.append(
            Spacer(1, 20)
        )

    # -----------------------------
    # DOCUMENTATION
    # -----------------------------

    documentation = Documentation.query.filter_by(
        review_id=review.id
    ).first()

    if documentation:

        story.append(
            Paragraph(
                "<b>Documentation</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Spacer(1, 10)
        )

        paragraphs = documentation.documentation.split("\n")

        for line in paragraphs:

            if line.strip():

                safe_line = (
                    line
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                )

                story.append(
                    Paragraph(
                        safe_line,
                        styles["Normal"]
                    )
                )

        story.append(
            Spacer(1, 20)
        )

    # -----------------------------
    # Findings
    # -----------------------------

    story.append(
        Paragraph(
            "<b>Findings</b>",
            styles["Heading2"]
        )
    )

    if len(findings) == 0:

        story.append(
            Paragraph(
                "No issues found.",
                styles["Normal"]
            )
        )

    else:

        for finding in findings:

            story.append(
                Paragraph(
                    (
                        f"<b>{finding.tool}</b> | "
                        f"{finding.severity} | "
                        f"Line {finding.line_number}<br/>"
                        f"{finding.issue}"
                    ),
                    styles["Normal"]
                )
            )

            story.append(
                Spacer(1, 10)
            )

    document.build(story)

    return filepath