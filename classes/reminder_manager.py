from classes.models import Reminder
from datetime import datetime
from config import app, db


class ReminderManager:
    def __init__(self):
        self.app = app
        self.db = db
        self.init_db()

    def init_db(self):
        with self.app.app_context():
            self.db.create_all()

    def get_all_reminders(self):
        reminders = Reminder.query.order_by(Reminder.reminder_at.asc()).all()
        for reminder in reminders:
            if reminder.reminder_at is not None and reminder.reminder_at < datetime.now():
                reminder.complete = True
                reminder.reminder_at = None
        self.db.session.commit()
        return reminders

    def get_active_reminders(self):
        reminders = Reminder.query.filter_by(complete=False).all()
        return reminders

    def add_reminder(self, title, text, date, time, favorite, complete):
        if time and (not date):
            date = datetime.now().date().strftime('%Y-%m-%d')
            reminder_at = datetime.strptime(
                f"{date} {time}", '%Y-%m-%d %H:%M')
        elif date and (not time):
            reminder_at = datetime.strptime(
                f"{date} 00:00", '%Y-%m-%d %H:%M')
        elif time and date:
            reminder_at = datetime.strptime(
                f"{date} {time}", '%Y-%m-%d %H:%M')
        else:
            reminder_at = None

        reminder = Reminder(title=title, text=text, reminder_at=reminder_at,
                            favorite=favorite, complete=complete)
        self.db.session.add(reminder)
        self.db.session.commit()

    def get_reminder_from_id(self, reminder_id):
        return Reminder.query.get(reminder_id)

    def edit_reminder(self, reminder_id, title, text, date, time, favorite, complete):
        reminder = self.get_reminder_from_id(reminder_id)
        reminder.title = title
        reminder.text = text
        reminder.favorite = favorite
        reminder.complete = complete

        if time and (not date):
            date = datetime.now().date().strftime('%Y-%m-%d')
            reminder.reminder_at = datetime.strptime(
                f"{date} {time}", '%Y-%m-%d %H:%M')
        elif date and (not time):
            reminder.reminder_at = datetime.strptime(
                f"{date} 00:00", '%Y-%m-%d %H:%M')
        elif time and date:
            reminder.reminder_at = datetime.strptime(
                f"{date} {time}", '%Y-%m-%d %H:%M')
        else:
            reminder.reminder_at = None

        self.db.session.commit()

    def complete_reminder(self, reminder_id):
        reminder = Reminder.query.get(reminder_id)
        reminder.complete = not reminder.complete
        self.db.session.commit()

    def remove_reminder(self, reminder_id):
        reminder = Reminder.query.get(reminder_id)
        self.db.session.delete(reminder)
        self.db.session.commit()
