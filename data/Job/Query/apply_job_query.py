from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from django.views.decorators.csrf import csrf_exempt
from data.Account_creation.Tables.table import Signup,ResumeDetails
from sqlalchemy.orm import declarative_base

Base = declarative_base()

@csrf_exempt
def get_user_details(user_id):
    try:
        engine = create_engine('mysql://theuser:thepassword@16.171.19.241:3306/backend1')

        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(Signup).filter_by(id=user_id).first()
        resume = session.query(ResumeDetails).filter_by(user_id=user_id).first()
        if user:
            return user.email, user.mobile_number , resume.resume
        else:
            return None, None , None
    except Exception as e:
        print(f"Error: {e}")
        return None, None
