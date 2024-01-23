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

Insert data into signup table
Check email is already register or not in signup table
Once signup is successful , sent mail to registered email address


Login Page :

Check email and password from signup Table
Check email is register or not in signup table
Update the logged in time (loggedinTime) column

Forget Password Page :
Check email is register or not in signup table
Sent mail for change the Password

Update Password Function
Update the password in Signup table