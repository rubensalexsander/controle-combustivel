# **controle-combustivel** 🚔📊
Sistema desenvolvido para **atividade extensionista do curso de Ciências da Computação** que visa auxiliar em processo administrativo de controle de combustível para viaturas da polícia. ✅

- Link da pasta com a **planilha e o formulário de exemplo** que deverão ser implantados: 🔗 https://drive.google.com/drive/folders/1jVTqp72AUoP0NCn5pskz-T_gy8Q9KnBH?usp=sharing
- Link de participante do **formulário de exemplo**: 🔗 https://forms.gle/z8jAXbp7tDRouUK9A

# **Funcionamento do sistema**:
- Após o policial realizar o abastecimento, deverá ser preenchido um formulário como o que está no link acima. 🔗
- Os dados ficarão armazenados na planilha do Google Sheets e poderão ser analisados. 📊
- O aplicativo "**Controle Combustível**" será implementado em um computador na sede da delegacia e através dele será possível gerar relatórios e análises dos abastecimentos com base nos dados dos preenchimentos dos formulários.
- Inicialmente, o aplicativo "Controle Combustível" irá gerar uma planilha conforme modelo prévio com os dados de um mês específico.

# Tecnologias do sistema
- Google Sheets e Google Forms
- Python (*Google Sheets API, Pandas, Tkinter, Openpyxl e outras bibliotecas*)

# Como implementar o sistema:
- Fazer o download e instalar o Python em 🔗 https://www.python.org;
- Fazer o download deste repositório;
- Extrair arquivos;
- Copiar a pasta "controle-combustivel" para o endereço de instalação;
- Abrir o terminal;
- Escrever comandos que estão no arquivo "controle-combustivel/infor" para instalar dependências;
- Abrir o arquivo "controle-combustivel/configs.py";
- Fazer configurações: ⚙️
  - install_path - Endereço de instalação
  - cia_name - Nome da delegacia que estará no relatório mensal
  - vps_dict - Viaturas fixas da delegacia
  - spread_sheet_id - Id da planilha Google criada
  - sheet_pag_name - Nome da página da planilha que os dados do formulário estão
  - sheet_range - Intervalo dos dados. Exemplo:'C:I' (O aplicativo só irá solicitar os dados de C a I)
  - sheet_map - Dados que serão usados para processamento dos dados no aplicativo
- Criar credenciais do Google Sheets. (Link para criação da credencial: 🔗 https://developers.google.com/workspace/guides/create-credentials?hl=pt-br)
- No Google Cloud, clique em Credenciais, em IDs do cliente OAuth 2.0, clique na sua credencial e em "Chave secreta do cliente" clique na seta de download do JSON;
- Após o download, copie o arquivo "credentials.json" para a pasta "controle-combustivel/credentials"; ⚠️ **Na primeira execução, será requerido login em uma conta Google. Certifique-se de que a planilha está acessível para seu usuário!**
- Faça um atalho da pasta "controle-combustivel/app" para a área de trabalho;
- Renomeie o atalho para Controle Combustível ou qualquer nome de preferência;
- Se preferir, é possível mudar o ícone do atalho para a imagem "police.ico" que está na pasta "controle-combustivel/img".


# Formulário de exemplo:
![Screenshot from 2025-04-06 19-57-57](https://github.com/user-attachments/assets/4448e55d-07e7-45da-a148-7ef6287c1039)

# Planilha de respostas: 
(**Dados fictícios** ⚠️)

![Screenshot from 2025-04-06 20-09-08](https://github.com/user-attachments/assets/c7c37a9b-af08-4181-bb88-20cf12e0c878)


# Janelas do aplicativo:
![Screenshot from 2025-04-10 11-32-26](https://github.com/user-attachments/assets/0fe479a5-36dd-435d-a16f-f9daec281aa7)
![Screenshot from 2025-04-10 11-32-37](https://github.com/user-attachments/assets/45080c78-102b-47d6-9eaa-d3443e2f6e98)
![Screenshot from 2025-04-10 11-32-58](https://github.com/user-attachments/assets/621b843f-f16e-437b-8fcf-60916aef2cdd)


# Relatório mensal (gerado pelo aplicativo):


