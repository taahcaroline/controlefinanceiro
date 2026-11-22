from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# =================================
# CATEGORIAS
# =================================

class Categoria(models.Model):

    TIPOS = [
        ('R', 'Receita'),
        ('D', 'Despesa'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categorias'
    )

    nome = models.CharField(max_length=50)

    tipo = models.CharField(
        max_length=1,
        choices=TIPOS
    )

    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'nome', 'tipo'],
                name='categoria_unica_usuario'
            )
        ]

    def __str__(self):
        return self.nome


# =================================
# MOVIMENTAÇÕES
# =================================

class Movimentacao(models.Model):

    TIPOS = [
        ('R', 'Receita'),
        ('D', 'Despesa'),
    ]

    FORMAS_PAGAMENTO = [
        ('DINHEIRO', 'Dinheiro'),
        ('PIX', 'Pix'),
        ('DEBITO', 'Débito'),
        ('CREDITO', 'Crédito'),
        ('BOLETO', 'Boleto'),
        ('OUTRO', 'Outro'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='movimentacoes'
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='movimentacoes'
    )

    descricao = models.CharField(max_length=150)

    tipo = models.CharField(
        max_length=1,
        choices=TIPOS
    )

    valor = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    data = models.DateField(default=timezone.localdate)

    forma_pagamento = models.CharField(
        max_length=20,
        choices=FORMAS_PAGAMENTO,
        blank=True
    )

    observacao = models.TextField(blank=True)

    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data', '-criada_em']

    def __str__(self):
        return f'{self.descricao} - R$ {self.valor}'


# =================================
# ORÇAMENTO MENSAL
# =================================

class Budget(models.Model):

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orcamentos'
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='orcamentos'
    )

    mes = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )

    ano = models.PositiveSmallIntegerField()

    limite = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'categoria', 'mes', 'ano'],
                name='orcamento_unico_categoria_periodo'
            )
        ]

    def __str__(self):
        return f'{self.categoria.nome} - {self.mes}/{self.ano}'


# =================================
# MOVIMENTAÇÕES RECORRENTES
# =================================

class RecurringTransaction(models.Model):

    FREQUENCIAS = [
        ('S', 'Semanal'),
        ('M', 'Mensal'),
        ('A', 'Anual'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recorrencias'
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='recorrencias'
    )

    descricao = models.CharField(max_length=150)

    tipo = models.CharField(
        max_length=1,
        choices=Movimentacao.TIPOS
    )

    valor = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    frequencia = models.CharField(
        max_length=1,
        choices=FREQUENCIAS
    )

    data_inicio = models.DateField()

    proxima_data = models.DateField()

    data_fim = models.DateField(
        null=True,
        blank=True
    )

    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.descricao


# =================================
# NOTIFICAÇÕES
# =================================

class Notification(models.Model):

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notificacoes'
    )

    titulo = models.CharField(max_length=150)

    mensagem = models.TextField()

    lida = models.BooleanField(default=False)

    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criada_em']

    def __str__(self):
        return self.titulo


# =================================
# ANEXOS (OPCIONAL)
# =================================

class Attachment(models.Model):

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='anexos'
    )

    movimentacao = models.ForeignKey(
        Movimentacao,
        on_delete=models.CASCADE,
        related_name='anexos'
    )

    arquivo = models.FileField(
        upload_to='comprovantes/%Y/%m/'
    )

    descricao = models.CharField(
        max_length=150,
        blank=True
    )

    enviado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descricao or self.arquivo.name
