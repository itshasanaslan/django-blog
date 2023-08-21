from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .db_helper import HandleDatabase
import os


db_handler = HandleDatabase()



def home(request, *args, **kwargs):
    return HttpResponse("<h1>There is nothing to show here, yet. </h1>")

@api_view(['GET', 'POST'])
def attendance_page(request):
    if request.method ==  "GET":
        return HttpResponse("<h1>Please wait for new ÇDM Course Modules<br><i>itshasanaslan@gmail.com</i></h1>")
        print("attendance")
        students = db_handler.get_students()
        lessons = db_handler.get_lessons()
        return render(request, 'form.html', {"students":students, "lessons":lessons})
    else:
        user_id = request.POST.get("students")
        lesson_time = request.POST.get("lessons")
        excuse = request.POST.get("excuse")
        if not user_id or not lesson_time or not excuse:
            return HttpResponse("<h1>An error occured.<br>Contact itshasanaslan@gmail.com</h1>")
        try:
            db_handler.add_excuse(user_id, lesson_time, excuse)
        except Exception as f:
            return HttpResponse(f"<h1>An error occured: {f}</h1>")
        return render(request, "done.html")

@csrf_exempt
@api_view(['GET', 'POST'])
def get_results(request, *args, **kwargs):
    global db_handler
    if request.method == "POST":
        print("Incoming post request")
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"Status":"Error","Message":"Provide a username and password."})
        if username != "admin" or password != db_handler.passcode:
            return Response({"Status":"Denial","Message":"Invalid  username or password."})
        return Response({"Status":"Success", "Data":db_handler.get_excuses_list() })
    else:
        return HttpResponse("<h1>Bad request bruh!</h1>")



