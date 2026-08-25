from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404, render
from .models import Attempt, Scenario


@login_required
def scenario_list(request):
    scenarios = Scenario.objects.annotate(
        answered=Exists(
            Attempt.objects.filter(
                user=request.user, 
                scenario=OuterRef("pk")
            )
        )
    )
    return render(
        request, 
        "phishing_sim/scenario_list.html", 
        {"scenarios": scenarios}
    )


@login_required
def scenario_detail(request, pk):
    scenario = get_object_or_404(Scenario, pk=pk)
    attempt = Attempt.objects.filter(user=request.user, scenario=scenario).first()

    if request.method == "POST" and not attempt:
        user_choice = request.POST.get("answer")
        if user_choice in ["phishing", "safe"]:
            marked_as_phishing = (user_choice == "phishing")
            attempt = Attempt.objects.create(
                user=request.user,
                scenario=scenario,
                marked_as_phishing=marked_as_phishing,
                is_correct=(marked_as_phishing == scenario.is_phishing),
            )

    return render(
        request,
        "phishing_sim/scenario_detail.html",
        {
            "scenario": scenario,
            "attempt": attempt,
        },
    )