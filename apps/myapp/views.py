from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Athlete
from django.views.decorators.csrf import csrf_exempt


# Athlete.objects.all().delete()

# Create your views here.
def index(request):
    athletes = Athlete.objects.all()
    return render(request, 'index.html', {'athletes': athletes})

# def test(request, num):
#     return render(request, 'index.html', {'num':num})


def search(request):
    athletes = Athlete.objects.all()
    return render(request, 'search.html', {'athletes':athletes})

def create(request):
    # print(request.POST)

    result = Athlete.objects.validator(request.POST)
    # print(result)

    if not result[0]:
        for key, error in result[1].items():
            messages.add_message(request, messages.ERROR, error, extra_tags=key)

    return redirect('/')

@csrf_exempt
def athlete_api(request):
    print(request.POST)
    athletes = Athlete.objects.all().order_by('created_at').reverse()[0:int(request.POST['num'])]
    return render(request, 'table.html', {'athletes': athletes})

@csrf_exempt
def athlete_images(request):
    print(request.POST)

    # example of request.POST with everything checked:
    # <QueryDict: {'search_string': ['hello'], 'female': [''], 'male': [''], 'gymnastics': ['on'], 'climbing': ['on'], 'tennis': ['on'], 'soccer': ['on'], 'boxing': ['on'], 'mma': ['on'], 'snowboarding': ['on']}>

    form = request.POST


    # ======= SEARCH_STRING =======
    search_string = form["name"]
    athletes1 = Athlete.objects.filter(fname__contains=search_string)
    athletes2 = Athlete.objects.filter(lname__contains=search_string)

    athletes = athletes1 | athletes2

    # ======= GENDER =======
    if 'female' in form and 'male' in form:
        pass
    elif 'female' in form:
        athletes = athletes.filter(gender="Female")
    elif 'male' in form:
        athletes = athletes.filter(gender="Male")

    # ======= SPORT =======
    if 'gymnastics' in form:
        gym = athletes.filter(sport="Gymnastics")
    else:
        gym = Athlete.objects.none()

    if 'climbing' in form:
        climb = athletes.filter(sport="Climbing")
    else:
        climb = Athlete.objects.none()

    if 'tennis' in form:
        tennis = athletes.filter(sport="Tennis")
    else:
        tennis = Athlete.objects.none()

    if 'running' in form:
        running = athletes.filter(sport="Running")
    else:
        running = Athlete.objects.none()

    if 'boxing' in form:
        boxing = athletes.filter(sport="Boxing")
    else:
        boxing = Athlete.objects.none()

    if 'snowboarding' in form:
        snowboarding = athletes.filter(sport="Snowboarding")
    else:
        snowboarding = Athlete.objects.none()

    if 'mma' in form:
        mma = athletes.filter(sport="MMA")
    else:
        mma = Athlete.objects.none()

    # ======= RESULT_LIST =======
    if 'gymnastics' not in form and 'climbing' not in form and 'tennis' not in form and 'running' not in form and 'boxing' not in form and 'snowboarding' not in form and 'mma' not in form:
        result_list = athletes
    else:
        result_list = gym | climb | tennis | running | mma | snowboarding | boxing

    return render(request, 'athlete_images.html', {'athletes':result_list})
