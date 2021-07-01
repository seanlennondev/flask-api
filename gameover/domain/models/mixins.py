from datetime import datetime

from gameover.api.ext.database import db

class DateTimeMixin(object):
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow()
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=True,
        onupdate=datetime.utcnow()
    )
