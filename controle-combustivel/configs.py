# App sets ------------------------------------------------------
install_path = r'/home/alex/Documents/dev/repositorios/controle-combustivel-public/controle-combustivel'
cia_name = 'Delegacia A - Cidade exemplo'
resolution = [320, 240]

# VPs sets ------------------------------------------------------
vps_dict = {
    '123':['AAA-5544', 5],
    '456':['BBB-2211', 7],
    'outros':['', 9],
}

# Google sheet sets ---------------------------------------------
spread_sheet_id = '19ogjTzqBT0_v-N_7EGmL2eyP22-_E-LhOCB6SR206OA'
sheet_pag_name = 'plan1'
sheet_range = 'B:H'

sheet_map = { #converted to python list (-1)
        'prefixo':0,
        'data':1,
        'hora':2,
        'km':3,
        'litragem':4,
        'combustivel':5,
        'origem':6
    }

# Standard plan sets -----------------------------------------------
standard_plan_pag = 'plan1'
standard_plan_range = 'A:K'

# Other
quant_day = {'01':'31','02':'28','03':'31','04':'30','05':'31','06':'30','07':'31','08':'31','09':'30','10':'31','11':'30','12':'31'}
