from django.shortcuts import render


def simulation(request):
    return render(request, 'phishing_sim/simulation.html')