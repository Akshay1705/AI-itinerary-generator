from django.shortcuts import render
from .gemini_service import generate_itinerary_with_gemini   # ✅ import Gemini service

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



