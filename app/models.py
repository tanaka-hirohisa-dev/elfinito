from .extensions import db

class TAccessLog(db.Model):
    __tablename__ = "t_access_log"

    id = db.Column(db.Integer, primary_key=True)
    as_of_date = db.Column(db.Date, nullable=False)
    path = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String(20), nullable=False)
    user_agent = db.Column(db.String(500), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now(),
        onupdate=db.func.now(),
        nullable=False
    )

    def __repr__(self):
        return f"<TAccessLog {self.id} {self.path} {self.ip}>"

