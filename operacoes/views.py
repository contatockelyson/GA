import csv

from django.conf import settings
from django.db.models import Count, Sum
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.crypto import constant_time_compare
from django.utils import timezone

from .forms import (
    AcaoReuniaoForm,
    EmpilhadeiraForm,
    EtiquetaForm,
    KaizenForm,
    LimpezaEmpilhadeiraForm,
    MovimentacaoForm,
    OperadorForm,
    PerdaForm,
    RegistroSegurancaForm,
    ReuniaoGAForm,
)
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


PERFIS = {
    'ckelyson': {
        'titulo': 'Dashboard Ckelyson',
        'nome': 'CKELYSON',
    },
    'diego': {
        'titulo': 'Dashboard Diego',
        'nome': 'DIEGO',
    },
}


MODULOS = {
    'operadores': {
        'titulo': 'Operadores',
        'singular': 'operador',
        'model': Operador,
        'form': OperadorForm,
        'campos': ['nome', 'matricula', 'turno', 'ativo'],
        'busca': ['nome', 'matricula', 'turno'],
    },
    'empilhadeiras': {
        'titulo': 'Empilhadeiras',
        'singular': 'empilhadeira',
        'model': Empilhadeira,
        'form': EmpilhadeiraForm,
        'campos': ['codigo', 'modelo', 'setor', 'ativa'],
        'busca': ['codigo', 'modelo', 'setor'],
    },
    'movimentacoes': {
        'titulo': 'Perdas de movimentacao',
        'singular': 'perda de movimentacao',
        'model': Movimentacao,
        'form': MovimentacaoForm,
        'campos': ['data_hora', 'operador', 'empilhadeira', 'tipo', 'tempo_minutos', 'custo_reais', 'motivo'],
        'busca': ['motivo', 'observacao', 'operador__nome', 'empilhadeira__codigo'],
        'data_field': 'data_hora',
        'choice_filter': 'tipo',
        'dashboard_filter': 'responsavel_dashboard',
    },
    'seguranca': {
        'titulo': 'Seguranca',
        'singular': 'ocorrencia de seguranca',
        'model': RegistroSeguranca,
        'form': RegistroSegurancaForm,
        'campos': ['data_hora', 'motivo', 'status', 'operador', 'empilhadeira'],
        'busca': ['motivo', 'acao_tomada', 'operador__nome', 'empilhadeira__codigo'],
        'data_field': 'data_hora',
        'choice_filter': 'status',
        'dashboard_filter': 'responsavel_dashboard',
    },
    'etiquetas': {
        'titulo': 'Etiquetas',
        'singular': 'etiqueta',
        'model': Etiqueta,
        'form': EtiquetaForm,
        'campos': ['numero', 'descricao', 'status', 'aberta_em', 'fechada_em', 'operador', 'responsavel'],
        'busca': ['numero', 'descricao', 'responsavel', 'operador__nome'],
        'data_field': 'aberta_em',
        'choice_filter': 'status',
        'dashboard_filter': 'responsavel_dashboard',
    },
    'limpezas': {
        'titulo': 'Limpezas',
        'singular': 'limpeza',
        'model': LimpezaEmpilhadeira,
        'form': LimpezaEmpilhadeiraForm,
        'campos': ['data', 'empilhadeira', 'responsavel', 'limpeza_externa', 'limpeza_interna'],
        'busca': ['empilhadeira__codigo', 'responsavel__nome', 'observacao'],
        'data_field': 'data',
        'dashboard_filter': 'responsavel_dashboard',
    },
    'perdas': {
        'titulo': 'Perdas',
        'singular': 'perda',
        'model': Perda,
        'form': PerdaForm,
        'campos': ['data', 'tipo', 'descricao', 'minutos', 'valor_reais'],
        'busca': ['descricao', 'acao_corretiva'],
        'data_field': 'data',
        'choice_filter': 'tipo',
        'dashboard_filter': 'responsavel_dashboard',
    },
    'kaizens': {
        'titulo': 'Kaizens',
        'singular': 'kaizen',
        'model': Kaizen,
        'form': KaizenForm,
        'campos': ['data', 'titulo', 'responsavel', 'status', 'ganho_estimado'],
        'busca': ['titulo', 'descricao', 'responsavel'],
        'data_field': 'data',
        'choice_filter': 'status',
        'dashboard_filter': 'responsavel_dashboard',
    },
    'reunioes': {
        'titulo': 'Reunioes de GA',
        'singular': 'reuniao',
        'model': ReuniaoGA,
        'form': ReuniaoGAForm,
        'campos': ['data', 'tema', 'participantes'],
        'busca': ['tema', 'participantes', 'pauta', 'decisoes'],
        'data_field': 'data',
        'dashboard_filter': 'responsavel_dashboard',
    },
    'acoes': {
        'titulo': 'Acoes de reuniao',
        'singular': 'acao',
        'model': AcaoReuniao,
        'form': AcaoReuniaoForm,
        'campos': ['reuniao_tema', 'descricao', 'responsavel', 'prazo', 'status'],
        'busca': ['descricao', 'responsavel', 'reuniao_tema'],
        'data_field': 'prazo',
        'choice_filter': 'status',
        'dashboard_filter': 'responsavel_dashboard',
    },
}


def dashboard(request):
    return dashboard_perfil(request, 'ckelyson')


def dashboard_perfil(request, perfil):
    perfil_config = PERFIS.get(perfil)
    if perfil_config is None:
        raise Http404('Dashboard nao encontrado.')

    hoje = timezone.localdate()
    movimentacoes = Movimentacao.objects.filter(responsavel_dashboard=perfil)
    movimentacoes_hoje = movimentacoes.filter(data_hora__date=hoje)
    etiquetas = Etiqueta.objects.filter(responsavel_dashboard=perfil)
    seguranca = RegistroSeguranca.objects.filter(responsavel_dashboard=perfil)
    limpezas = LimpezaEmpilhadeira.objects.filter(responsavel_dashboard=perfil)
    perdas = Perda.objects.filter(responsavel_dashboard=perfil)
    kaizens = Kaizen.objects.filter(responsavel_dashboard=perfil)
    reunioes = ReuniaoGA.objects.filter(responsavel_dashboard=perfil)
    acoes = AcaoReuniao.objects.filter(responsavel_dashboard=perfil)
    etiquetas_total = etiquetas.count()
    seguranca_total = seguranca.count()
    acoes_total = acoes.count()
    kaizens_total = kaizens.count()
    limpezas_total = limpezas.count()
    movimentacoes_total_custo = movimentacoes.aggregate(total=Sum('custo_reais'))['total'] or 0

    cards = [
        {
            'titulo': 'Perdas totais',
            'valor': perdas.aggregate(total=Sum('valor_reais'))['total'] or 0,
            'detalhe': f"{perdas.aggregate(total=Sum('minutos'))['total'] or 0} minutos",
        },
        {
            'titulo': 'Etiquetas abertas',
            'valor': etiquetas.filter(status='aberta').count(),
            'detalhe': f"{etiquetas.filter(status='fechada').count()} fechadas",
        },
        {
            'titulo': 'Seguranca geral',
            'valor': seguranca.count(),
            'detalhe': f"{seguranca.exclude(status='ok').count()} com atencao",
        },
        {
            'titulo': 'GA geral',
            'valor': reunioes.count(),
            'detalhe': f"{acoes.exclude(status='concluida').count()} acoes pendentes",
        },
        {
            'titulo': 'Kaizens',
            'valor': kaizens.count(),
            'detalhe': f"{kaizens.filter(status='sugestao').count()} sugestoes",
        },
    ]

    contexto = {
        'perfil_slug': perfil,
        'perfil_config': perfil_config,
        'perfis': PERFIS,
        'mostrar_cadastros': True,
        'cards': cards,
        'movimentacoes': movimentacoes.select_related('operador', 'empilhadeira')[:8],
        'etiquetas_abertas': etiquetas.filter(status='aberta'),
        'etiquetas_fechadas': etiquetas.filter(status='fechada'),
        'limpezas_recentes': limpezas.select_related('empilhadeira', 'responsavel')[:8],
        'perdas_recentes': perdas[:8],
        'perdas_total_minutos': perdas.aggregate(total=Sum('minutos'))['total'] or 0,
        'perdas_total_reais': perdas.aggregate(total=Sum('valor_reais'))['total'] or 0,
        'seguranca_geral': seguranca[:8],
        'kaizens_recentes': kaizens[:8],
        'kaizens_sugestoes': kaizens.filter(status='sugestao')[:8],
        'reunioes_recentes': reunioes[:5],
        'acoes_recentes': acoes[:8],
        'produtividade_por_tipo': movimentacoes.values('tipo').annotate(total=Sum('custo_reais'), registros=Count('id')).order_by('tipo'),
        'perdas_por_tipo': [
            {
                'tipo': item['tipo'].title(),
                'registros': item['registros'],
                'total': item['total'] or 0,
                'percentual': calcular_percentual(item['total'] or 0, movimentacoes_total_custo),
            }
            for item in movimentacoes.values('tipo').annotate(total=Sum('custo_reais'), registros=Count('id')).order_by('tipo')
        ],
        'percentuais': {
            'etiquetas_abertas': calcular_percentual(etiquetas.filter(status='aberta').count(), etiquetas_total),
            'etiquetas_fechadas': calcular_percentual(etiquetas.filter(status='fechada').count(), etiquetas_total),
            'seguranca_ok': calcular_percentual(seguranca.filter(status='ok').count(), seguranca_total),
            'seguranca_atencao': calcular_percentual(seguranca.exclude(status='ok').count(), seguranca_total),
            'acoes_concluidas': calcular_percentual(acoes.filter(status='concluida').count(), acoes_total),
            'acoes_pendentes': calcular_percentual(acoes.exclude(status='concluida').count(), acoes_total),
            'kaizens_sugestao': calcular_percentual(kaizens.filter(status='sugestao').count(), kaizens_total),
            'kaizens_implantados': calcular_percentual(kaizens.filter(status='implantado').count(), kaizens_total),
            'limpeza_interna': calcular_percentual(limpezas.filter(limpeza_interna=True).count(), limpezas_total),
            'limpeza_externa': calcular_percentual(limpezas.filter(limpeza_externa=True).count(), limpezas_total),
        },
    }
    contexto['modulos'] = MODULOS
    contexto['dashboard_modulos'] = get_dashboard_modulos()
    return render(request, 'operacoes/dashboard.html', contexto)


def calcular_percentual(parte, total):
    if not total:
        return 0
    return round((float(parte) / float(total)) * 100, 1)


def lista_modulo(request, modulo, perfil=None):
    config = get_object_or_404_config(modulo)
    validar_perfil(perfil)
    objetos = filtrar_queryset(config, request.GET, perfil)
    choice_options = get_choice_options(config)
    return render(request, 'operacoes/lista.html', {
        'perfil_slug': perfil,
        'modulo': modulo,
        'config': config,
        'objetos': objetos,
        'filtros': request.GET,
        'choice_options': choice_options,
        'perfis': PERFIS,
    })


def exportar_modulo(request, modulo, perfil=None):
    config = get_object_or_404_config(modulo)
    validar_perfil(perfil)
    objetos = filtrar_queryset(config, request.GET, perfil)
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = f'attachment; filename="{modulo}.csv"'
    response.write('\ufeff')

    writer = csv.writer(response, delimiter=';')
    writer.writerow([formatar_cabecalho(campo) for campo in config['campos']])
    for objeto in objetos:
        writer.writerow([formatar_valor(objeto, campo) for campo in config['campos']])
    return response


def criar_registro(request, modulo, perfil=None):
    config = get_object_or_404_config(modulo)
    validar_perfil(perfil)
    form_class = config['form']
    form = form_class(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        objeto = form.save(commit=False)
        aplicar_perfil(objeto, config, perfil)
        objeto.save()
        return redirect_lista(modulo, perfil)
    return render(request, 'operacoes/formulario.html', {
        'perfil_slug': perfil,
        'modulo': modulo,
        'config': config,
        'form': form,
        'acao': 'Novo',
    })


def editar_registro(request, modulo, pk, perfil=None):
    config = get_object_or_404_config(modulo)
    validar_perfil(perfil)
    objeto = get_object_or_404(filtrar_queryset(config, {}, perfil), pk=pk)
    form_class = config['form']
    form = form_class(request.POST or None, request.FILES or None, instance=objeto)
    if request.method == 'POST' and form.is_valid():
        objeto = form.save(commit=False)
        aplicar_perfil(objeto, config, perfil)
        objeto.save()
        return redirect_lista(modulo, perfil)
    return render(request, 'operacoes/formulario.html', {
        'perfil_slug': perfil,
        'modulo': modulo,
        'config': config,
        'form': form,
        'objeto': objeto,
        'acao': 'Editar',
    })


def excluir_registro(request, modulo, pk, perfil=None):
    config = get_object_or_404_config(modulo)
    validar_perfil(perfil)
    objeto = get_object_or_404(filtrar_queryset(config, {}, perfil), pk=pk)
    erro_senha = ''
    if request.method == 'POST':
        senha = request.POST.get('senha_exclusao', '')
        if senha_exclusao_valida(senha):
            objeto.delete()
            return redirect_lista(modulo, perfil)
        erro_senha = 'Senha incorreta. O registro nao foi excluido.'
    return render(request, 'operacoes/confirmar_exclusao.html', {
        'perfil_slug': perfil,
        'modulo': modulo,
        'config': config,
        'objeto': objeto,
        'erro_senha': erro_senha,
    })


def get_object_or_404_config(modulo):
    config = MODULOS.get(modulo)
    if config is None:
        raise Http404('Modulo nao encontrado.')
    return config


def get_dashboard_modulos():
    ocultos = {'operadores', 'empilhadeiras'}
    return {slug: config for slug, config in MODULOS.items() if slug not in ocultos}


def filtrar_queryset(config, params, perfil=None):
    queryset = config['model'].objects.all()

    if perfil and config.get('dashboard_filter'):
        queryset = queryset.filter(**{config['dashboard_filter']: perfil})

    busca = params.get('q', '').strip()
    if busca and config.get('busca'):
        condicao = Q()
        for campo in config['busca']:
            condicao |= Q(**{f'{campo}__icontains': busca})
        queryset = queryset.filter(condicao)

    escolha = params.get('tipo_status', '').strip()
    if escolha and config.get('choice_filter'):
        queryset = queryset.filter(**{config['choice_filter']: escolha})

    params_perfil = params.get('perfil', '').strip()
    if not perfil and params_perfil and config.get('dashboard_filter'):
        queryset = queryset.filter(**{config['dashboard_filter']: params_perfil})

    data_field = config.get('data_field')
    data_inicio = params.get('data_inicio', '').strip()
    data_fim = params.get('data_fim', '').strip()
    if data_field and data_inicio:
        filtro = f'{data_field}__date__gte' if data_field.endswith('_hora') else f'{data_field}__gte'
        queryset = queryset.filter(**{filtro: data_inicio})
    if data_field and data_fim:
        filtro = f'{data_field}__date__lte' if data_field.endswith('_hora') else f'{data_field}__lte'
        queryset = queryset.filter(**{filtro: data_fim})

    return queryset


def validar_perfil(perfil):
    if perfil is not None and perfil not in PERFIS:
        raise Http404('Dashboard nao encontrado.')


def aplicar_perfil(objeto, config, perfil):
    if perfil and config.get('dashboard_filter'):
        setattr(objeto, config['dashboard_filter'], perfil)


def senha_exclusao_valida(senha):
    senha_configurada = getattr(settings, 'SENHA_EXCLUSAO', '')
    return bool(senha_configurada) and constant_time_compare(senha, senha_configurada)


def redirect_lista(modulo, perfil):
    if perfil:
        return redirect('operacoes:lista_modulo_perfil', perfil=perfil, modulo=modulo)
    return redirect('operacoes:lista_modulo', modulo=modulo)


def get_choice_options(config):
    campo = config.get('choice_filter')
    if not campo:
        return []
    model_field = config['model']._meta.get_field(campo)
    return model_field.choices


def formatar_cabecalho(campo):
    return campo.replace('_', ' ').title()


def formatar_valor(objeto, campo):
    display = getattr(objeto, f'get_{campo}_display', None)
    if callable(display):
        return display()
    valor = getattr(objeto, campo, '')
    if callable(valor):
        valor = valor()
    return str(valor) if valor is not None else ''
