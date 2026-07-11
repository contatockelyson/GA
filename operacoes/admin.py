from django.contrib import admin

from .models import (
    AcaoReuniao,
    Empilhadeira,
    Etiqueta,
    Kaizen,
    LimpezaEmpilhadeira,
    Movimentacao,
    Operador,
    Perda,
    RegistroSeguranca,
    ReuniaoGA,
)


@admin.register(Operador)
class OperadorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'turno', 'ativo')
    list_filter = ('ativo', 'turno')
    search_fields = ('nome', 'matricula')


@admin.register(Empilhadeira)
class EmpilhadeiraAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'modelo', 'setor', 'ativa')
    list_filter = ('ativa', 'setor')
    search_fields = ('codigo', 'modelo', 'setor')


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('data_hora', 'responsavel_dashboard', 'operador', 'empilhadeira', 'tipo', 'tempo_minutos', 'custo_reais', 'motivo')
    list_filter = ('responsavel_dashboard', 'tipo', 'empilhadeira', 'data_hora')
    search_fields = ('operador__nome', 'empilhadeira__codigo', 'motivo', 'observacao')
    date_hierarchy = 'data_hora'


@admin.register(RegistroSeguranca)
class RegistroSegurancaAdmin(admin.ModelAdmin):
    list_display = ('data_hora', 'responsavel_dashboard', 'motivo', 'status', 'operador', 'empilhadeira')
    list_filter = ('responsavel_dashboard', 'status', 'empilhadeira', 'data_hora')
    search_fields = ('motivo', 'acao_tomada', 'operador__nome', 'empilhadeira__codigo')
    date_hierarchy = 'data_hora'


@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'responsavel_dashboard', 'descricao', 'status', 'aberta_em', 'fechada_em', 'operador', 'responsavel')
    list_filter = ('responsavel_dashboard', 'status', 'aberta_em')
    search_fields = ('numero', 'descricao', 'responsavel')
    date_hierarchy = 'aberta_em'


@admin.register(LimpezaEmpilhadeira)
class LimpezaEmpilhadeiraAdmin(admin.ModelAdmin):
    list_display = ('data', 'responsavel_dashboard', 'empilhadeira', 'responsavel', 'limpeza_externa', 'limpeza_interna')
    list_filter = ('responsavel_dashboard', 'data', 'empilhadeira', 'limpeza_externa', 'limpeza_interna')
    search_fields = ('empilhadeira__codigo', 'responsavel__nome')
    date_hierarchy = 'data'


@admin.register(Perda)
class PerdaAdmin(admin.ModelAdmin):
    list_display = ('data', 'responsavel_dashboard', 'tipo', 'descricao', 'minutos', 'valor_reais')
    list_filter = ('responsavel_dashboard', 'tipo', 'data')
    search_fields = ('descricao', 'acao_corretiva')
    date_hierarchy = 'data'


@admin.register(Kaizen)
class KaizenAdmin(admin.ModelAdmin):
    list_display = ('data', 'responsavel_dashboard', 'titulo', 'responsavel', 'status', 'ganho_estimado')
    list_filter = ('responsavel_dashboard', 'status', 'data')
    search_fields = ('titulo', 'descricao', 'responsavel')
    date_hierarchy = 'data'


@admin.register(ReuniaoGA)
class ReuniaoGAAdmin(admin.ModelAdmin):
    list_display = ('data', 'responsavel_dashboard', 'tema')
    list_filter = ('responsavel_dashboard', 'data')
    search_fields = ('tema', 'participantes', 'pauta', 'decisoes')
    date_hierarchy = 'data'


@admin.register(AcaoReuniao)
class AcaoReuniaoAdmin(admin.ModelAdmin):
    list_display = ('responsavel_dashboard', 'reuniao_tema', 'descricao', 'responsavel', 'prazo', 'status')
    list_filter = ('responsavel_dashboard', 'status', 'prazo')
    search_fields = ('reuniao_tema', 'descricao', 'responsavel')
