from datetime import datetime
from extensions import db, bcrypt



class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    from utils.timezone import india_now

    created_at = db.Column(db.DateTime, default=india_now)

    reset_token = db.Column(db.String(255), nullable=True)

    reset_token_expiry = db.Column(db.DateTime, nullable=True)


    projects = db.relationship(
        "Project",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)