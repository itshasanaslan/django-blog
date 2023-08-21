from django.shortcuts import render
from .api_helpers import DatabaseHelper
from rest_framework.decorators import api_view
from rest_framework.response import Response
import threading

db = DatabaseHelper()

def home(request, *args, **kwargs):
    return render(request, 'vaultafed_home.html',{})

def hidden_database(request, *args, **kwargs):
    db.current_data = db.read_data()
    return render(request, 'vaultafed_database.html',{'data':db.current_data})

@api_view(['GET', 'POST'])
def add_user(request):
    success, response = db.add_user(request.data)
    return Response(response)


@api_view(['GET', 'POST'])
def get_user(request):
    response = db.get_user(request.data)
    if not response:
        response = {
                "username":"null",
                "password":"null",
                "eMail":"null",
                "name":"null",
                "lastName":"null"
            }
    return Response(response)


@api_view(['GET', 'POST'])
def delete_user(request):
    response_obj = db.delete_user(request.data["username"], request.data["AuthCode"])
    return Response(response_obj)

@api_view(['GET', 'POST'])
def update_user(request):
    response_obj = db.update_user(request.data)
    print(request.data)
    return Response(response_obj)

@api_view(['GET', 'POST'])
def send_mail(request):
    check_user = db.get_user(request.data)
    if not check_user:
        return Response(db.create_post_response_obj(False, "Check User", msg = f"No such user found on the database."))

    mail_thread = threading.Thread(target=db.send_email, args=(request.data['eMail'],))
    try:
        mail_thread.start()
        return Response(db.create_post_response_obj(True, "E-Mail", msg = "E-mail has been sent successfully."))
    except Exception as f:
        return Response(db.create_post_response_obj(False, "E-Mail", msg = "Couldn't send e-mail because of: " + f))

@api_view(['GET', 'POST'])
def verify_mail_code(request):
    return Response(db.manage_mail_code(operation = 'verifyCode', email = request.data['eMail'], code = request.data['password']))

@api_view(['GET', 'POST'])
def check_user_exists(request):
    data = db.get_user(request.data)
    if not data:
        return Response(db.create_post_response_obj(False, "Check User", msg = f"No such user found on the database."))
    else:
        return Response(db.create_post_response_obj(True, "Check User", msg = "Found user."))

@api_view(['GET', 'POST'])
def try_login(request):
    return Response(db.check_credentials(request.data))

@api_view(['GET', 'POST'])
def request_logs(request):
    if not db.credentials_check_admin_auth(request.data['AuthCode']):
        db.log("LOG ACCESS", False, "Someone tried to access logs: " + request.json["AuthCode"])
        return Response({"Logs":"Fuck off"})
    
    return Response(db.clear_log())

@api_view(['GET','POST'])
def get_user(request):
    user = db.get_user(request.data)
    if not user:
        data =  {
                "username":"null",
                "password":"null",
                "eMail":"null",
                "name":"null",
                "lastName":"null"}
    else:
        data = {"username":user[0][0],
                "password":user[0][1],
                "eMail":user[0][2],
                "name":user[0][3],
                "lastName":user[0][4],
                "hasPurchased":user[0][5]}
    return Response(data)

@api_view(['GET','POST'])
def get_admin_message(request):
    return Response(db.get_admin_messages())
