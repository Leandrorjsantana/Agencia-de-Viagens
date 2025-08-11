# subscribers/models.py

from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="E-mail do Inscrito")
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Inscrição")

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "Inscrito na Newsletter"
        verbose_name_plural = "Inscritos na Newsletter"