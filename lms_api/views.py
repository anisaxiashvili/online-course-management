from django.shortcuts import render

def landing_page(request):
    return render(request, "login.html")

def signup_page(request):
    return render(request, "signup.html")

def courses_page(request):
    return render(request, "courses.html")

def course_detail_page(request):
    return render(request, "course_detail.html")

def lecture_detail_page(request):
    return render(request, "lecture_detail.html")

def assignment_detail_page(request):
    return render(request, "assignment_detail.html")