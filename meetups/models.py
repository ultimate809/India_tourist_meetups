from django.db import models

class Location(models.Model):
  name = models.CharField(max_length=100)
  code = models.CharField(max_length=100)

  def __str__(self):
    return f"{self.name} ({self.code})"

class Attendees(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField()
  def __str__(self):
    return self.name

class Organiser(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField()
  def __str__(self):
    return self.name

class Meetup(models.Model):
  title = models.CharField(max_length=255)
  organiser = models.ForeignKey(Organiser, on_delete=models.CASCADE)
  date = models.DateField()
  location = models.ForeignKey(Location, on_delete=models.CASCADE)
  slug = models.SlugField(unique=True)
  description = models.TextField()
  image = models.ImageField(upload_to='meetups')
  participants = models.ManyToManyField(Attendees, blank=True,null=True)

  def __str__(self):
    return self.title
  def get_absolute_url(self):
    pass

