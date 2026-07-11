from django import forms

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


class DateInput(forms.DateInput):
    input_type = 'date'


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class OperadorForm(BaseModelForm):
    class Meta:
        model = Operador
        fields = ['nome', 'matricula', 'turno', 'ativo']


class EmpilhadeiraForm(BaseModelForm):
    class Meta:
        model = Empilhadeira
        fields = ['codigo', 'modelo', 'setor', 'ativa']


class MovimentacaoForm(BaseModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['operador'].required = True
        self.fields['empilhadeira'].required = True

    class Meta:
        model = Movimentacao
        fields = ['data_hora', 'operador', 'empilhadeira', 'tipo', 'tempo_minutos', 'custo_reais', 'motivo', 'observacao']
        widgets = {'data_hora': DateTimeInput(format='%Y-%m-%dT%H:%M')}


class RegistroSegurancaForm(BaseModelForm):
    class Meta:
        model = RegistroSeguranca
        fields = ['data_hora', 'operador', 'empilhadeira', 'motivo', 'foto', 'status', 'acao_tomada']
        widgets = {'data_hora': DateTimeInput(format='%Y-%m-%dT%H:%M')}


class EtiquetaForm(BaseModelForm):
    class Meta:
        model = Etiqueta
        fields = ['numero', 'descricao', 'status', 'aberta_em', 'fechada_em', 'operador', 'responsavel']
        widgets = {'aberta_em': DateInput(), 'fechada_em': DateInput()}


class LimpezaEmpilhadeiraForm(BaseModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['empilhadeira'].required = True
        self.fields['responsavel'].required = True

    class Meta:
        model = LimpezaEmpilhadeira
        fields = ['data', 'empilhadeira', 'responsavel', 'limpeza_externa', 'limpeza_interna', 'observacao']
        widgets = {'data': DateInput()}


class PerdaForm(BaseModelForm):
    class Meta:
        model = Perda
        fields = ['data', 'tipo', 'descricao', 'minutos', 'valor_reais', 'acao_corretiva']
        widgets = {'data': DateInput()}


class KaizenForm(BaseModelForm):
    class Meta:
        model = Kaizen
        fields = ['data', 'titulo', 'descricao', 'responsavel', 'status', 'ganho_estimado']
        widgets = {'data': DateInput()}


class ReuniaoGAForm(BaseModelForm):
    class Meta:
        model = ReuniaoGA
        fields = ['data', 'tema', 'participantes', 'pauta', 'decisoes']
        widgets = {'data': DateInput()}


class AcaoReuniaoForm(BaseModelForm):
    class Meta:
        model = AcaoReuniao
        fields = ['reuniao_tema', 'descricao', 'responsavel', 'prazo', 'status']
        widgets = {'prazo': DateInput()}
