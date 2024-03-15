from django.db import connection
import bcrypt
# Base = declarative_base()
con = connection.cursor()
# engine = create_engine('mysql://root:mysqllocal@localhost:3306/jobportal')
# Base.metadata.create_all(engine)  # Create tables if not exists
# Session = sessionmaker(bind=engine)
# session = Session()
def demo():
  assert 1==1

# Check email is already registered in the table or not
def email_check(email) :
  check_sql = "SELECT * FROM signup WHERE email = %s"
  query=con.execute(check_sql,[email])
  if query:
    return True
  else:
    return False
  # query = Query(Signup)
  # signup_query = query.filter_by(email=email).first()
  # return signup_query is not None

# Insert the signup data into signup table
# Store the password as hashed format
def signup_query(email,mobile_number,password,signup_by):
  try:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    sql = "INSERT INTO signup(email,mobile_number,password,signup_by) VALUES(%s,%s,%s,%s)"
    value = (email,mobile_number,hashed_password.decode('utf-8'),signup_by)
    con.execute(sql,value)
    # insert_query = insert(Signup).values(
    #     email=email,
    #     mobile_number=mobile_number,
    #     password=hashed_password,
    #     signup_by=signup_by
    # )

    # # Execute the insert query
    # session.execute(insert_query)

    # # Commit the transaction
    # session.commit()
    # return True
  except Exception as e:
    print(f"Error during Signup: {e}")
    return False
