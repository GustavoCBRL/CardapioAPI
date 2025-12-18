from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Categoria(models.Model):
    nome = models.CharField(max_length=64)
    descricao = models.CharField(max_length=300)
    def __str__(self):
        return f"{self.nome}"

class Item(models.Model):
    nome = models.CharField(max_length=64)
    descricao = models.CharField(max_length=300)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="item", default=1)
    imagem = models.URLField(blank=True)
    def __str__(self):
        return f"{self.nome}" 