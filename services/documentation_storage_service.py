from extensions import db
from config import Config

from models.documentation import Documentation


def get_documentation(review_id):

    return Documentation.query.filter_by(
        review_id=review_id
    ).first()


def save_documentation(
    review_id,
    documentation
):

    doc = Documentation(

        review_id=review_id,

        documentation=documentation,

        model_used=Config.OLLAMA_MODEL

    )

    db.session.add(doc)

    db.session.commit()

    return doc


def update_documentation(
    doc,
    documentation
):

    doc.documentation = documentation

    doc.model_used = Config.OLLAMA_MODEL

    db.session.commit()

    return doc