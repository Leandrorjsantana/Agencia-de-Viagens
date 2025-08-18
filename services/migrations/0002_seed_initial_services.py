# services/migrations/0002_seed_initial_services.py

from django.db import migrations
from django.utils.text import slugify

# Lista dos serviços que queremos criar
INITIAL_SERVICES = [
    "Passagens Aéreas",
    "Ofertas",
    "Pacotes",
    "Disney",
    "Cruzeiros",
    "Transfer",
]

def create_initial_services(apps, schema_editor):
    """
    Esta função será executada quando aplicarmos a migração.
    """
    # Pegamos a versão histórica do modelo 'Service' para esta migração
    Service = apps.get_model('services', 'Service')
    
    for index, name in enumerate(INITIAL_SERVICES):
        # slugify transforma "Passagens Aéreas" em "passagens-aereas"
        slug = slugify(name)
        
        # O 'get_or_create' é seguro: ele só cria se o serviço não existir
        Service.objects.get_or_create(
            name=name,
            defaults={
                'slug': slug,
                'order': index, # Define uma ordem inicial
                'is_active': True
            }
        )

class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'), # Depende da migração que criou a tabela
    ]

    operations = [
        # Diz ao Django para executar nossa função
        migrations.RunPython(create_initial_services),
    ]