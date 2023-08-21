import sqlite3
import re
import smtplib
import random
import json
import string
from datetime import datetime
from email.mime.text import MIMEText
import os

DIRECTORY = os.path.join(os.getcwd(), 'vaultafed')

class DatabaseHelper:
	def __init__(self, connection = True ,data_folder = "system_data", database_file = '/vaultafed_sql.db'):
		current_dir = '/var/www/itshasanaslan/vaultafed/system_data'
		self.data_folder = data_folder
		self.database_connection = None
		self.data_directory = os.path.join(DIRECTORY, data_folder)
		self.data_location = os.path.join(current_dir, "vaultafed_sql.db")
		self.admin_messages_location = os.path.join(current_dir, "admin_messages")
		self.current_data = []
		self.logs = []
		self.success_code = "Success"
		self.fail_code = "Failed:"
		self.operation_counter = 0 # for logs
		self.log_filename = os.path.join(current_dir, "logs.json")
		self.mail_codes_file = os.path.join(current_dir, "mail_codes.json")
		self.essentials_cred_file =  os.path.join(current_dir, "essential.json")
		self.tokens_file =  os.path.join(current_dir, "tokens.json")
		self.admin_messages = {}
		

		if connection:
			self.connect()

	def connect(self):
		try:
			self.database_connection = sqlite3.connect(self.data_location, check_same_thread=False)
			print("Connected database:",self.data_location)
			self.log("Init",True, "Connected to database.")
		except Exception as f:
			print('sql connect error',f, self.data_location)

	def create_tables(self):
		#never use this!
		table_cursor = self.database_connection.cursor()
		table_cursor.execute('''CREATE TABLE Users(
			username,
			name text,
			lastName text,
			password text,
			eMail text,
			hasPurchased integer
		)''')
		self.database_connection.commit()

	def safe_sql_query(self, info_dict):
		for i in info_dict.items():
			for j in i:
				if i in [',',";"]:
					return False, self.create_post_response_obj(False, "Sql Query",msg = "Failed: SQL Injection Detected!")
		return True, {}
                	

	def add_user(self,info_dict):
		temp_success, temp_response = self.safe_sql_query(info_dict)
		if not temp_success:
			return temp_response

		cursor = self.database_connection.cursor()
		parameters = """insert into users (username,name,lastName,password,email,hasPurchased) values(?,?,?,?,?,?);"""

		username = info_dict.get("username")
		name = info_dict.get('name')
		surname = info_dict.get("lastName")
		passw = info_dict.get("password")
		mail = info_dict.get("eMail")
		sla = info_dict.get("hasPurchased")
		parameter_values = (username,name,surname,passw,mail,sla)
		#parameter_values = (user.name, user.surname, user.birth_year, user.password, user.email, user.salary)
		try:
			cursor.execute(parameters, parameter_values)
			self.database_connection.commit()
			cursor.close()
			self.log("Add User", True, f"User '{info_dict['username']}' saved to database successfully.")
			self.save_token(username, info_dict["AuthCode"])
			return True, self.create_post_response_obj(True, "Save User", msg = f"User '{info_dict['username']}' saved to database successfully.")
		
		except Exception as ff:
			cursor.close()
			self.log("Add User", False, f"Couldn't save user  '{info_dict['username']}': {ff} ")
			return False, self.create_post_response_obj(False, "Save User",msg = self.fail_code + " " + str(ff))

	def read_data(self):
		cursor = self.database_connection.execute("select * from Users")
		data = cursor.fetchall()
		cursor.close()
		return data

	def delete_user(self, user_info, auth_code):
		if not self.check_token(user_info, auth_code):
			return self.create_post_response_obj(False, "Delete User", msg = "Invalid token.")

		cursor = self.database_connection.cursor()
		try:
			if DatabaseHelper.check_is_mail(user_info):
				parameters = f"""DELETE FROM users where eMail = '{user_info}'"""
			else:
				parameters = f"""DELETE FROM users where username = '{user_info}'"""
			cursor.execute(parameters)
			self.database_connection.commit()
			cursor.close()
			msg = f"User '{user_info}' has been deleted successfully."
			self.log('Delete User', True, msg)
			self.delete_token(user_info)
			return self.create_post_response_obj(True, "Delete User", msg = msg)
		except Exception as f:
			cursor.close()
			msg  = f"Couldn't delete user '{user_info}': {f}"
			self.log('Delete User', False, msg)
			return self.create_post_response_obj(False, "Delete User", msg = msg)

	def update_user(self, kwargs):
		if not self.check_token(kwargs["eMail"], kwargs["AuthCode"], True):
			return self.create_post_response_obj(False, "Update User", msg = "Invalid token or user info. Update receives only email info.")

		parameters = f"""UPDATE users set username = '{kwargs['username']}', password = '{kwargs['password']}', name = '{kwargs['name']}', lastName = '{kwargs['lastName']}', hasPurchased = '{kwargs["hasPurchased"]}', eMail = '{kwargs['eMail']}' where username = '{kwargs['username']}'"""
		cursor = self.database_connection.cursor()
		try:
			cursor.execute(parameters)
			self.database_connection.commit()
			cursor.close()
			msg = f"User '{kwargs['username']}' has been updated."
			self.log('Update User',True, msg)
			return self.create_post_response_obj(True, "Update User", msg = msg)
		except Exception as f:
			cursor.close()
			msg = f"Couldn't update user '{kwargs['username']}' because of : {f}"
			self.log('Update User', False, msg)
			return  self.create_post_response_obj(False, "Update User", msg = msg)

	def get_user(self,data):
		cursor = self.database_connection.cursor()
		if data["eMail"] != "" and data["eMail"] != None and self.check_is_mail(data['eMail']):
			cursor.execute("SELECT * FROM users WHERE eMail=?", (data["eMail"],))
		else:
			cursor.execute("SELECT * FROM users WHERE username=?", (data["username"],))
		result = cursor.fetchall()

		if len(result) == 0:
			self.log('Get User', True, f"No such user record found: {data['username']}.")
			return False
		else:
			self.log('Get User', True, f"Returned {data['username']}'s data.")
			return result

		cursor.close()
		
	

	def check_credentials(self, data):
		user = self.get_user(data)
		if not user:
			return self.create_post_response_obj(False, "Log in", msg = "No such user found.")
		else:
			user = user[0]
			if user[1] == data['password']: # data comes as a list, password is the second index.
				self.log('Log in', True, f"Access granted to '{user[0]}'.")
				auth_code = self.get_token(data["username"], data["eMail"])
				return self.create_post_response_obj(True, "Log in", msg = "Access granted. SPLITHERE" + auth_code)
			else:
				self.log('Log in', False, msg = f"Access denied for '{data['username']}', invalid password.")
				return self.create_post_response_obj(False, "Log in", msg = f"Access denied, invalid password.")

	def credentials_encrypt_file(self, file):
		with open(file,'rb') as f:
			raw_data = f.read()

		l = 1
		while l % 2 == 1:
			l = random.randint(0, 100)

		temp = [l]

		for i in range(len(raw_data)):
			x  = raw_data[i] + l
			if x > 255:
				x = l + 1
			
			temp.append(x)

		return bytearray(temp)

	def credentials_retrive_data(self, file):
		with open(file, "rb") as f:
			raw_data = f.read()
	
		l = raw_data[0]
		temp = []

		for i in range(1, len(raw_data)):
			x = raw_data[i] - l
			if x < l:
				x = 255 - l

			temp.append(x)
		self.log('Retrieve Admin', True, 'Retrieved essential data.')
		return eval(bytearray(temp))

	def credentials_save(self, file, data):

		with open(file, 'wb') as f:
			f.write(data)

	def credentials_check_admin_auth(self, code):
		data= self.credentials_retrive_data(self.essentials_cred_file)
		return code == data["password"]

	@staticmethod
	def check_is_mail(mail):
		regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
		return re.search(regex,mail)

	def create_post_response_obj(self, success, operation_type, msg = "Cool"):
		return {
			"OperationSuccessful":success,
			"OperationType":operation_type,
			"ServerMessage":msg
		}

	def manage_mail_code(self, **kwargs):
		codes = {}
		with open(self.mail_codes_file, 'r') as file:
			codes = json.load(file)

		if kwargs['operation'] == "add":
			codes[kwargs['email']] = kwargs['code']

		elif kwargs['operation'] == "get":
			if kwargs['email'] in codes:
				return codes[kwargs['email']]
			else:
				return None
		elif kwargs['operation'] == "verifyCode":
			if kwargs['email'] in codes:
				if kwargs['code'] == codes[kwargs['email']]:
					codes.pop(kwargs['email'], None)
					self.save_mail_json(codes)
					self.log('Mail Code',True, f"Generated a code for '{kwargs['email']}'")
					return self.create_post_response_obj(True, "Check Mail Code", msg = 'Match')
				else:
					msg = "Invalid"
					self.log('Mail code', False, f"Invalid code passed for '{kwargs['email']}'")
			else:
				msg = "No code found"

			return self.create_post_response_obj(False, "Check Mail Code", msg = msg)
		else:
			raise Exception("Invalid operation")

		self.save_mail_json(codes)

	def save_mail_json(self,data):
		with open(self.mail_codes_file,'w') as file:
			json.dump(data, file)

	def send_email(self, to):
		d = self.credentials_retrive_data(self.essentials_cred_file)
		EMAIL_ADDRESS = d['mail']
		PASSWORD = d['password']

		mail_code = self.generate_mail_code(8)
		self.manage_mail_code(operation='add', email = to, code = mail_code )

		msg = f'Verification code for password reset : '  + mail_code + "\nPlease do not share this code."
		subject = 'Vaultafed Password Reset'

		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login(EMAIL_ADDRESS,PASSWORD)

		message = 'Subject: {}\n\n{}'.format(subject,msg)
		server.sendmail(EMAIL_ADDRESS,to,message)
		#os.system(f"echo {msg} | mail -s '{subject}' {to}")
		self.log('Send Mail',True, f"Sent a mail to '{to}'.")
		server.quit()

	def generate_mail_code(self, length):
		letters = string.ascii_letters + string.digits
		return  ''.join(random.choice(letters).upper() for i in range(length))

	def log(self, operation, success ,msg):
		return # I decided not to log.
		exact_time = datetime.today().strftime('%d-%m-%Y %H:%M:%S') 
		msg = f"{exact_time} [{operation}]({str(success).upper()}) {msg}"
		self.logs.append(msg)
		self.operation_counter += 1
		if self.operation_counter >= 4:
			with open(self.log_filename,"a") as f:
				o = ''
				for i in self.logs:
					o += i + '\n'
					f.write(o)

			self.operation_counter = 0
			self.logs.clear()


	def save_token(self, username, token):
		with open(self.tokens_file, 'r') as file:
			data = eval(file.read())
		data[username] = token

		with open(self.tokens_file, 'w') as f:
			json.dump(data, f)
		
	def check_token(self, username, token, from_system = False):
		if from_system:
			data = self.credentials_retrive_data(self.essentials_cred_file)
			return data["AuthCode"] == token

		user = self.get_user({'username':username, 'eMail':username})
		if not user:
			return False
		username = user[0][0]
		user_mail = user[0][2]
		with open(self.tokens_file , 'r') as f:
			data = eval(f.read())
		if username not in data:
			if user_mail not in data:
				return False
		return data[username] == token

	def delete_token(self, username):
		with open(self.tokens_file, 'r') as f:
			data = eval(f.read())
		try:
			del data[username]
		except Exception as f:
			self.log("Delete Token", False, msg = str(f) + ":" + username)
		
		with open(self.tokens_file, 'w') as file:
			json.dump(data, file)

	def get_token(self, user_info, user_mail):
		with open(self.tokens_file, 'r') as file:
			data = eval(file.read())
		if not user_info in data:
			return user_mail
		return data[user_info]

	def clear_log(self):
		with open(self.log_filename, 'r') as f:
			logs = f.read()

		with open(self.log_filename, 'w') as f:
			self.log("Log Clear", True, "Cleared log.")

		return {"logs":logs}


	def get_admin_messages(self):
		if not os.path.exists(self.admin_messages_location):
			data =  self.create_post_response_obj(False, "Get Messages", msg="No")
			data["Id"] = 0
			return data
			
		with open(self.admin_messages_location, 'r') as file:
			data = eval(file.read())
		max = 0
		for i,j in data.items():
			if i > max:
				max = i
		data_to_send = self.create_post_response_obj(True, "Get Messages", msg = data[max])
		data_to_send["Id"] = max
		return data_to_send
# önce token requesti alacak. Sonra o token ile servera bağlanacak.
