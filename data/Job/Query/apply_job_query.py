from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from django.views.decorators.csrf import csrf_exempt
from data.Account_creation.Tables.table import Signup,CompanyDetails,Address
from sqlalchemy.orm import declarative_base
import json
import base64

Base = declarative_base()

@csrf_exempt
def get_user_details(user_id):
    try:
        print(user_id)
        engine = create_engine('mysql://theuser:thepassword@16.171.19.241:3306/backend1')

        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine) 
        session = Session()
        query=select([Signup.email, Signup.mobile_number]).where(Signup.id==user_id)
        result=session.execute(query)
        # Fetch the result
        row = result.fetchone()
        session.close()

        # Check if a result is found
        if row:
            email, mobile_number = row
            return email,mobile_number
        else:
            return None,None
    except Exception as e:
      print(f"Error: {e}")
      return None
    