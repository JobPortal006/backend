from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from sqlalchemy.orm import declarative_base  # Add this import

Base = declarative_base()

class JobPost(Base):
    __tablename__ = 'job_post'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('signup.id'))
    company_id = Column(Integer, ForeignKey('company_details.id'))
    job_title = Column(String(255))
    job_description = Column(Text)
    qualification = Column(String(255))
    experience = Column(String(50))
    salary_range = Column(String(50))
    no_of_vacancies = Column(Integer)
    employee_type_id = Column(Integer, ForeignKey('employees_types.id'))
    job_role_id = Column(Integer, ForeignKey('job_role.id'))
    location_id = Column(Integer, ForeignKey('location.id'))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')

    employee = relationship("Signup")
    company = relationship('CompanyDetails')
    employee_type = relationship('EmployeeTypes')
    job_role = relationship('JobRole')
    location = relationship('Location')

class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')

class EmployeeTypes(Base):
    __tablename__ = 'employees_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_type = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')

class JobRole(Base):
    __tablename__ = 'job_role'

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_role = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')

class SkillSets(Base):
    __tablename__ = 'skill_sets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    skill_set = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')

class SkillSetMapping(Base):
    __tablename__ = 'skill_set_mapping'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('signup.id'))
    skill_id = Column(Integer, ForeignKey('skill_sets.id'))
    job_id = Column(Integer, ForeignKey('job_post.id'))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')

    employee = relationship('Signup')
    skill = relationship('SkillSets')
    job = relationship('JobPost')


engine = create_engine('mysql://theuser:thepassword@13.51.66.252:3306/backend1')
Base.metadata.create_all(engine)        