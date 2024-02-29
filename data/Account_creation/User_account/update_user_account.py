from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from data.Account_creation.Tables.table import Signup, PersonalDetails, ProfessionalDetails, Address, CollegeDetails, EducationDetails, JobPreferences, ResumeDetails
import json
import base64
from data.Account_creation.Query import create_account_user_query
from data.Account_creation import message
from sqlalchemy.orm import declarative_base

Base = declarative_base()

@csrf_exempt
def update_user_details(request):
    try:
        # data = json.loads(request.body)
        # print(data)
        # user_details = data.get('data', {}).get('userDetails', {})
        # address_data = data.get('data', {}).get('address', {})
        # education_data = data.get('data', {}).get('education_details', {})
        # job_preference_data = data.get('data', {}).get('jobPreference', {})
        user_details = json.loads(request.POST.get('userDetails', '{}'))
        print(user_details)
        address_data = json.loads(request.POST.get('address', '{}'))
        print(address_data)
        education_data = json.loads(request.POST.get('education', '{}'))
        print(education_data)
        job_preference_data = json.loads(request.POST.get('jobPreference', '{}'))
        print(job_preference_data)
        professional_details_data = json.loads(request.POST.get('professionalDetails'))
        print(professional_details_data)

        # Extracting user details
        first_name = user_details.get('first_name')
        last_name = user_details.get('last_name')
        gender = user_details.get('gender')
        date_of_birth = user_details.get('date_of_birth')
        mobile_number = user_details.get('mobile_number')
        profile_picture = request.FILES.get('profilePicture')
        resume = request.FILES.get("resume")

        # Extracting current address details
        current_address = address_data.get('current', {})
        street_current = current_address.get('street')
        city_current = current_address.get('city')
        state_current = current_address.get('state')
        country_current = current_address.get('country')
        pincode_current = current_address.get('pincode')
        address_type_current = current_address.get('address_type')

        # Extracting permanent address details
        permanent_address = address_data.get('permanent', {})
        street_permanent = permanent_address.get('street')
        city_permanent = permanent_address.get('city')
        state_permanent = permanent_address.get('state')
        country_permanent = permanent_address.get('country')
        pincode_permanent = permanent_address.get('pincode')
        address_type_permanent = permanent_address.get('address_type')

        # Extracting education details
        sslc_school_name = education_data.get('sslc_school_name')
        sslc_start_year = education_data.get('sslc_start_year')
        sslc_end_year = education_data.get('sslc_end_year')
        sslc_percentage = education_data.get('sslc_percentage')
        hsc_school_name = education_data.get('hsc_school_name')
        hsc_start_year = education_data.get('hsc_start_year')
        hsc_end_year = education_data.get('hsc_end_year')
        hsc_percentage = education_data.get('hsc_percentage')
        college_name = education_data.get('college_name')
        college_start_year = education_data.get('college_start_year')
        college_end_year = education_data.get('college_end_year')
        college_percentage = education_data.get('college_percentage')
        department = education_data.get('department')
        degree = education_data.get('degree')
        education_type = education_data.get('education_type')
        pg_college_degree = education_data.get("pg_college_degree")
        pg_college_department = education_data.get("pg_college_department")
        pg_college_end_year = education_data.get("pg_college_end_year")
        pg_college_name = education_data.get("pg_college_name")
        pg_college_percentage = education_data.get("pg_college_percentage")
        pg_college_start_year = education_data.get("pg_college_start_year")
        diploma_college_name = education_data.get("diploma_college_name")
        diploma_college_start_year = education_data.get("diploma_college_start_year")
        diploma_college_end_year = education_data.get("diploma_college_end_year")
        diploma_college_percentage = education_data.get("diploma_college_percentage")
        diploma_college_department = education_data.get("diploma_college_department")
        diploma_college_degree = education_data.get("diploma_college_degree")

        # Extracting job preference details
        department = job_preference_data.get('department')
        industry = job_preference_data.get('industry')
        key_skills = job_preference_data.get('key_skills')
        prefered_locations = job_preference_data.get('preferred_locations')

        # Extracting professional details
        # professional_details_list = professional_details_data.get("companies", [])

        # Fetching user ID
        user_id, registered_by, mobile_number = create_account_user_query.mobile_number(mobile_number)
        print(user_id, registered_by, mobile_number)

        # Creating SQLAlchemy engine and session
        engine = create_engine('mysql://theuser:thepassword@13.51.207.189:3306/backend1')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Update PersonalDetails table
        personal_details = session.query(PersonalDetails).filter_by(user_id=user_id).first()
        if personal_details:
            personal_details.date_of_birth = date_of_birth
            personal_details.first_name = first_name
            personal_details.gender = gender
            personal_details.last_name = last_name

        # Update Address table for current address
        current_address_obj = session.query(Address).filter_by(user_id=user_id, address_type='Current').first()
        if current_address_obj:
            current_address_obj.city = city_current
            current_address_obj.country = country_current
            current_address_obj.pincode = pincode_current
            current_address_obj.state = state_current
            current_address_obj.street = street_current
        else:
            new_current_address = Address(user_id=user_id, address_type='Current', city=city_current,
                                          country=country_current, pincode=pincode_current, state=state_current,
                                          street=street_current)
            session.add(new_current_address)

        # Update Address table for permanent address
        permanent_address_obj = session.query(Address).filter_by(user_id=user_id, address_type='Permanent').first()
        if permanent_address_obj:
            permanent_address_obj.city = city_permanent
            permanent_address_obj.country = country_permanent
            permanent_address_obj.pincode = pincode_permanent
            permanent_address_obj.state = state_permanent
            permanent_address_obj.street = street_permanent
        else:
            new_permanent_address = Address(user_id=user_id, address_type='Permanent', city=city_permanent,
                                            country=country_permanent, pincode=pincode_permanent, state=state_permanent,
                                            street=street_permanent)
            session.add(new_permanent_address)

        # Update EducationDetails table
        education_details = session.query(EducationDetails).filter_by(user_id=user_id).first()
        if education_details:
            education_details.hsc_end_year = hsc_end_year
            education_details.hsc_start_year = hsc_start_year
            education_details.hsc_percentage = hsc_percentage
            education_details.hsc_school_name = hsc_school_name
            education_details.sslc_end_year = sslc_end_year
            education_details.sslc_percentage = sslc_percentage
            education_details.sslc_school_name = sslc_school_name
            education_details.sslc_start_year = sslc_start_year

        # Update CollegeDetails table for UG education type
        college_details_ug = session.query(CollegeDetails).filter_by(user_id=user_id, education_type='UG').first()
        if college_details_ug:
            college_details_ug.end_year = college_end_year
            college_details_ug.college_name = college_name
            college_details_ug.percentage = college_percentage
            college_details_ug.start_year = college_start_year
            college_details_ug.degree = degree
            college_details_ug.department = department

        # Update CollegeDetails table for PG education type
        college_details_pg = session.query(CollegeDetails).filter_by(user_id=user_id, education_type='PG').first()
        if college_details_pg:
            college_details_pg.degree = pg_college_degree
            college_details_pg.department = pg_college_department
            college_details_pg.end_year = pg_college_end_year
            college_details_pg.college_name = pg_college_name
            college_details_pg.percentage = pg_college_percentage
            college_details_pg.start_year = pg_college_start_year

        # Update CollegeDetails table for Diploma education type
        college_details_diploma = session.query(CollegeDetails).filter_by(user_id=user_id, education_type='Diploma').first()
        if college_details_diploma:
            college_details_diploma.degree = diploma_college_degree
            college_details_diploma.department = diploma_college_department
            college_details_diploma.end_year = diploma_college_end_year
            college_details_diploma.college_name = diploma_college_name
            college_details_diploma.percentage = diploma_college_percentage
            college_details_diploma.start_year = diploma_college_start_year

        # Update JobPreferences table
        job_preferences = session.query(JobPreferences).filter_by(user_id=user_id).first()
        if job_preferences:
            job_preferences.department = department
            job_preferences.industry = industry
            job_preferences.key_skills = key_skills
            job_preferences.preferred_locations = prefered_locations

        # Update ProfessionalDetails table
        # professional_details = session.query(ProfessionalDetails).filter_by(user_id=user_id).all()
        # for i, prof_detail in enumerate(professional_details):
        #     if i < len(professional_details_list):
        #         company = professional_details_list[i]
        #         prof_detail.company_name = company.get('company_name')
        #         prof_detail.years_of_experience = company.get('years_of_experience')
        #         prof_detail.job_role = company.get('job_role')
        #         prof_detail.skills = company.get('skills')

        session.commit()
        session.close()

        return JsonResponse({"message": "Data updated successfully"})
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": "Failed to update data"})
