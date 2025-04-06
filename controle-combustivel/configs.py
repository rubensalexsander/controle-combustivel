# App sets ------------------------------------------------------
install_path = r'/home/alex/Documents/dev/repositorios/abastecimento-vp/abastecimento-vp'
cia_name = '6° Pel / 2° Gp - Crucilândia'
resolution = [320, 240]

# VPs sets ------------------------------------------------------
vps_dict = {
    '34730':['SYC-5E03', 5],
    '27990':['QMV-1210', 7],
    'outros':['', 9],
}

# Google sheet sets ---------------------------------------------
spread_sheet_id = '1IbouRnIx2tJbI_ScCUALjW_CPJocKLitErhoL1MOcsU'
sheet_pag_name = 'plan1'
sheet_range = 'C:I'

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
