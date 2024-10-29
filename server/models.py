from datetime import datetime
import pytz
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, MetaData
from sqlalchemy_serializer import SerializerMixin

# Define timezone
gmt_plus_3 = pytz.timezone("Africa/Nairobi")

# Define metadata with naming conventions
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

# Initialize SQLAlchemy
db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)  # Body must not be empty
    username = db.Column(db.String, nullable=False)  # Username must not be empty
    created_at = db.Column(
        DateTime(timezone=True),
        server_default=db.func.now(),  # Use server-side default for creation time
    )
    updated_at = db.Column(
        DateTime(timezone=True),
        onupdate=db.func.now(),  # Automatically updates to current time on modification
        default=db.func.now(),  # Set the default to the current time
    )

    def to_dict(self):
        """Convert the Message instance to a dictionary."""
        return {
            "id": self.id,
            "body": self.body,
            "username": self.username,
            "created_at": self.created_at.astimezone(gmt_plus_3).isoformat() if self.created_at else None,
            "updated_at": self.updated_at.astimezone(gmt_plus_3).isoformat() if self.updated_at else None,
        }
