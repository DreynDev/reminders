from datetime import datetime, timezone
from config import db


class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    text = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    reminder_at = db.Column(db.DateTime)
    favorite = db.Column(db.Boolean, default=False)
    complete = db.Column(db.Boolean, default=False)

    def category(self):
        categories = []

        if not self.complete and self.favorite:
            categories.append('Избранные')

        if not self.complete and (self.reminder_at is not None and self.reminder_at.date() == datetime.now().date()):
            categories.append('Сегодня')

        if not self.complete and self.reminder_at is not None and self.reminder_at.date() > datetime.now().date():
            categories.append('В планах')

        if self.complete or (self.reminder_at is not None and self.reminder_at < datetime.now()):
            categories.append('Завершено')

        return categories
