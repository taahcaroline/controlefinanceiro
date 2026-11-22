from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('cadastro/', views.cadastro_usuario, name='cadastro'),
    path('cadastrar_receita/', views.cadastrar_receita, name='cadastrar_receita'),
    path('receitas/', views.receitas, name='receitas'),
    path('receitas/<int:receita_id>/editar/', views.editar_receita, name='editar_receita'),
    path('receitas/<int:receita_id>/excluir/', views.excluir_receita, name='excluir_receita'),
    path('cadastrar_despesa/', views.cadastrar_despesa, name='cadastrar_despesa'),
    path('despesas/<int:despesa_id>/editar/', views.editar_despesa, name='editar_despesa'),
    path('despesas/<int:despesa_id>/excluir/', views.excluir_despesa, name='excluir_despesa'),
    path('despesas/', views.despesas, name='despesas'),
    path('cadastrar_categoria/', views.cadastrar_categoria, name='cadastrar_categoria'),
    path('categorias/', views.categorias, name='categorias'),
    path('categorias/<int:categoria_id>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:categoria_id>/excluir/', views.excluir_categoria, name='excluir_categoria'),
    ]