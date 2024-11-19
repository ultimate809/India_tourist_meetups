import os
import asyncio
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import Meetup, Attendees
from .forms import AttendeesForm
from .utils.participant_in_queue import  send_participant_in_email_queue

def index(request):
  env = os.getenv("ENVIRONMENT")
  meetups = Meetup.objects.all().order_by('-title')
  return render(request, 'meetups/index.html', { 'meetups': meetups, 'env': env  })

def about(request, meetup_slug):
  print(meetup_slug)
  found = False
  env = os.getenv("ENVIRONMENT")
  selected_meetup = Meetup.objects.get(slug=meetup_slug)
  print(selected_meetup)


  if request.method == 'GET':
    form = AttendeesForm()
    return render(request, 'meetups/meetup-detail.html',
                  {'meetup': selected_meetup, 'meetup_found': True, 'form': form, 'env': env})
  elif request.method == 'POST':
    form = AttendeesForm(request.POST)
    if form.is_valid():
      print("valid form")
      email = form.cleaned_data['email']
      name = form.cleaned_data['name']
      participant, _ = Attendees.objects.get_or_create(email=email, name=name)
      selected_meetup.participants.add(participant)
      request.session['participant_name'] = participant.name
      request.session['participant_email'] = participant.email
      return redirect(reverse('success_register_tag',kwargs={'meetup_slug': meetup_slug}))
    else:
      print("invalid form")
      return render(request, 'meetups/meetup-detail.html',
                    {'meetup': selected_meetup, 'meetup_found': True, 'form': form, 'env': env})

def success_register(request,meetup_slug):
  print(meetup_slug)
  env = os.getenv("ENVIRONMENT")
  selected_meetup = Meetup.objects.get(slug=meetup_slug)
  participant_name = request.session.get('participant_name')
  participant_email = request.session.get('participant_email')

  send_participant_in_email_queue(participant_name,participant_email, selected_meetup)

  print(participant_name)
  return render(request, 'meetups/success.html', {'meetup': selected_meetup, 'participant_name': participant_name, 'env': env})
