# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Association table for Employee-Meeting many-to-many
employee_meeting = db.Table('employee_meetings',
    db.Column('employee_id', db.Integer, db.ForeignKey('employees.id'), primary_key=True),
    db.Column('meeting_id', db.Integer, db.ForeignKey('meetings.id'), primary_key=True)
)

# Association model for Employee-Project many-to-many with additional attributes
class Assignment(db.Model):
    __tablename__ = 'assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    role = db.Column(db.String)
    start_date = db.Column(db.Date)
    
    employee = db.relationship('Employee', back_populates='assignments')
    project = db.relationship('Project', back_populates='assignments')
    
    def __repr__(self):
        return f'<Assignment {self.id}, Employee: {self.employee_id}, Project: {self.project_id}, Role: {self.role}>'


class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    hire_date = db.Column(db.Date)
    
    # Many-to-many with Meeting
    meetings = db.relationship('Meeting', secondary=employee_meeting, back_populates='employees')
    
    # One-to-many with Assignment
    assignments = db.relationship('Assignment', back_populates='employee')
    
    # Association proxy to get projects through assignments
    projects = association_proxy('assignments', 'project')

    def __repr__(self):
        return f'<Employee {self.id}, {self.name}, {self.hire_date}>'


class Meeting(db.Model):
    __tablename__ = 'meetings'

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    scheduled_time = db.Column(db.DateTime)
    location = db.Column(db.String)
    
    # Many-to-many with Employee
    employees = db.relationship('Employee', secondary=employee_meeting, back_populates='meetings')

    def __repr__(self):
        return f'<Meeting {self.id}, {self.topic}, {self.scheduled_time}, {self.location}>'


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    budget = db.Column(db.Integer)
    
    # One-to-many with Assignment
    assignments = db.relationship('Assignment', back_populates='project')
    
    # Association proxy to get employees through assignments
    employees = association_proxy('assignments', 'employee')

    def __repr__(self):
        return f'<Project {self.id}, {self.title}, {self.budget}>'
