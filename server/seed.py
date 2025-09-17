#!/usr/bin/env python3
# server/seed.py

import datetime
from app import app
from models import db, Employee, Meeting, Project, Assignment

with app.app_context():

    # Delete all rows in tables
    Employee.query.delete()
    Meeting.query.delete()
    Project.query.delete()

    # Add employees
    e1 = Employee(name="Uri Lee", hire_date=datetime.datetime(2022, 5, 17))
    e2 = Employee(name="Tristan Tal", hire_date=datetime.datetime(2020, 1, 30))
    e3 = Employee(name="Sasha Hao", hire_date=datetime.datetime(2021, 12, 1))
    e4 = Employee(name="Taylor Jai", hire_date=datetime.datetime(2015, 1, 2))
    db.session.add_all([e1, e2, e3, e4])
    db.session.commit()

    # Add meetings
    m1 = Meeting(topic="Software Engineering Weekly Update",
                 scheduled_time=datetime.datetime(
                     2023, 10, 31, 9, 30),
                 location="Building A, Room 142")
    m2 = Meeting(topic="Github Issues Brainstorming",
                 scheduled_time=datetime.datetime(
                     2023, 12, 1, 15, 15),
                 location="Building D, Room 430")
    db.session.add_all([m1, m2])
    db.session.commit()

    # Add projects
    p1 = Project(title="XYZ Project Flask server",  budget=50000)
    p2 = Project(title="XYZ Project React UI", budget=100000)
    db.session.add_all([p1, p2])
    db.session.commit()

    # Many-to-many relationship between employee and meeting
    e1.meetings.extend([m1, m2])
    e2.meetings.append(m1)
    e3.meetings.append(m2)
    
    # Many-to-many relationship between employee and project through assignment
    a1 = Assignment(employee=e1, project=p1, role="Lead Developer", start_date=datetime.date(2023, 1, 15))
    a2 = Assignment(employee=e2, project=p1, role="Backend Developer", start_date=datetime.date(2023, 2, 1))
    a3 = Assignment(employee=e3, project=p2, role="Frontend Developer", start_date=datetime.date(2023, 3, 1))
    a4 = Assignment(employee=e4, project=p2, role="Project Manager", start_date=datetime.date(2023, 1, 1))
    
    db.session.add_all([a1, a2, a3, a4])
    db.session.commit()
