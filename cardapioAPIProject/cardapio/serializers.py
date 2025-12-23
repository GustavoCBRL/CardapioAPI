from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    class Meta:
        model = Item
        fields = ['id', 'nome', 'descricao', 'preco', 'imagem', 'categoria_nome']  # Exibe também o nome da categoria