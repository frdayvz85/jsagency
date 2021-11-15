from .models import Subscribe, Setting
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect

# def subscribers(request):
#     socials = Setting.objects.get(pk=1)

#     return {'social': socials}