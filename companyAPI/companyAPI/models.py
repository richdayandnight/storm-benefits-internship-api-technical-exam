from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper
from companyAPI.database import metadata, db_session


# class Company defining each column in our company table
class Company(object):
    query = db_session.query_property()

    def __init__(self, id=None, name=None, employees_num=None, location=None, email=None, industry=None):
        self.id = id
        self.name = name
        self.employees_num = employees_num
        self.location = location
        self.email = email
        self.industry = industry

    def __repr__(self):
        return '<Company %r %r>' % (self.id, self.name)

    def serialize(self):
        return {
            'id' : self.id,
            'name': self.name,
            'employees_num': self.employees_num,
            'location': self.location,
            'email': self.email,
            'industry': self.industry
        }


# Metadata of the company table
company = Table('company', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(120), unique=True, nullable=False),
    Column('employees_num', Integer),
    Column('location', String(120)),
    Column('email', String(120)),
    Column('industry', String(120))
)

# Map the company metadata to the class Company
mapper(Company, company)