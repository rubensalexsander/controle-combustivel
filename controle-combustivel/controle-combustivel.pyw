from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from openpyxl import load_workbook
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Alignment
from openpyxl.utils import rows_from_range
from random import randint
from lib.arsqlite import *
import pandas as pd
import tkinter as tk
import tkinter.ttk as ttk
from configs import *
from datetime import datetime
from lib.datepy import *
from lib.selection_sort import *

def get_gsheet_data(start_date, final_date):
    # Pegando dados da sheet google
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    
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
    
    # Selecionando dados que estão no intervalo
    for index, row in df_sheet.iterrows():
        date = row[sheet_map['data']]
        # Verifica se a data da row está no intervalo
        if not date_between(date=date, date1=start_date, date2=final_date):
            # Remove o row que não está no range
            df_sheet = df_sheet.drop(index)
    
    # Redefine o index de df_sheet
    df_sheet = df_sheet.reset_index(drop=True)
    
    # Ordenando dados que estão no intervalo pela data
    new_df = pd.DataFrame(columns=df_sheet.columns)
    
    for i in range(df_sheet.shape[0]):
        # Encontra índice de row da menor data
        minor_index = get_minor(df_sheet, sheet_map['data'], date_minor)
        
        # Adiciona row de menor data ao novo df
        new_df.loc[len(new_df)] = df_sheet.iloc[minor_index]
        
        # Remove row do índice de menor data
        df_sheet = df_sheet.drop(minor_index)
        
        # Redefine o index de df_sheet
        df_sheet = df_sheet.reset_index(drop=True)

    # Retoma dados para df_sheet
    df_sheet = new_df
    
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
        data = row[sheet_map['data']]
        hora = row[sheet_map['hora']]
        km = int(row[sheet_map['km']])
        litragem = row[sheet_map['litragem']]
        combustivel = row[sheet_map['combustivel']]
        origem = row[sheet_map['origem']]

        if prefixo in list(vps_dict_copy.keys()):
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
    
    # Salva planilha final
    arq.save(f"{install_path}/app/planilha-controle-combustível-{start_date.replace('/', '-')}a{final_date.replace('/', '-')}-{randint(1001,9999)}.xlsx")

class WinMain():
    def __init__(self, resolution=[320, 240], title='Abastecimento-VP'):
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
        #self.win.iconbitmap(rf'{install_path}/img/police.ico')
        # Definições da janela #END
        
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
        
        frame_title_bt = tk.Frame(self.win)
        frame_title_bt.pack(fill='x', padx=5, pady=[0, 5])
        
        bt_configurar = ttk.Button(frame_title_bt, image=photo, command=self.open_config, width=10)
        bt_configurar.pack(pady=[5, 0], side=tk.RIGHT)
        
        tx_mensagem = tk.Label(frame_title_bt, text='Gerar planilha abastecimento', font=['arial', 14])
        tx_mensagem.pack(padx=5, pady=[15, 0], anchor='w')
        
        tx_cia_name = tk.Label(frame_title_bt, text=f'{cia_name}', font=['arial', 11])
        tx_cia_name.pack(padx=8, anchor='w')
        
        frame = tk.Frame(self.win)
        frame.pack(fill='both', padx=10)
        
        frame_mes_ano = tk.Frame(frame)
        frame_mes_ano.pack(padx=10, pady=5)
        
        frame_mes = tk.Frame(frame_mes_ano)
        frame_mes.pack(anchor='w', pady=[0, 5])
        tx_mes = tk.Label(frame_mes, text='Mês: ')
        tx_mes.pack(side='left')
        
        current_year = str(datetime.now().year)
        
        if len(str(datetime.now().month)) == 1: current_month = '0' + str(datetime.now().month)
        else: current_month = str(datetime.now().month)
        
        month_var = tk.StringVar()
        
        combo_mes = ttk.Combobox(frame_mes, textvariable=month_var, width=5)
        combo_mes.pack(side='left')
        combo_mes['values'] = list(quant_day.keys())
        combo_mes.current(list(quant_day.keys()).index(current_month))
        
        year_var = tk.StringVar()
        frame_year = tk.Frame(frame_mes_ano)
        frame_year.pack(anchor='w')
        tx_year = tk.Label(frame_year, text='Ano: ')
        tx_year.pack(side='left')
        
        combo_years = [str(i) for i in range(2025, 2051)]
        
        combo_year = ttk.Combobox(frame_year, textvariable=year_var, width=8)
        combo_year.pack(side='left')
        combo_year['values'] = combo_years
        combo_year.current(combo_years.index(current_year))
        
        tx_mensagem_var = tk.StringVar()
        tx_mensagem_var.set(value='')
        
        def fazer_planilha():
            tx_mensagem['text'] = 'Buscando dados da planilha Google.'
            win_main.win.update()
            
            month = month_var.get()
            year = year_var.get()
            
            # Datas
            start_date = f'01/{month}/{year}'
            final_date = f'{quant_day[month]}/{month}/{year}'
            
            query = get_gsheet_data(start_date, final_date)
            
            tx_mensagem['text'] = 'Gerando planilha.'
            win_main.win.update()
            
            plan_generation(query, start_date, final_date)
            
            tx_mensagem['text'] = 'Planilha gerada.'
            win_main.win.update()
        
        bt_confirmar = ttk.Button(frame, text='Confirmar', command=fazer_planilha)
        bt_confirmar.pack(pady=[10, 5])
        
        tx_mensagem = tk.Label(frame)
        tx_mensagem.pack(pady=5)

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
        #self.win.iconbitmap(rf'{install_path}/img/police.ico')
        # Definições da janela #END
        
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
        
        # bt salvar
        bt_salvar = ttk.Button(frame, text='Salvar', command=salvar)
        bt_salvar.pack(anchor='s', pady=[20,0]) 

if __name__ == '__main__':
    win_main = WinMain(resolution=resolution)
    win_main.win.mainloop()
