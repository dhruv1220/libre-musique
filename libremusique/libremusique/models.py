from django.db import models
from django.conf import settings

class Collaborator(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    instrument = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.instrument})"


class Recital(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    venue = models.CharField(max_length=255)
    time = models.TimeField()

    def __str__(self):
        return f"{self.name} at {self.venue} on {self.date} at {self.time}"


class Piece(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # user = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    composer = models.CharField(max_length=255)
    date_started = models.DateField()
    key = models.CharField(max_length=50)
    collaborators = models.ManyToManyField(Collaborator, related_name='pieces', blank=True)
    recital = models.ManyToManyField(Recital, related_name='pieces', blank=True)

    def __str__(self):
        return self.name
    

class Note(models.Model):
    piece = models.ForeignKey(Piece, related_name='notes', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"Note for {self.piece.name}: {self.text[:50]}..."

