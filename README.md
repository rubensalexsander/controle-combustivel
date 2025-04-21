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
- Fazer o download e instalar o **Python** em 🔗 https://www.python.org;
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
- Criar credenciais do Google Sheets. (Link para criação da **credencial**: 🔗 https://developers.google.com/workspace/guides/create-credentials?hl=pt-br)
- No Google Cloud, clique em Credenciais, em IDs do cliente OAuth 2.0, clique na sua credencial e em "Chave secreta do cliente" clique na seta de download do JSON;
- Após o download, copie o arquivo "credentials.json" para a pasta "controle-combustivel/credentials"; ⚠️ **Na primeira execução, será requerido login em uma conta Google. Certifique-se de que a planilha está acessível para seu usuário!**
- Faça um atalho do script "controle-combustivel.pyw" para a área de trabalho;

# Formulário de exemplo:
![Screenshot from 2025-04-10 16-02-03](https://github.com/user-attachments/assets/d621a45e-bb91-4543-a50a-9a6e024e8148)


# Planilha de respostas: 
(**Dados fictícios** ⚠️)
![Screenshot from 2025-04-10 16-02-31](https://github.com/user-attachments/assets/ba47ae03-790a-4c15-98f0-0352956a93b2)



# Janelas do aplicativo:
![Screenshot from 2025-04-21 09-59-58](https://github.com/user-attachments/assets/88580d42-2705-43f3-b2cd-88fb59c404e4)
![Screenshot from 2025-04-21 10-00-18](https://github.com/user-attachments/assets/bf88a075-4c47-4320-85ed-95ce67716dfa)
![Screenshot from 2025-04-10 16-01-23](https://github.com/user-attachments/assets/a6296675-d4c4-4a8c-b711-ec54767aba79)

# Relatório mensal (gerado pelo aplicativo):
(**Dados fictícios** ⚠️)
![Captura de tela 2025-04-11 001916](https://github.com/user-attachments/assets/4c478494-53ff-49cf-9cd2-31b3860cb905)


