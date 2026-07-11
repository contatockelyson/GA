# Controle GA

Sistema Django para acompanhar produtividade de movimentacoes de empilhadeira e rotinas de GA.

## Modulos iniciais

- Operadores e empilhadeiras
- Perdas de movimentacao com tempo, custo em reais e motivo
- Ocorrencias de seguranca com foto, motivo, acao, data e hora
- Etiquetas abertas, fechadas e canceladas
- Limpezas internas e externas realizadas nas empilhadeiras
- Perdas interligadas a seguranca e movimentacoes
- Reunioes de GA e acoes

## Como rodar

O projeto foi criado com Django 6.0.7.

```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Se o comando `python` estiver instalado no Windows, tambem pode usar:

```powershell
python manage.py runserver
```

Ou use o atalho no PowerShell/CMD:

```powershell
.\runserver.bat
```

Depois acesse:

- Dashboard: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

Usuario inicial de desenvolvimento:

- Login: `admin`
- Senha: `admin123`

## Comandos uteis

```powershell
.\.venv\Scripts\python.exe manage.py makemigrations
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py check
```

Tambem da para usar:

```powershell
.\manage.bat check
.\manage.bat migrate
.\manage.bat createsuperuser
```
