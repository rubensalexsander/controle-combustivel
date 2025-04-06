# controle-combustivel-public
Sistema desenvolvido para atividade extensionista que visa auxiliar em processo administrativo de controle de combustível para viaturas da polícia

Link planilha e formulário de exemplo que deverão ser implantados: https://drive.google.com/drive/folders/1jVTqp72AUoP0NCn5pskz-T_gy8Q9KnBH?usp=drive_link

# Funcionamento do sistema:
- Após o policial realizar o abastecimento, deverá ser preenchido um formulário como o que está no link acima.
- Os dados ficarão armazenados na planilha do Google Sheets e poderão ser analisados
- O aplicativo "Controle Combustível" será implementado em um computador na sede da delegacia e através dele será possível gerar relatórios e análises dos abastecimentos com base nos dados dos preenchimentos dos formulários.
- Inicialmente, o aplicativo "Controle Combustível" irá gerar uma planilha conforme modelo prévio com os dados de um mês específico.

# Tecnologias do sistema
- Google Sheets e Google Forms
- Python (Google Sheets API, Pandas, Tkinter, Openpyxl e outras bibliotecas)

# Como implementar o sistema:
- Fazer o download e instalar o Python em https://www.python.org;
- Fazer o download deste repositório;
- Extrair arquivos;
- Copiar a pasta "controle-combustivel" para o endereço de instalação;
- Abrir o terminal;
- Escrever comandos que estão no arquivo "controle-combustivel/infor" para instalar dependências;
- Abrir o arquivo "controle-combustivel/configs.py";
- Fazer configurações:
  - install_path - Endereço de instalação
  - cia_name = Nome da delegacia que estara no relatorio mensal
  - vps_dict = Viaturas fixas da delegacia
  - spread_sheet_id = Id da planilha Google criada
  - sheet_pag_name = Nome da página da planilha que os dados do formulário estão
  - sheet_range = Intervalo dos dados. Exemplo:'C:I' (O aplicativo só irá solicitar os dados de C a I)
  - sheet_map = Dados que serão usados para processamento dos dados no aplicativo
- Fazer um atalho da pasta "controle-combustivel/app" para a área de trabalho;
- Renome o atalho para Controle Combustível ou qualquer nome de preferência;
- Se preferir, é possível mudar o icone do atalho para a imagem "police.ico" que está na pasta "controle-combustivel/img".
