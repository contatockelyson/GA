from django.db import models
from django.utils import timezone


DASHBOARD_CHOICES = [
    ('ckelyson', 'CKELYSON'),
    ('diego', 'DIEGO'),
]


class Operador(models.Model):
    nome = models.CharField(max_length=120)
    matricula = models.CharField(max_length=30, unique=True)
    turno = models.CharField(max_length=30, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'operador'
        verbose_name_plural = 'operadores'

    def __str__(self):
        return f'{self.nome} ({self.matricula})'


class Empilhadeira(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    modelo = models.CharField(max_length=80, blank=True)
    setor = models.CharField(max_length=80, blank=True)
    ativa = models.BooleanField(default=True)

    class Meta:
        ordering = ['codigo']
        verbose_name = 'empilhadeira'
        verbose_name_plural = 'empilhadeiras'

    def __str__(self):
        return self.codigo


class Movimentacao(models.Model):
    TIPO_CHOICES = [
        ('tempo', 'Tempo'),
        ('custo', 'Custo em reais'),
        ('avaria', 'Avaria'),
        ('retrabalho', 'Retrabalho'),
        ('outro', 'Outro'),
    ]

    data_hora = models.DateTimeField(default=timezone.now)
    responsavel_dashboard = models.CharField(max_length=20, choices=DASHBOARD_CHOICES, default='ckelyson')
    operador = models.ForeignKey(Operador, on_delete=models.PROTECT, null=True)
    empilhadeira = models.ForeignKey(Empilhadeira, on_delete=models.PROTECT, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='tipo de perda')
    tempo_minutos = models.PositiveIntegerField(default=0)
    custo_reais = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    motivo = models.CharField(max_length=180, default='Nao informado')
    observacao = models.TextField(blank=True)

    class Meta:
        ordering = ['-data_hora']
        verbose_name = 'perda de movimentacao'
        verbose_name_plural = 'perdas de movimentacao'

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.motivo} - {self.data_hora:%d/%m/%Y %H:%M}'


class RegistroSeguranca(models.Model):
    STATUS_CHOICES = [
        ('ok', 'OK'),
        ('atencao', 'Atencao'),
        ('critico', 'Critico'),
    ]

    data_hora = models.DateTimeField(default=timezone.now)
    responsavel_dashboard = models.CharField(max_length=20, choices=DASHBOARD_CHOICES, default='ckelyson')
    operador = models.ForeignKey(Operador, on_delete=models.PROTECT, null=True, blank=True)
    empilhadeira = models.ForeignKey(Empilhadeira, on_delete=models.PROTECT, null=True, blank=True)
    motivo = models.CharField(max_length=180, default='Nao informado')
    foto = models.FileField(upload_to='seguranca/', blank=True)
    item_verificado = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ok')
    acao_tomada = models.TextField(blank=True)

    class Meta:
        ordering = ['-data_hora']
        verbose_name = 'ocorrencia de seguranca'
        verbose_name_plural = 'ocorrencias de seguranca'

    def __str__(self):
        return f'{self.motivo} - {self.get_status_display()}'


class Etiqueta(models.Model):
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('fechada', 'Fechada'),
        ('cancelada', 'Cancelada'),
    ]

    numero = models.CharField(max_length=40, unique=True)
    responsavel_dashboard = models.CharField(max_length=20, choices=DASHBOARD_CHOICES, default='ckelyson')
    descricao = models.CharField(max_length=180)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='aberta')
    aberta_em = models.DateField(default=timezone.localdate)
    fechada_em = models.DateField(null=True, blank=True)
    operador = models.ForeignKey(Operador, on_delete=models.PROTECT, null=True, blank=True)
    responsavel = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ['status', '-aberta_em']
        verbose_name = 'etiqueta'
        verbose_name_plural = 'etiquetas'

    def __str__(self):
        return f'{self.numero} - {self.get_status_display()}'


class LimpezaEmpilhadeira(models.Model):
    data = models.DateField(default=timezone.localdate)
    responsavel_dashboard = models.CharField(max_length=20, choices=DASHBOARD_CHOICES, default='ckelyson')
    empilhadeira = models.ForeignKey(Empilhadeira, on_delete=models.PROTECT, null=True)
    responsavel = models.ForeignKey(Operador, on_delete=models.PROTECT, null=True)
    limpeza_externa = models.BooleanField(default=False)
    limpeza_interna = models.BooleanField(default=False)
    observacao = models.TextField(blank=True)

    class Meta:
        ordering = ['-data']
        verbose_name = 'limpeza de empilhadeira'
        verbose_name_plural = 'limpezas de empilhadeiras'

    def __str__(self):
        return f'{self.empilhadeira} - {self.data:%d/%m/%Y}'


class Perda(models.Model):
    TIPO_CHOICES = [
        ('minutos', 'Minutos'),
        ('reais', 'R$'),
    ]

    data = models.DateField(default=timezone.localdate)
    responsavel_dashboard = models.CharField(max_length=20, choices=DASHBOARD_CHOICES, default='ckelyson')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descricao = models.CharField(max_length=180)
    minutos = models.PositiveIntegerField(default=0)
    valor_reais = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    acao_corretiva = models.TextField(blank=True)

    class Meta:
        ordering = ['-data']
        verbose_name = 'perda'
        verbose_name_plural = 'perdas'

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.descricao}'


class Kaizen(models.Model):
    STATUS_CHOICES = [
        ('sugestao', 'Sugestao'),
        ('andamento', 'Em andamento'),
        ('implantado', 'Implantado'),
        ('cancelado', 'Cancelado'),
    ]

    data = models.DateField(default=timezone.localdate)
    responsavel_dashboard = models.CharField(max_length=20, choices=DASHBOARD_CHOICES, default='ckelyson')
    titulo = models.CharField(max_length=140)
    descricao = models.TextField()
    responsavel = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sugestao')
    ganho_estimado = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-data']
        verbose_name = 'kaizen'
        verbose_name_plural = 'kaizens'

    def __str__(self):
        return f'{self.titulo} - {self.get_status_display()}'


class ReuniaoGA(models.Model):
    data = models.DateField(default=timezone.localdate)
    responsavel_dashboard = models.CharField(max_length=20, choices=DASHBOARD_CHOICES, default='ckelyson')
    tema = models.CharField(max_length=140)
    participantes = models.TextField(blank=True)
    pauta = models.TextField(blank=True)
    decisoes = models.TextField(blank=True)

    class Meta:
        ordering = ['-data']
        verbose_name = 'reuniao de GA'
        verbose_name_plural = 'reunioes de GA'

    def __str__(self):
        return f'{self.tema} - {self.data:%d/%m/%Y}'


class AcaoReuniao(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('andamento', 'Em andamento'),
        ('concluida', 'Concluida'),
        ('atrasada', 'Atrasada'),
    ]

    responsavel_dashboard = models.CharField(max_length=20, choices=DASHBOARD_CHOICES, default='ckelyson')
    reuniao_tema = models.CharField(max_length=140, blank=True)
    descricao = models.CharField(max_length=180)
    responsavel = models.CharField(max_length=120)
    prazo = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    class Meta:
        ordering = ['prazo']
        verbose_name = 'acao de reuniao'
        verbose_name_plural = 'acoes de reuniao'

    def __str__(self):
        return f'{self.descricao} - {self.get_status_display()}'
