from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .models import Item, Categoria
from rest_framework import viewsets
from .serializers import ItemSerializer
from django.http import HttpResponseRedirect
# Create your views here.

def index(request):
    return render(request, "cardapio/index.html",{
        "item": Item.objects.all()
    })

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "cardapio/login.html", {
                "message": "Senha e/ou usuário inválido(s)!"
            })
    return render(request, "cardapio/login.html")

def logout_view(request):
    logout(request)
    return render(request,"cardapio/login.html",{
        "message": "Desconectado!"
    })

def itemadd(request):
    if request.method == "POST":
        nome = request.POST ["nome"]
        descricao = request.POST ["descricao"]
        preco = request.POST [ "preco" ] 
        imagem = request.POST.get ("imagem", "")
        categoria_id = request.POST["categoria"]

        Item.objects.create(
            nome=nome,
            descricao=descricao,
            preco=preco,
            imagem=imagem,
            categoria_id=categoria_id
        )
        return HttpResponseRedirect(reverse("index"))
    categorias = Categoria.objects.all()
    return render(request, "cardapio/additem.html", {
        "categorias": categorias
    })

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()  # Busca todos os itens do banco
    serializer_class = ItemSerializer  # Usa o serializer para converter
 
def item_page(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    categorias = Categoria.objects.all()

    return render(request, "cardapio/itempage.html",{
        "item": item,
        "categorias": categorias
    })

def itemmod(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    
    if request.method == "POST":
        item.nome = request.POST["nome"]
        item.descricao = request.POST["descricao"]
        item.preco = request.POST["preco"]
        item.imagem = request.POST.get("imagem", "")
        item.categoria_id = request.POST["categoria"]
        item.save()
        
        return HttpResponseRedirect(reverse("itempage", args=[item_id]))
    
    categorias = Categoria.objects.all()
    return render(request, "cardapio/itempage.html", {
        "item": item,
        "categorias": categorias
    })

def itemdel(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item.delete()
    return HttpResponseRedirect(reverse("index"))