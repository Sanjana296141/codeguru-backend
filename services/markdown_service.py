import os
from models.ai_review import AIReview
from models.documentation import Documentation

def generate_markdown(review, findings):

    reports_folder = "reports"

    os.makedirs(
        reports_folder,
        exist_ok=True
    )

    filename = f"review_{review.id}.md"

    filepath = os.path.join(
        reports_folder,
        filename
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        file.write("# CodeGuru Review Report\n\n")

        file.write(
            f"## Project\n"
            f"{review.project.project_name}\n\n"
        )

        file.write(
            f"## Score\n"
            f"{review.review_score}\n\n"
        )

        file.write(
            f"## Summary\n"
            f"{review.summary}\n\n"
        )

        file.write("## Metrics\n\n")

        file.write(
            f"- Maintainability Index : {review.maintainability_index}\n"
        )

        file.write(
            f"- LOC : {review.loc}\n"
        )

        file.write(
            f"- SLOC : {review.sloc}\n"
        )

        file.write(
            f"- LLOC : {review.lloc}\n"
        )

        file.write(
            f"- Comments : {review.comments}\n"
        )

        file.write(
            f"- Blank Lines : {review.blank}\n\n"
        )


            # -----------------------------
        # AI REVIEW
        # -----------------------------

        ai_review = AIReview.query.filter_by(
            review_id=review.id
        ).first()

        if ai_review:

            file.write("## AI Code Review\n\n")

            file.write(
                f"**Model:** {ai_review.model_used}\n\n"
            )

            file.write(
                ai_review.ai_response
            )

            file.write("\n\n")

                # -----------------------------
        # DOCUMENTATION
        # -----------------------------

        documentation = Documentation.query.filter_by(
            review_id=review.id
        ).first()

        if documentation:

            file.write("## Documentation\n\n")

            file.write(
                f"**Model:** {documentation.model_used}\n\n"
            )

            file.write(
                documentation.documentation
            )

            file.write("\n\n")



        file.write("## Findings\n\n")

        if len(findings) == 0:

            file.write("No issues found.\n")

        else:

            for finding in findings:

                file.write(
                    f"### {finding.tool}\n"
                )

                file.write(
                    f"- Severity : {finding.severity}\n"
                )

                file.write(
                    f"- Line : {finding.line_number}\n"
                )

                file.write(
                    f"- Issue : {finding.issue}\n\n"
                )

    return filepath