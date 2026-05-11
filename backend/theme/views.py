import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .gemini_service import generate_itinerary_with_gemini

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def generate_itinerary_view(request):
    itinerary = None
    destination = None
    itinerary_days = None
    budget = None
    interests = None
    days = None

    if request.method == "POST":
        destination = request.POST.get("destination")
        days = request.POST.get("days")
        budget = request.POST.get("budget")
        interests = request.POST.get("interests")

        itinerary = generate_itinerary_with_gemini(destination, days, budget, interests)

        # ✅ Split by "Day" instead of every line
        itinerary_days = []
        for part in itinerary.split("Day "):
            if part.strip():
                itinerary_days.append("Day " + part.strip())

    return render(request, "generate_itinerary.html", {
        "itinerary_days": itinerary_days,
        "destination": destination,
        "budget": budget,
        "interests": interests,
        "days": days
    })

@csrf_exempt
@require_POST
def generate_itinerary_api(request):
    try:
        data = json.loads(request.body.decode("utf-8") or "{}")
    except ValueError:
        data = {}

    destination = data.get("destination")
    days = data.get("days")
    budget = data.get("budget")
    interests = data.get("interests")

    itinerary = generate_itinerary_with_gemini(
        destination,
        days,
        budget,
        interests
    )

    itinerary_days = itinerary.split("Day ")

    cleaned_days = []

    for day in itinerary_days:
        if day.strip():
            cleaned_days.append("Day " + day.strip())

    return JsonResponse({
        "destination": destination,
        "days": days,
        "budget": budget,
        "interests": interests,
        "itinerary": cleaned_days
    })

