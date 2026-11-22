from pyexpat.errors import messages

from django.shortcuts import get_object_or_404, render, redirect

from controlefinanceiro.models import Categoria, Movimentacao
from .forms import CategoriaForm, ReceitaForm, CadastroUsuarioForm, LoginForm, DespesaForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages




def cadastro_usuario(request):

    if request.method == 'POST':

        form = CadastroUsuarioForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Conta criada com sucesso!'
            )

            return redirect('login')

    else:
        form = CadastroUsuarioForm()

    return render(
        request,
        'registration/cadastro.html',
        {'form': form}
    )

def login_usuario(request):

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            usuario = authenticate(
                request,
                username=username,
                password=password
            )

            if usuario is not None:

                login(request, usuario)

                return redirect('receitas')

            else:
                messages.error(
                    request,
                    'Usuário ou senha incorretos!'
                )

    else:
        form = LoginForm()

    return render(
        request,
        'registration/login.html',
        {'form': form}
    )
def logout_usuario(request):

    logout(request)

    return redirect('login')
# Create your views here.
def home(request):
    return render(request, 'index.html')

def cadastrar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.usuario = request.user
            categoria.save()
            return redirect('cadastrar_categoria')
    else:
        form = CategoriaForm()
    return render(request, 'cadastrar_categoria.html', {'form': form})

@login_required
def cadastrar_receita(request):

    if request.method == 'POST':

        form = ReceitaForm(
            request.POST,
            usuario=request.user
        )

        if form.is_valid():

            receita = form.save(commit=False)

            receita.usuario = request.user
            receita.tipo = 'R'

            receita.save()

            return redirect('cadastrar_receita')

    else:

        form = ReceitaForm(usuario=request.user)

    return render(
        request,
        'cadastrar_receitas.html',
        {'form': form}
    )
@login_required
def receitas(request):

    receitas = Movimentacao.objects.filter(
        usuario=request.user,
        tipo='R'
    )

    return render(
        request,
        'receitas.html',
        {'receitas': receitas}
    )


@login_required
def despesas(request):

    despesas = Movimentacao.objects.filter(
        usuario=request.user,
        tipo='D'
    )

    return render(
        request,
        'despesas.html',
        {'despesas': despesas}
    )

@login_required
def editar_receita(request, receita_id):
    receita = get_object_or_404(Movimentacao, id=receita_id)
    if request.method == "POST":
        form = ReceitaForm(request.POST, instance=receita)
        if form.is_valid():
            form.save()
            messages.success(request, "Item atualizado com sucesso!")
            return redirect('receitas')
    else:
        form = ReceitaForm(instance=receita)
    return render(request, 'editar_receita.html', {'form': form, 'receita': receita})


@login_required
def excluir_receita(request, receita_id):

    receita = get_object_or_404(
        Movimentacao,
        id=receita_id,
        usuario=request.user,
        tipo='R'
    )

    if request.method == 'POST':

        receita.delete()

        messages.success(
            request,
            'Receita excluída com sucesso!'
        )

        return redirect('receitas')

    return render(
        request,
        'excluir_receita.html',
        {'receita': receita}
    )


@login_required
def cadastrar_despesa(request):

    if request.method == 'POST':

        form = DespesaForm(
            request.POST,
            usuario=request.user
        )

        if form.is_valid():

            despesa = form.save(commit=False)

            despesa.usuario = request.user
            despesa.tipo = 'D'

            despesa.save()

            return redirect('cadastrar_despesa')

    else:

        form = DespesaForm(usuario=request.user)

    return render(
        request,
        'cadastrar_despesa.html',
        {'form': form}
    )


@login_required
def editar_despesa(request, despesa_id):
    despesa = get_object_or_404(Movimentacao, id=despesa_id)
    if request.method == "POST":
        form = DespesaForm(request.POST, instance=despesa)
        if form.is_valid():
            form.save()
            messages.success(request, "Item atualizado com sucesso!")
            return redirect('despesas')
    else:
        form = DespesaForm(instance=despesa)
    return render(request, 'editar_despesa.html', {'form': form, 'despesa': despesa})


@login_required
def excluir_despesa(request, despesa_id):

    despesa = get_object_or_404(
        Movimentacao,
        id=despesa_id,
        usuario=request.user,
        tipo='D'
    )

    if request.method == 'POST':

        despesa.delete()

        messages.success(
            request,
            'Receita excluída com sucesso!'
        )

        return redirect('receitas')

    return render(
        request,
        'excluir_despesa.html',
        {'despesa': despesa}
    )


@login_required
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Item atualizado com sucesso!")
            return redirect('categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'editar_categoria.html', {'form': form, 'categoria': categoria})


@login_required
def excluir_categoria(request, categoria_id):

    categoria = get_object_or_404(
        Categoria,
        id=categoria_id,
        usuario=request.user
    )

    if request.method == 'POST':

        categoria.delete()

        messages.success(
            request,
            'Categoria excluída com sucesso!'
        )

        return redirect('categorias')

    return render(
        request,
        'excluir_categoria.html',
        {'categoria': categoria}
    )

@login_required
def categorias(request):
    categorias = Categoria.objects.filter(
        usuario=request.user
    )

    return render(
        request,
        'categorias.html',
        {'categorias': categorias}
    )

    