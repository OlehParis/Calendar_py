from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, request, url_for
from .forms import AppointmentForm
import sqlite3
import os

bp = Blueprint('main', __name__, url_prefix='/')
DB_FILE = os.environ.get("DB_FILE")

@bp.route("/")
def main():
    d = datetime.now()
    return redirect(url_for(".daily", year=d.year, month=d.month, day=d.day))

@bp.route("/<int:year>/<int:month>/<int:day>", methods=['GET', 'POST'])
def daily(year, month, day):
    form = AppointmentForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Extract form data
        name = form.name.data
        start_date = form.start_date.data
        start_time = form.start_time.data
        end_date = form.end_date.data
        end_time = form.end_time.data
        description = form.description.data
        private = form.private.data
       
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO appointments (name, start_datetime, end_datetime, description, private)
            VALUES (?, ?, ?, ?, ?);
        """, (name, datetime.combine(start_date, start_time), datetime.combine(end_date, end_time), description, private))
        conn.commit()
        conn.close()

        return redirect('/')
    
    day = datetime(year, month, day)
    one_day = timedelta(days=1)
    next_day = day + one_day
    
    # Fetch appointments for the specified day
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, start_datetime, end_datetime
        FROM appointments
        WHERE start_datetime BETWEEN :day AND :next_day
        ORDER BY start_datetime""", {'day': day, 'next_day': next_day})
    rows = cursor.fetchall()
    conn.close()

    formatted_rows = []
    for row in rows:
        start_datetime = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
        end_datetime = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
        formatted_row = (
            row[0],
            row[1],
        start_datetime.strftime('%H:%M'),
        end_datetime.strftime('%H:%M')
    )
    formatted_rows.append(formatted_row)

    return render_template('main.html', rows=formatted_rows, form=form,  day=day )
