from __future__ import print_function
import pickle, os.path, calendar
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from openpyxl import load_workbook
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Alignment
from openpyxl.utils import rows_from_range
from random import randint
from datetime import datetime, date
from lib.arsqlite import *
from configs import *
import pandas as pd
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
from tkcalendar import DateEntry

def get_gsheet_data(start_date, final_date):
    ''' Buscando dados de planilha Google Sheets usando o Sheets API '''
    # Definições
    credentials_path = rf'{install_path}/credentials/credentials.json'
    token_path = rf'{install_path}/credentials/token.pickle'
    
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    
    # The ID and range of a sample spreadsheet.
    pag_range = f"'{sheet_pag_name}'!{sheet_range}"
    creds = None
    
    # The file token.pickle stores the user's access and refresh tokens, and is created automatically when 
    # the authorization flow completes for the first time.
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
            
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spread_sheet_id, range=pag_range).execute()
    values = result.get('values', [])
    
    # Tratando dados da planilha google
    df_sheet = pd.DataFrame(values)
    df_sheet = df_sheet.drop(0)
    
    # Converte coluna data e hora para datetime
    df_sheet[sheet_map['datahora']] = pd.to_datetime(df_sheet[sheet_map['datahora']], format='%d/%m/%Y %H:%M:%S')
    
    # Selecionando dados que estão no intervalo
    for index, row in df_sheet.iterrows():
        date = row[sheet_map['datahora']]
        
        # Verifica se a data da row está no intervalo
        if not ((date >= start_date) and (date <= final_date)):
            # Remove o row que não está no range
            df_sheet = df_sheet.drop(index)
    
    # Ordena pelo datetime
    df_sheet = df_sheet.sort_values(by=sheet_map['datahora'])
    
    # Redefine o index de df_sheet
    df_sheet = df_sheet.reset_index(drop=True)
    
    return df_sheet

def plan_generation(df_sheet, start_date, final_date):
    # Paths definitions
    plan_standard_path = rf'{install_path}/other/controle-combustivel-padrao.xlsx'
    db_path = rf'{install_path}/db/db.db' 
    
    # Abre planilha padrão
    arq = load_workbook(plan_standard_path)
    plan = arq[standard_plan_pag]
    
    # Abrindo DB
    db = DbSqlite(local=db_path)
    
    # Cria cópia para trabalhar nessa geração da planilha
    vps_dict_copy = {i: vps_dict[i][:] for i in list(vps_dict.keys())}
    
    # Adiciona nome da cia/destacamento
    plan[f'A1'] = cia_name
    
    # Iterando sob o df
    for index, row in df_sheet.iterrows():
        # Define variáveis
        prefixo = row[sheet_map['prefixo']]
        data = row[sheet_map['datahora']].strftime('%d/%m/%Y')
        hora = row[sheet_map['datahora']].strftime('%H:%M')
        km = int(row[sheet_map['km']])
        litragem = row[sheet_map['litragem']]
        combustivel = row[sheet_map['combustivel']]
        origem = row[sheet_map['origem']]
        
        # Verifica se a VP está no db
        prefixo_no_db = False
        
        for i in list(vps_dict_copy.keys()):
            if i in prefixo:
                prefixo_no_db = True
                prefixo = i
        
        if prefixo_no_db:
            placa = vps_dict_copy[prefixo][0]
            y_val = int(vps_dict_copy[prefixo][1])
            vps_dict_copy[prefixo][1] += 1
        else:
            placa = vps_dict_copy['outros'][0]
            y_val = int(vps_dict_copy['outros'][1])
            vps_dict_copy['outros'][1] += 1
            
        # Define o cod
        if origem == 'Prefeitura':
            cod = 2
        elif origem == 'Estado':
            cod = 3
        else: 
            cod = 5
        
        # Define combustivel_cod
        combustivel_cod = db.get_instance(table='combustivel', key=['nome', combustivel])[0][1]
        
        if combustivel_cod.isnumeric():
            combustivel_cod = int(combustivel_cod)

        # Move intervalo
        range_to_move = f'{standard_plan_range[0]}{y_val}:{standard_plan_range[2]}{100}'
        plan.move_range(range_to_move, rows=1, cols=0, translate=True)
        
        # Adiciona borda e alinhamento às novas células
        range_to_border = f'{standard_plan_range[0]}{y_val}:{standard_plan_range[2]}{y_val}'
        for row in rows_from_range(range_to_border):
            for cell in row:
                plan[cell].border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
                plan[cell].alignment = Alignment(horizontal='center', vertical='center', text_rotation=0, wrap_text=False, shrink_to_fit=False, indent=0)
        
        # Adiciona 1 ao position de cada vp abaixo
        for i in list(vps_dict_copy.keys()):
            if (vps_dict_copy[i][1] > (y_val+1)): vps_dict_copy[i][1] += 1
        
        # Adiciona valores às células
        plan[f'A{y_val}'] = int(prefixo)
        plan[f'B{y_val}'] = placa
        plan[f'C{y_val}'] = cod
        plan[f'D{y_val}'] = data
        plan[f'E{y_val}'] = hora[0:5]
        plan[f'G{y_val}'] = km
        plan[f'H{y_val}'] = combustivel_cod
        plan[f'I{y_val}'] = float(litragem.replace(',', '.'))
        plan[f'J{y_val}'] = db.get_instance(table='combustivel', key=['nome', combustivel])[0][2]
        plan[f'J{y_val}'].number_format = 'R$ #,##0.00'
        plan[f'K{y_val}'] = f'=I{y_val}*J{y_val}'
        plan[f'K{y_val}'].number_format = 'R$ #,##0.00'
    
    # Adiciona datas
    plan['P2'] = start_date
    plan['Q2'] = final_date
    
    # Define o local de salvamento
    dir_save = filedialog.askdirectory(title="Selecione uma pasta")
    save_path = f"{dir_save}/planilha-combustível-{str(start_date.strftime('%m/%Y')).replace('/', 'de')}-{randint(1001,9999)}.xlsx"
    
    try:
        if len(dir_save):
            # Salva planilha final
            arq.save(save_path)
            
            # Retorna mensagem
            return f'Planilha salva em: \n{dir_save}'
        else:
            return ''
    except:
            return "Erro ao salvar"

class WinMain():
    def __init__(self, resolution=[400, 300], title='Controle Combustível'):
        self.running = True
        self.resolution = resolution
        self.title = title
        
        # Definições da janela
        self.win = tk.Tk()
        
        geometry = f'{resolution[0]}x{resolution[1]}'
        place = f'{int(self.win.winfo_screenwidth()/2)-int(resolution[0]/2)}+{int(self.win.winfo_screenheight()/2)-int(resolution[1]/1.3)}'
        
        self.win.geometry(f'{geometry}+{place}')
        self.win.title(title)
        self.win.protocol("WM_DELETE_WINDOW", self.finish)
        self.win.option_add('*tearOff', tk.FALSE)
        self.win.resizable(width=0, height=0)
        
        # Chama construtor da janela
        self.constructor()
    
    def finish(self):
        self.win.destroy()
        self.running = False
    
    def open_config(self):
        win_main = WinConfig(title='Configurações', resolution=resolution)
        win_main.win.mainloop()

    def constructor(self):
        #THEME
        self.win.tk.call("source", rf"{install_path}/theme/azure-ttk-theme/azure.tcl")
        self.win.tk.call("set_theme", "light")
        
        photo = tk.PhotoImage(file=rf'{install_path}/img/gear.png')
        self.photo = photo
        
        photo_grafico = tk.PhotoImage(file=rf'{install_path}/img/grafico.png')
        self.photo_grafico = photo_grafico
        
        frame_title_bt = tk.Frame(self.win)
        frame_title_bt.pack(fill='x', padx=5, side=tk.TOP)
        
        frame_title = tk.Frame(frame_title_bt)
        frame_title.pack(fill='x', padx=5, pady=[0, 5], side=tk.LEFT, anchor='nw')
        
        tx_mensagem = tk.Label(frame_title, text='Gerar planilha Controle de Combustível', font=['arial', 14])
        tx_mensagem.pack(padx=0, pady=[15, 0], anchor='w')
        
        tx_cia_name = tk.Label(frame_title, text=f'{cia_name}', font=['arial', 11])
        tx_cia_name.pack(padx=2, anchor='w')
        
        frame_bts = tk.Frame(frame_title_bt)
        frame_bts.pack(fill='x', padx=0, side=tk.RIGHT)
        
        bt_configurar = ttk.Button(frame_bts, image=photo, command=self.open_config, width=10)
        bt_configurar.pack(pady=[5, 0], side=tk.TOP)
        
        def fazer_grafico():
            # Datas
            start_date = datetime.strptime(f'{date_entry_inicio.get()} 00:00:00', '%d/%m/%Y %H:%M:%S')
            final_date = datetime.strptime(f'{date_entry_fim.get()} 23:59:59', '%d/%m/%Y %H:%M:%S')
            
            # Recupera dados da planilha
            query = get_gsheet_data(start_date, final_date)
            
            # Manipula dados
            dados_data = []
            dados_gasto_acul_total = []
            
            total_gasto_etanol_litragem = 0
            total_gasto_gasolina_litragem = 0
            total_gasto_diesel_litragem = 0
            total_gasto_prefeitura = 0
            total_gasto_estado = 0
            gasto_total = 0
            
            # Abrindo DB
            db_path = rf'{install_path}/db/db.db' 
            db = DbSqlite(local=db_path)
            
            # Valores dos litros
            val_litro_etanol = db.get_instance(table='combustivel', key=['nome', 'Etanol'])[0][2]
            val_litro_gasolina = db.get_instance(table='combustivel', key=['nome', 'Gasolina'])[0][2]
            val_litro_diesel = db.get_instance(table='combustivel', key=['nome', 'Diesel'])[0][2]
            
            # Transforma litragem para gasto aculmulado em R$
            for index, row in query.iterrows():
                # Define variáveis
                dados_data.append(row[sheet_map['datahora']].strftime('%d/%m'))
                
                litragem = float(row[sheet_map['litragem']].replace(',', '.'))
                combustivel = row[sheet_map['combustivel']]
                origem = row[sheet_map['origem']]
                
                if combustivel == 'Etanol':
                    # Total do abastecimento
                    valor_total = litragem * val_litro_etanol
                    
                    # Adiciona às variáveis
                    total_gasto_etanol_litragem += litragem
                    
                elif combustivel == 'Gasolina':
                    # Total do abastecimento
                    valor_total = litragem * val_litro_gasolina
                    
                    # Adiciona às variáveis
                    total_gasto_gasolina_litragem += litragem
                    
                elif combustivel == 'Diesel':
                    # Total do abastecimento
                    valor_total = litragem * val_litro_diesel
                    
                    # Adiciona às variáveis
                    total_gasto_diesel_litragem += litragem
                
                # Soma à variável de aculmulação
                gasto_total += valor_total
                
                # Adiciona o valor para prefeitura/estado
                if origem == 'Prefeitura':
                    total_gasto_prefeitura += valor_total
                elif origem == 'Estado':
                    total_gasto_estado += valor_total
                
                # Adiciona à serie temporal
                dados_gasto_acul_total.append(gasto_total)
                
            # Cria gráfico
            fig, ax = plt.subplots()
            
            ax.plot(dados_data, dados_gasto_acul_total, color='blue', marker='o', linestyle='--')
            plt.setp(ax.get_xticklabels(), rotation=55, fontsize=8)
            ax.set_title(f"Gasto de combusível {start_date.strftime('%d/%m')} a {final_date.strftime('%d/%m')}")
            ax.set_xlabel("Data")
            ax.set_ylabel("Gasto total (R$)")
            
            # Define texo para mostrar
            string = 'Informações:\n'
            string += f'\n\n'
            string += f'Etanol: {total_gasto_etanol_litragem:.2f} litros\n'.replace('.', ',')
            string += f'Gasolina: {total_gasto_gasolina_litragem:.2f} litros\n'.replace('.', ',')
            string += f'Diesel: {total_gasto_diesel_litragem:.2f} litros\n'.replace('.', ',')
            string += f'\n\n'
            string += f'Gastos Prefeitura: R${total_gasto_prefeitura:.2f}\n'.replace('.', ',')
            string += f'Gastos Estado: R${total_gasto_estado:.2f}\n'.replace('.', ',')
            string += f'\n\n'
            
            # Escreve informações ao lado do gráfico
            fig.text(0.72, 0.5, string, fontsize=8, ha='left', va='center')
            fig.text(0.72, 0.3, f'Gasto Total: R${dados_gasto_acul_total[-1]:.2f}\n'.replace('.', ','), fontsize=8, fontweight='bold', ha='left', va='center')
            fig.subplots_adjust(right=0.7, bottom=0.15)
            fig.canvas.manager.set_window_title(f"Análise dos gastos de Combustível")

            # Abre gráfico
            plt.show()
        
        bt_grafico = ttk.Button(frame_bts, image=photo_grafico, command=fazer_grafico, width=10)
        bt_grafico.pack(pady=[5, 0])
        
        frame = tk.Frame(self.win)
        frame.pack(fill='both', padx=10)
        
        frame_datas = tk.Frame(frame)
        frame_datas.pack(padx=10, pady=5)
        
        # Data de início
        frame_data_inicio = tk.Frame(frame_datas)
        frame_data_inicio.pack(anchor='e', padx=[0, 30], pady=[0, 5])
        
        date_entry_inicio = DateEntry(frame_data_inicio, 
                                      width=12, 
                                      background='darkblue', 
                                      borderwidth=1, 
                                      date_pattern='dd/mm/yyyy', 
                                      firstweekday='sunday', 
                                      showweeknumbers=False, 
                                      locale='pt_BR')
        
        date_entry_inicio.pack(side='right')
        
        tx_data_inicio = tk.Label(frame_data_inicio, text='De: ')
        tx_data_inicio.pack(side='right')
        
        # Data de fim
        frame_data_fim = tk.Frame(frame_datas)
        frame_data_fim.pack(anchor='e', padx=[0, 30])
        
        date_entry_fim = DateEntry(frame_data_fim, 
                                   width=12, 
                                   background='darkblue', 
                                   borderwidth=1, 
                                   date_pattern='dd/mm/yyyy', 
                                   showweeknumbers=False, 
                                   locale='pt_BR')
        
        date_entry_fim.pack(side='right')
        
        tx_data_fim = tk.Label(frame_data_fim, text='Até: ')
        tx_data_fim.pack(side='right')
        
        tx_mensagem_var = tk.StringVar()
        tx_mensagem_var.set(value='')
        
        def fazer_planilha():
            tx_mensagem['text'] = 'Buscando dados da planilha Google.'
            win_main.win.update()
            
            # Datas
            start_date = datetime.strptime(f'{date_entry_inicio.get()} 00:00:00', '%d/%m/%Y %H:%M:%S')
            final_date = datetime.strptime(f'{date_entry_fim.get()} 23:59:59', '%d/%m/%Y %H:%M:%S')
            
            mensagem = 'Gerando planilha.'
            
            print(mensagem)
            
            query = get_gsheet_data(start_date, final_date)
            
            tx_mensagem['text'] = mensagem
            win_main.win.update()
            
            mensagem = plan_generation(query, start_date, final_date)
            
            tx_mensagem['text'] = mensagem
            print(mensagem)
            win_main.win.update()
        
        bt_confirmar = ttk.Button(frame, text='Confirmar', command=fazer_planilha)
        bt_confirmar.pack(pady=[10, 5])
        
        tx_mensagem = tk.Label(frame)
        tx_mensagem.pack(pady=5)
        
        # Define datas dos date_entry
        mes_atual = datetime.now().month
        ano_atual = datetime.now().year
        
        # Retorna o número de dias do mês atual
        _, dias_no_mes = calendar.monthrange(int(ano_atual), int(mes_atual))
        
        # Define a data inicial date_entry_inicio
        data_inicial_inicio = date(ano_atual, mes_atual, 1)
        date_entry_inicio.set_date(data_inicial_inicio)
        
        # Define a data inicial date_entry_fim
        data_inicial_fim = date(ano_atual, mes_atual, dias_no_mes)
        date_entry_fim.set_date(data_inicial_fim)

class WinConfig():
    def __init__(self, resolution=[320, 240], title='win1'):
        self.running = True
        self.resolution = resolution
        self.title = title
        
        # Definições da janela
        self.win = tk.Toplevel(win_main.win)
        
        geometry = f'{resolution[0]}x{resolution[1]}'
        place = f'{int(self.win.winfo_screenwidth()/2)-int(resolution[0]/2)}+{int(self.win.winfo_screenheight()/2)-int(resolution[1]/1.3)}'
        
        self.win.geometry(f'{geometry}+{place}')
        self.win.title(title)
        self.win.protocol("WM_DELETE_WINDOW", self.finish)
        self.win.resizable(width=0, height=0)
        self.win.focus_force()
        self.win.grab_set()
        self.win.option_add('*tearOff', tk.FALSE)
        
        # Chama o construtor da janela
        self.constructor()
        
    def finish(self):
        self.win.destroy()
        self.running = False
    
    def constructor(self):
        frame = ttk.Frame(self.win)
        frame.pack(padx=10, pady=10)
        
        tx_config = ttk.Label(frame, text='Configurações', font=['arial', 12])
        tx_config.pack(pady=[0, 15])
        
        # Abrindo DB
        db_path = rf'{install_path}/db/db.db'
        db = DbSqlite(local=db_path)
        
        # Etanol
        current_etanol = str(db.get_instance(table='combustivel', key=['nome', 'Etanol'])[0][2]).replace('.', ',')
        
        frame_etanol = ttk.Frame(frame)
        frame_etanol.pack(pady=[0, 3], anchor='e')
        
        tx_etanol = ttk.Label(frame_etanol, text='Valor unitário Etanol: R$')
        tx_etanol.pack(side=tk.LEFT)
        
        entry_etanol = ttk.Entry(frame_etanol, width=4)
        entry_etanol.pack(side=tk.LEFT)
        entry_etanol.insert(0, current_etanol)
        
        # Gasolina
        current_gasolina = str(db.get_instance(table='combustivel', key=['nome', 'Gasolina'])[0][2]).replace('.', ',')
        
        frame_gasolina = ttk.Frame(frame)
        frame_gasolina.pack(pady=[0, 3], anchor='e')
        
        tx_gasolina = ttk.Label(frame_gasolina, text='Valor unitário Gasolina: R$')
        tx_gasolina.pack(side=tk.LEFT)
        
        entry_gasolina = ttk.Entry(frame_gasolina, width=4)
        entry_gasolina.pack(side=tk.LEFT)
        entry_gasolina.insert(0, current_gasolina)
        
        # Diesel
        current_diesel = str(db.get_instance(table='combustivel', key=['nome', 'Diesel'])[0][2]).replace('.', ',')
        
        frame_diesel = ttk.Frame(frame)
        frame_diesel.pack(pady=[0, 3], anchor='e')
        
        tx_diesel = ttk.Label(frame_diesel, text='Valor unitário Diesel: R$')
        tx_diesel.pack(side=tk.LEFT)
        
        entry_diesel = ttk.Entry(frame_diesel, width=4)
        entry_diesel.pack(side=tk.LEFT)
        entry_diesel.insert(0, current_diesel)
        
        def salvar():
            # Take values
            etanol_new_val = float(entry_etanol.get().replace(',', '.'))
            gasolina_new_val = float(entry_gasolina.get().replace(',', '.'))
            diesel_new_val = float(entry_diesel.get().replace(',', '.'))
            
            # Set values in db
            db.edit_instance(table='combustivel', key=['nome', 'Etanol'], attribute='valor', value=etanol_new_val)
            db.edit_instance(table='combustivel', key=['nome', 'Gasolina'], attribute='valor', value=gasolina_new_val)
            db.edit_instance(table='combustivel', key=['nome', 'Diesel'], attribute='valor', value=diesel_new_val)
            
            # Close win
            self.finish()
        
        # Test treeview
        colunas = ['prefixo', 'placa', 'Reserva']
        
        '''tree = ttk.Treeview(frame, columns=colunas, show='headings')
        
        # Função para carregar dados da tabela para a Treeview
        def carregar_dados():
            #for item in tree.get_children():
            #    tree.delete(item)

            table_viaturas = db.get_table(tabela='viaturas')
            
            for row in table_viaturas:
                tree.insert("", "end", values=row)
        
        carregar_dados()
        
        for col in colunas:
            tree.heading(col, text=col)
        
        tree.pack()'''
        
        colunas = ("Prefixo", "Placa", "Res")
        tree = ttk.Treeview(frame, columns=colunas, show='headings', height=2)
        tree.pack()
        
        # Função para inserir novo registro
        def inserir_dado():
            prefixo = entry_prefixo.get()
            placa = entry_placa.get()
            res = entry_res.get()
            if prefixo and placa and res:
                print(f'dados inseridos: {prefixo}, {placa}, {res}')
                carregar_dados()
                limpar_campos()

        # Função para carregar os dados no Treeview
        def carregar_dados():
            #for item in tree.get_children():
            #    tree.delete(item)

            table_viaturas = db.get_table(tabela='viaturas')
            
            for row in table_viaturas:
                tree.insert("", "end", values=row)

        # Preenche os campos com os dados selecionados na tabela
        def selecionar_linha(event):
            item = tree.selection()
            if item:
                valores = tree.item(item[0])['values']
                entry_prefixo.delete(0, tk.END)
                entry_prefixo.insert(0, valores[0])
                entry_placa.delete(0, tk.END)
                entry_placa.insert(0, valores[1])
                entry_res.delete(0, tk.END)
                entry_res.insert(0, valores[2])

        # Atualiza o registro no banco
        def atualizar_dado():
            prefixo = entry_prefixo.get()
            placa = entry_placa.get()
            res = entry_res.get()
            if prefixo and placa and res:
                print(f'Atualiza no db: {prefixo}, {placa}, {res}')
                carregar_dados()
                limpar_campos()

        # Limpa os campos de entrada
        def limpar_campos():
            entry_prefixo.delete(0, tk.END)
            entry_placa.delete(0, tk.END)
            entry_res.delete(0, tk.END)

        frame_entrys = ttk.Frame(frame)
        frame_entrys.pack(padx=10, pady=10)
        
        # Campos de entrada
        tk.Label(frame_entrys, text="Prefixo:").pack(side='left')
        entry_prefixo = tk.Entry(frame_entrys, width=8)
        entry_prefixo.pack(side='left')

        tk.Label(frame_entrys, text="Placa:").pack(side='left')
        entry_placa = tk.Entry(frame_entrys, width=8)
        entry_placa.pack(side='left')

        tk.Label(frame_entrys, text="Res:").pack(side='left')
        entry_res = tk.Entry(frame_entrys, width=8)
        entry_res.pack(side='left')

        tk.Button(frame, text="Inserir", command=inserir_dado).pack(pady=5)
        tk.Button(frame, text="Atualizar", command=atualizar_dado).pack(pady=5)

        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=80)

        tree.bind("<<TreeviewSelect>>", selecionar_linha)

        carregar_dados()
        
        # bt salvar
        bt_salvar = ttk.Button(frame, text='Salvar', command=salvar)
        bt_salvar.pack(anchor='s', pady=[20,0])

if __name__ == '__main__':
    win_main = WinMain(resolution=resolution)
    win_main.win.mainloop()
