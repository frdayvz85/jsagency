from .models import Social, ContactInfo
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect

def socials(request):
    social = Social.objects.get(pk=1)

    return {'social': social}


def contact(request):
    contact = ContactInfo.objects.get(pk=1)

    return {'contact': contact}