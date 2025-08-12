# contacts/models.py

from django.db import models

class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Nova'),
        ('READ', 'Lida'),
        ('REPLIED', 'Respondida'),
    ]

    full_name = models.CharField(max_length=255, verbose_name="Nome Completo")
    email = models.EmailField(verbose_name="E-mail")
    # CORREÇÃO: O campo 'phone' agora é obrigatório (blank=False por padrão)
    phone = models.CharField(max_length=20, verbose_name="Telefone")
    subject = models.CharField(max_length=100, verbose_name="Assunto")
    message = models.TextField(verbose_name="Mensagem")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW', verbose_name="Status")
    received_at = models.DateTimeField(auto_now_add=True, verbose_name="Recebida em")

    def __str__(self):
        return f"Mensagem de {self.full_name} sobre '{self.subject}'"

    class Meta:
        ordering = ['-received_at']
        verbose_name = "Mensagem de Contato"
        verbose_name_plural = "Mensagens de Contato"