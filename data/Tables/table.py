from sqlalchemy import create_engine, Column, Integer, String, Enum, Date, DECIMAL, Text, TIMESTAMP, DateTime, ForeignKey, text 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base 
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Signup(Base):
    __tablename__ = 'signup'

    id = Column(Integer, primary_key=True, autoincrement=True)
    signup_by = Column(Enum('User', 'Recruiter', name='signup_by_enum'), nullable=False)
    email = Column(String(100), nullable=False)
    mobile_number = Column(String(15), nullable=False)
    password = Column(String(255), nullable=False)
    signup_time = Column(TIMESTAMP, server_default=func.now())
    loggedin_time = Column(TIMESTAMP)

    address = relationship('Address')
    personal_details = relationship('PersonalDetails')
    education_details = relationship('EducationDetails')
    college_details = relationship('CollegeDetails')
    professional_details = relationship('ProfessionalDetails')
    job_preferences = relationship('JobPreferences')
    resume_details = relationship('ResumeDetails')

class PersonalDetails(Base):
    __tablename__ = 'personal_details'

    personal_details_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('signup.id'))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum('Male', 'Female', 'Others', name='gender_enum'), nullable=False)
    profile_picture_path = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('signup.id'))
    registered_by = Column(Enum('User', 'Recruiter', name='registered_by_enum'), nullable=False)
    street = Column(String(255), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    pincode = Column(String(15), nullable=False)
    address_type = Column(Enum('Permanent', 'Current', name='address_type_enum'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')

class EducationDetails(Base):
    __tablename__ = 'education_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('signup.id'))
    sslc_school_name = Column(String(100), nullable=False)
    sslc_start_year = Column(Integer)
    sslc_end_year = Column(Integer)
    sslc_percentage = Column(DECIMAL(5, 2))
    hsc_school_name = Column(String(100), nullable=False)
    hsc_start_year = Column(Integer)
    hsc_end_year = Column(Integer)
    hsc_percentage = Column(DECIMAL(5, 2))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')

class CollegeDetails(Base):
    __tablename__ = 'college_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('signup.id'))
    college_name = Column(String(100), nullable=False)
    start_year = Column(Integer)
    end_year = Column(Integer)
    percentage = Column(DECIMAL(5, 2))
    department = Column(String(50), nullable=False)
    degree = Column(String(100), nullable=False)
    education_type = Column(Enum('UG', 'PG', 'Diploma', name='education_type_enum'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')

class ProfessionalDetails(Base):
    __tablename__ = 'professional_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('signup.id'))
    company_name = Column(String(100))
    years_of_experience = Column(Integer)
    job_role = Column(String(100))
    skills = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')

class JobPreferences(Base):
    __tablename__ = 'job_preferences'
     
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('signup.id'))
    key_skills = Column(String(255), nullable=False)
    industry = Column(String(100))
    department = Column(String(100))
    preferred_locations = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')

class ResumeDetails(Base):
    __tablename__ = 'resume_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('signup.id'))
    employment_status = Column(Enum('Fresher', 'Experienced', name='employment_status_enum'), nullable=False)
    resume_path = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')

class CompanyDetails(Base):
    __tablename__ = 'company_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('signup.id'))
    company_name = Column(String(100), nullable=False)
    no_of_employees = Column(Integer)
    company_industry = Column(String(100))
    company_description = Column(String(100))
    company_logo_path = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')
    contact_person_name = Column(String(100), nullable=False)
    contact_person_position = Column(String(100), nullable=False)
    company_website_link = Column(String(100), nullable=False)

    employee = relationship("Signup")

class JobPost(Base):
    __tablename__ = 'job_post'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('signup.id'))
    company_id = Column(Integer, ForeignKey('company_details.id'))
    job_title = Column(String(255))
    job_description = Column(Text)
    experience = Column(String(50))
    salary_range = Column(String(50))
    no_of_vacancies = Column(Integer)
    additional_queries = Column(String(50))
    # additional_queries = relationship("AdditionalQueries", back_populates="job_post")
    employee_type_id = Column(Integer, ForeignKey('employees_types.id'))
    job_role_id = Column(Integer, ForeignKey('job_role.id'))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')

    employee = relationship("Signup")
    company = relationship('CompanyDetails')
    employee_type = relationship('EmployeeTypes')
    job_role = relationship('JobRole')

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

class Qualification(Base):
    __tablename__ = 'qualification'

    id = Column(Integer, primary_key=True, autoincrement=True)
    qualification = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')

class QualificationMapping(Base):  
    __tablename__ = 'qualification_mapping'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('signup.id'))
    qualification_id = Column(Integer, ForeignKey('qualification.id'))
    job_id = Column(Integer, ForeignKey('job_post.id'))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')
    
    employee = relationship('Signup')
    qualification = relationship('Qualification')
    job = relationship('JobPost')

class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')

class LocationMapping(Base):
    __tablename__ = 'location_mapping'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('signup.id'))
    location_id = Column(Integer, ForeignKey('location.id'))
    job_id = Column(Integer, ForeignKey('job_post.id'))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')
    
    employee = relationship('Signup')
    location = relationship('Location')
    job = relationship('JobPost')

class ApplyJob(Base):
    __tablename__ = 'apply_job'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('signup.id'))
    resume_id = Column(Integer, ForeignKey('resume_details.id'))
    job_id = Column(Integer, ForeignKey('job_post.id'))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')
    
    signup = relationship('Signup')
    resume_details = relationship('ResumeDetails')
    job_post = relationship('JobPost')

class AdditionalQueries(Base):
    __tablename__ = 'additional_queries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey('job_post.id'))
    user_id = Column(Integer, ForeignKey('signup.id'))
    total_experience = Column(String(255))
    current_ctc = Column(String(255))
    expected_ctc = Column(String(255))
    notice_period = Column(String(255))

    # job_post = relationship('JobPost', back_populates='additional_queries')
    signup = relationship('Signup')

class SavedJob(Base):
    __tablename__ = 'saved_job'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('signup.id'))
    job_id = Column(Integer, ForeignKey('job_post.id'))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')
    
    signup = relationship('Signup')
    job_post = relationship('JobPost')

class JobNotification(Base):
    __tablename__ = 'job_notification'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('signup.id'))
    job_id = Column(Integer, ForeignKey('job_post.id'))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), server_onupdate='CURRENT_TIMESTAMP')
    
    signup = relationship('Signup')
    job_post = relationship('JobPost')

# engine = create_engine('mysql://theuser:thepassword@13.51.66.252:3306/jobportal')
engine = create_engine('mysql://root:mysqllocal@localhost:3306/jobportal')
Base.metadata.create_all(engine) 

# Define the raw SQL string containing stored procedure definitions
sql_create_procedures = """
DROP PROCEDURE IF EXISTS GetLocation;
DROP PROCEDURE IF EXISTS GetSkillSet;
DROP PROCEDURE IF EXISTS GetQualification;
DROP PROCEDURE IF EXISTS GetJobsDetailsById;
DROP PROCEDURE IF EXISTS GetJobsDetailsByEmployeeId;
DROP PROCEDURE IF EXISTS GetApplyJobDetails;

CREATE PROCEDURE GetLocation(IN jobId INT)
BEGIN
    SELECT l.location 
    FROM location l
    JOIN location_mapping lm ON l.id = lm.location_id 
    WHERE lm.job_id = jobId;
END;

CREATE PROCEDURE GetSkillSet(IN jobId INT)
BEGIN
    SELECT ss.skill_set
    FROM skill_sets ss
    JOIN skill_set_mapping ssm ON ss.id = ssm.skill_id
    WHERE ssm.job_id = jobId;
END;

CREATE PROCEDURE GetQualification(IN jobId INT)
BEGIN
    SELECT q.qualification 
    FROM qualification q 
    JOIN qualification_mapping qm ON q.id = qm.qualification_id 
    WHERE qm.job_id = jobId;
END;

CREATE PROCEDURE GetJobsDetailsById(IN jobId INT)
BEGIN
    SELECT 
        jp.id AS job_post_id, jp.job_title, jp.job_description,
        jp.experience, jp.salary_range, jp.no_of_vacancies, jp.created_at,
        c.company_name, c.company_industry, c.company_description, c.no_of_employees,
        c.company_website_link, c.company_logo_path, et.employee_type, jr.job_role
    FROM 
        job_post jp
    LEFT JOIN 
        employees_types et ON jp.employee_type_id = et.id
    LEFT JOIN 
        job_role jr ON jp.job_role_id = jr.id
    LEFT JOIN 
        company_details c ON jp.company_id = c.id
    WHERE 
        jp.id = jobId;
END;

CREATE PROCEDURE GetJobsDetailsByEmployeeId(IN employeeId INT)
BEGIN
    SELECT 
        jp.id AS job_post_id, jp.job_title, jp.job_description,
        jp.experience, jp.salary_range, jp.no_of_vacancies, jp.created_at,
        c.company_name, c.company_industry, c.company_description, c.no_of_employees,
        c.company_website_link, c.company_logo_path, et.employee_type, jr.job_role
    FROM 
        job_post jp
    LEFT JOIN 
        employees_types et ON jp.employee_type_id = et.id
    LEFT JOIN 
        job_role jr ON jp.job_role_id = jr.id
    LEFT JOIN 
        company_details c ON jp.company_id = c.id
    WHERE 
        jp.employee_id = employeeId;
END;

CREATE PROCEDURE GetApplyJobDetails(
    IN userId INT
)
BEGIN
    SELECT 
    jp.id AS job_post_id,jp.job_title, jp.job_description,
    jp.experience, jp.salary_range, jp.no_of_vacancies,jp.created_at,
    c.company_name,c.company_industry,c.company_description, c.no_of_employees,c.company_website_link,c.company_logo_path,et.employee_type,jr.job_role
FROM job_post jp
LEFT JOIN employees_types et ON jp.employee_type_id = et.id
LEFT JOIN job_role jr ON jp.job_role_id = jr.id
LEFT JOIN company_details c ON jp.company_id = c.id
LEFT JOIN apply_job aj ON aj.job_id = jp.id
WHERE aj.user_id = userId;
END;
"""

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Execute the raw SQL to create the stored procedure
session.execute(text(sql_create_procedures))

# Commit the changes
session.commit()

# Close the session
session.close()
       