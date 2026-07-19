from extensions import db


def save_metrics(
    review,
    maintainability,
    metrics
):

    review.maintainability_index = maintainability

    review.loc = metrics.get(
        "loc",
        0
    )

    review.sloc = metrics.get(
        "sloc",
        0
    )

    review.lloc = metrics.get(
        "lloc",
        0
    )

    review.comments = metrics.get(
        "comments",
        0
    )

    review.multi = metrics.get(
        "multi",
        0
    )

    review.blank = metrics.get(
        "blank",
        0
    )

    db.session.commit()