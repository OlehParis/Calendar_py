from crypt import methods
import sqlite3
import os
from datetime import datetime
from flask import Blueprint, render_template, redirect, request
from .forms import AppointmentForm
bp = Blueprint('main', __name__ , url_prefix='/')
DB_FILE = os.environ.get("DB_FILE")

@bp.route('/', methods=['GET','POST'])
def main():
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

    conn = sqlite3.connect(DB_FILE)
    # Create a cursor from the connection
    cursor = conn.cursor()
    # Execute the SQL query
    cursor.execute("""
        SELECT id, name, start_datetime, end_datetime, description, private
        FROM appointments
        ORDER BY start_datetime;
    """)
    # Fetch all of the records
    rows = cursor.fetchall()

    formatted_rows = []
    for row in rows:
        start_datetime = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
        end_datetime = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
        formatted_row = (
            row[0],
            row[1],
            start_datetime.strftime('%H:%M'),
            end_datetime.strftime('%H:%M'),
            row[4],
            row[5]
        )
        formatted_rows.append(formatted_row)
    # Close the connection
    conn.close()
    return render_template('main.html', rows=formatted_rows, form=form)
