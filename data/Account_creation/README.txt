Signup Page :

Table Name - Signup
Columns :
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(100) NOT NULL,
  mobileNumber VARCHAR(15) NOT NULL,
  password VARCHAR(255) NOT NULL,
  signupBy ENUM('User', 'Recruiter') NOT NULL,
  signupTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  loggedinTime TIMESTAMP

Insert the data into signup table
Data will store both User and Recruiter on same table
Check email is already registered in table or not
Password is inserted in hash format
Once registered - Send mail to registered email as (Signup Successfully message)

Login Page :

Check email and password is registered or not in Signup table
Create a token for each email and send token to response
Once logged in, update the loggedin time in table
Check mobile number is already registered or not in signup table 

Forget Password Page :

Check email is registered or not in Signup table
Sent mail to registered email for change password
Update password in signup Table and inserted in hash format

Creata Account User Page :

Insert the data into required tables
Data will store both User and Recruiter on same table
Get user_id, email data by using mobile_number
Store profile_picture and resume fils on project folders (Profile Picture and Resume)
Once registered - Send mail to registered email as (Account Created Successfully message)

Table Name - personal_details
Columns :
  personal_details_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  registered_by ENUM('User', 'Recruiter') NOT NULL,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  date_of_birth VARCHAR(50) NOT NULL,
  gender ENUM('Male', 'Female','Others') NOT NULL,
  profile_picture VARCHAR(255), 
  FOREIGN KEY (user_id) REFERENCES Signup(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

Table Name - address
Columns :
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  registered_by ENUM('User', 'Recruiter') NOT NULL,
  street VARCHAR(255),
  city VARCHAR(50),
  state VARCHAR(50),
  country VARCHAR(50),
  pincode VARCHAR(15),
  address_type ENUM('Permanent', 'Current'),
  FOREIGN KEY (user_id) REFERENCES Signup(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

Table Name - education_details
Columns : 
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  sslc_school_name VARCHAR(100) NOT NULL,
  sslc_start_year INT NOT NULL,
  sslc_end_year INT NOT NULL,
  sslc_percentage DECIMAL(5, 2) NOT NULL,
  hsc_school_name VARCHAR(100),
  hsc_start_year INT,
  hsc_end_year INT,
  hsc_percentage DECIMAL(5, 2),
  FOREIGN KEY (user_id) REFERENCES Signup(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

Table Name - college_details 
Columns : 
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  college_name VARCHAR(100) NOT NULL,
  start_year INT NOT NULL,
  end_year INT NOT NULL,
  percentage DECIMAL(5, 2) NOT NULL,
  department VARCHAR(50) NOT NULL,
  degree VARCHAR(100) NOT NULL,
  education_type ENUM('UG', 'PG', 'Diploma') NOT NULL,
  FOREIGN KEY (user_id) REFERENCES Signup(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

Table Name - professional_details 
Columns : 
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  company_name VARCHAR(100),
  years_of_experience INT,
  job_role VARCHAR(100),
  skills VARCHAR(255),
  registered_by ENUM('User', 'Employee'),
  FOREIGN KEY (user_id) REFERENCES Signup(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

Table Name - resume_details 
Columns : 
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  registered_by ENUM('User', 'Recruiter') NOT NULL,
  employment_status ENUM('Fresher', 'Experienced') NOT NULL,
  resume VARCHAR(255) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES Signup(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

Table Name - job_preferences 
Columns : 
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  key_skills VARCHAR(255) NOT NULL,
  industry VARCHAR(100) NOT NULL,
  department VARCHAR(100) NOT NULL,
  preferred_locations VARCHAR(255) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES Signup(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP