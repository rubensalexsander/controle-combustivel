def date_minor(date1, date2, sep='/', include_equal=False):
    # Faz split das datas
    date1_day, date1_month, date1_year = date1.split(sep=sep)
    date2_day, date2_month, date2_year = date2.split(sep=sep)
    
    # Converte datas para int
    date1_int = int(date1_year+date1_month.zfill(2)+date1_day.zfill(2))
    date2_int = int(date2_year+date2_month.zfill(2)+date2_day.zfill(2))
    
    # Verifica se date1 é menor que date2 e retorna
    return date1_int <= date2_int if include_equal else date1_int < date2_int

def date_between(date, date1, date2, sep='/', include_equal=True):
    # Verifica se date1 é menor que date e se date é menor que date2
    date1_minor = date_minor(date1, date, sep=sep, include_equal=include_equal)
    date2_major = date_minor(date, date2, sep=sep, include_equal=include_equal)
    
    # Retorna conjunção
    return date1_minor and date2_major
