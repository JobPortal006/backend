from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from django.http import JsonResponse
from data.Account_creation.Tables.table import Signup, ResumeDetails
from sqlalchemy.orm import declarative_base
from django.views.decorators.csrf import csrf_exempt
import base64

Base = declarative_base()

@csrf_exempt
def get_user_details(user_id):
    try:
        engine = create_engine('mysql://theuser:thepassword@13.51.207.189:3306/backend1')
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        user = session.query(Signup).filter_by(id=user_id).first()
        resume = session.query(ResumeDetails).filter_by(user_id=user_id).first()
        resume_base64 = base64.b64encode(resume.resume).decode('utf-8')
        response_data = {
                'email': user.email,
                'mobile_number': user.mobile_number,
                'resume': resume_base64
        }
        return response_data

    except Exception as e:
        print(f"Error: {e}")
        return {'status': 'Error', 'message': str(e)}
