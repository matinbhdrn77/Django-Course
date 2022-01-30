from django.http.response import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from django.urls import reverse
from django.template.loader import render_to_string

import challenges
# Create your views here.

monthly_challenge = {
    "january": "Eat burger",
    "febuary": "Practice Djange",
    "march": "Do what the hell you want",
    "july": None
}


def index(request):

    months = list(monthly_challenge.keys())
    return render(request, "challenges/index.html", {
        "months": months
    })


def monthly_challenges(request, month):

    try:
        challenge_text = monthly_challenge[month]
        return render(request, "challenges/challenge.html", {
            "text": challenge_text,
            "month": month
        })
    except:
        raise Http404()


def month_by_num(request, month):
    list_month = list(monthly_challenge)
    month = list_month[month - 1]
    path_redirect = reverse("month-challenge", args=[month])
    return HttpResponseRedirect(path_redirect)
