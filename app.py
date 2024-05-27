from flask import render_template, redirect, url_for, request, jsonify, send_from_directory
from datetime import datetime
from classes.reminder_manager import ReminderManager
from config import app

reminder_manager = ReminderManager()


@app.route('/scripts/<path:filename>')
def serve_scripts(filename):
    return send_from_directory('html/scripts', filename)


@app.route('/styles/<path:filename>')
def serve_styles(filename):
    return send_from_directory('html/styles', filename)


@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('html/images', filename)


@app.route('/')
def index():
    reminders = reminder_manager.get_all_reminders()
    return render_template('index.html', reminders=reminders)


@app.route('/reminders', methods=['GET'])
def get_reminders():
    reminders = reminder_manager.get_active_reminders()
    return jsonify([{
        'id': reminder.id,
        'title': reminder.title,
        'text': reminder.text,
        'reminder_at': reminder.reminder_at.isoformat()
    } for reminder in reminders if reminder.reminder_at is not None])


@app.route('/add', methods=['GET', 'POST'])
def add_reminder():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        date = request.form['date']
        time = request.form['time']
        favorite = 'favorite' in request.form
        complete = 'complete' in request.form

        reminder_manager.add_reminder(
            title, text, date, time, favorite, complete)
        return redirect(url_for('index'))

    current_datetime = datetime.now().strftime('%Y-%m-%dT%H:%M')
    return render_template('create_reminderForm.html', current_datetime=current_datetime)


@app.route('/edit/<int:reminder_id>', methods=['GET', 'POST'])
def edit_reminder(reminder_id):
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        date = request.form['date']
        time = request.form['time']
        favorite = 'favorite' in request.form
        complete = 'complete' in request.form

        reminder_manager.edit_reminder(
            reminder_id, title, text, date, time, favorite, complete)
        return redirect(url_for('index'))

    reminder = reminder_manager.get_reminder_from_id(reminder_id)
    current_datetime = datetime.now().strftime('%Y-%m-%dT%H:%M')
    return render_template('edit_reminderForm.html', reminder=reminder, current_datetime=current_datetime)


@app.route('/complete/<int:reminder_id>', methods=['POST'])
def complete(reminder_id):
    reminder_manager.complete_reminder(reminder_id)
    return redirect(url_for('index'))


@app.route('/remove/<int:reminder_id>', methods=['POST'])
def remove(reminder_id):
    reminder_manager.remove_reminder(reminder_id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
