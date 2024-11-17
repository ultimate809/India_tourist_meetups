import os
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import Meetup, Attendees
from .forms import AttendeesForm


def index(request):
  env = os.getenv("ENVIRONMENT")
  meetups = Meetup.objects.all()
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
      user_email = form.cleaned_data['email']
      name = form.cleaned_data['name']
      participant, _ = Attendees.objects.get_or_create(email=user_email, name=name)
      selected_meetup.participants.add(participant)
      request.session['participant_name'] = participant.name
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
  print(participant_name)
  return render(request, 'meetups/success.html', {'meetup': selected_meetup, 'participant_name': participant_name, 'env': env})
