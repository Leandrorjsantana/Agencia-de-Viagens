# menus/models.py
from django.db import models

class TopBarLink(models.Model):
    title = models.CharField(max_length=100, help_text="O texto que será exibido. Ex: Televendas 0800 883 6342")
    url = models.CharField(max_length=255, blank=True, help_text="OPCIONAL. Deixe em branco se não for um link.")
    icon_class = models.CharField(max_length=100, blank=True, help_text="Ex: fa-solid fa-phone.")
    # --- NOVO CAMPO ADICIONADO AQUI ---
    open_in_new_tab = models.BooleanField(default=True, verbose_name="Abrir em nova aba?")
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = "Link do Menu Superior"
        verbose_name_plural = "Links do Menu Superior"

# ... (O resto do ficheiro continua igual)
class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    is_external = models.BooleanField(default=False, help_text="Marque se for um link para outro site.")
    order = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['order']
        verbose_name = "Item do Menu Principal"
        verbose_name_plural = "Itens do Menu Principal"

class SocialMediaLink(models.Model):
    name = models.CharField(max_length=100, help_text="Ex: Facebook, Instagram")
    url = models.URLField(max_length=255)
    icon_class = models.CharField(max_length=100, help_text="Ex: fa-brands fa-instagram.")
    order = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['order']
        verbose_name = "Rede Social"
        verbose_name_plural = "Redes Sociais"