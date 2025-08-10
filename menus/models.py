# menus/models.py

from django.db import models

class TopBarLink(models.Model):
    title = models.CharField(max_length=100, help_text="O texto que será exibido. Ex: Televendas 0800 883 6342")
    # ATUALIZADO: URL opcional para o Televendas
    url = models.CharField(
        max_length=255,
        blank=True,
        help_text="OPCIONAL. Deixe em branco para ser apenas texto. Para WhatsApp, use: https://wa.me/5511999999999"
    )
    icon_class = models.CharField(max_length=100, blank=True, help_text="Ex: fa-solid fa-phone")
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = "Link do Menu Superior"
        verbose_name_plural = "Links do Menu Superior"

class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    is_external = models.BooleanField(default=False, help_text="Marque se for um link para outro site.")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = "Item do Menu Principal"
        verbose_name_plural = "Itens do Menu Principal"