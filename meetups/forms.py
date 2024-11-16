from django import forms
from .models import Attendees

class AttendeesForm(forms.ModelForm):
  class Meta:
    model = Attendees
    fields = '__all__'