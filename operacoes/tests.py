from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Empilhadeira, Kaizen, Movimentacao, Operador


class DashboardTests(TestCase):
    def test_dashboard_carrega_com_sucesso(self):
        response = self.client.get(reverse('operacoes:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard Ckelyson')
        self.assertContains(response, 'Sugestoes de kaizen e kaizens')
        self.assertContains(response, '/modulos/operadores/')
        self.assertContains(response, '/modulos/empilhadeiras/')
        self.assertNotContains(response, '/dash/ckelyson/modulos/operadores/')
        self.assertNotContains(response, '/dash/ckelyson/modulos/empilhadeiras/')
        self.assertNotContains(response, 'operadores ativos')
        self.assertNotContains(response, 'empilhadeiras ativas')

    def test_dashboard_diego_mostra_cadastros(self):
        response = self.client.get(reverse('operacoes:dashboard_perfil', args=['diego']))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard Diego')
        self.assertContains(response, '/modulos/operadores/')
        self.assertContains(response, '/modulos/empilhadeiras/')
        self.assertNotContains(response, '/dash/diego/modulos/operadores/')
        self.assertNotContains(response, '/dash/diego/modulos/empilhadeiras/')

    def test_dashboard_diego_nao_mostra_dados_do_ckelyson(self):
        operador = Operador.objects.create(nome='Carlos Silva', matricula='001', turno='A')
        empilhadeira = Empilhadeira.objects.create(codigo='EMP-01', modelo='GLP')
        Movimentacao.objects.create(
            data_hora=timezone.now(),
            responsavel_dashboard='ckelyson',
            operador=operador,
            empilhadeira=empilhadeira,
            tipo='tempo',
            tempo_minutos=35,
            custo_reais=120,
            motivo='Perda exclusiva CKELYSON',
        )

        response = self.client.get(reverse('operacoes:dashboard_perfil', args=['diego']))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Perda exclusiva CKELYSON')

    def test_dashboard_mostra_kaizen_do_perfil(self):
        Kaizen.objects.create(
            responsavel_dashboard='ckelyson',
            titulo='Reduzir espera na doca',
            descricao='Melhorar fluxo de liberacao',
            status='sugestao',
        )

        response = self.client.get(reverse('operacoes:dashboard'))

        self.assertContains(response, 'Reduzir espera na doca')

    def test_dashboard_mostra_percentuais_mensuraveis(self):
        response = self.client.get(reverse('operacoes:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '% abertas')
        self.assertContains(response, '% OK')
        self.assertContains(response, '% acoes concluidas')
        self.assertContains(response, '% sugestoes')


class CadastroSiteTests(TestCase):
    def test_lista_modulo_carrega_com_sucesso(self):
        response = self.client.get(reverse('operacoes:lista_modulo', args=['operadores']))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Operadores')

    def test_cria_operador_pelo_site(self):
        response = self.client.post(reverse('operacoes:criar_registro', args=['operadores']), {
            'nome': 'Maria Souza',
            'matricula': '002',
            'turno': 'B',
            'ativo': 'on',
        })

        self.assertRedirects(response, reverse('operacoes:lista_modulo', args=['operadores']))
        self.assertTrue(Operador.objects.filter(matricula='002').exists())

    def test_exporta_modulo_para_excel(self):
        Operador.objects.create(nome='Maria Souza', matricula='002', turno='B')

        response = self.client.get(reverse('operacoes:exportar_modulo', args=['operadores']))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8-sig')
        self.assertIn('attachment; filename="operadores.csv"', response['Content-Disposition'])
        self.assertIn('Maria Souza', response.content.decode('utf-8-sig'))

    def test_nao_exclui_registro_com_senha_errada(self):
        operador = Operador.objects.create(nome='Maria Souza', matricula='002', turno='B')

        response = self.client.post(reverse('operacoes:excluir_registro', args=['operadores', operador.pk]), {
            'senha_exclusao': 'senha-errada',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Senha incorreta')
        self.assertTrue(Operador.objects.filter(pk=operador.pk).exists())

    def test_exclui_registro_pelo_site_com_senha_correta(self):
        operador = Operador.objects.create(nome='Maria Souza', matricula='002', turno='B')

        response = self.client.post(reverse('operacoes:excluir_registro', args=['operadores', operador.pk]), {
            'senha_exclusao': '1234',
        })

        self.assertRedirects(response, reverse('operacoes:lista_modulo', args=['operadores']))
        self.assertFalse(Operador.objects.filter(pk=operador.pk).exists())


class MovimentacaoTests(TestCase):
    def test_movimentacao_registra_perda_operacional(self):
        operador = Operador.objects.create(nome='Carlos Silva', matricula='001', turno='A')
        empilhadeira = Empilhadeira.objects.create(codigo='EMP-01', modelo='GLP')

        movimentacao = Movimentacao.objects.create(
            data_hora=timezone.now(),
            operador=operador,
            empilhadeira=empilhadeira,
            tipo='tempo',
            tempo_minutos=35,
            custo_reais=120,
            motivo='Aguardando liberacao de doca',
        )

        self.assertEqual(movimentacao.tempo_minutos, 35)
        self.assertIn('Aguardando liberacao de doca', str(movimentacao))

    def test_cadastro_pela_area_diego_fica_no_dashboard_diego(self):
        operador = Operador.objects.create(nome='Diego Operador', matricula='003', turno='C')
        empilhadeira = Empilhadeira.objects.create(codigo='EMP-03', modelo='Eletrica')

        response = self.client.post(reverse('operacoes:criar_registro_perfil', args=['diego', 'movimentacoes']), {
            'data_hora': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'operador': operador.pk,
            'empilhadeira': empilhadeira.pk,
            'tipo': 'tempo',
            'tempo_minutos': 20,
            'custo_reais': 50,
            'motivo': 'Registro do Diego',
            'observacao': '',
        })

        self.assertRedirects(response, reverse('operacoes:lista_modulo_perfil', args=['diego', 'movimentacoes']))
        self.assertTrue(Movimentacao.objects.filter(motivo='Registro do Diego', responsavel_dashboard='diego').exists())

    def test_formulario_perfil_nao_mostra_responsavel_dashboard(self):
        response = self.client.get(reverse('operacoes:criar_registro_perfil', args=['diego', 'movimentacoes']))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Responsavel dashboard')
