def get_minor(df, val_index, checking_def):
    # Define índice inicial
    minor_index = 0
    
    # Passa por cada valor
    #for index, row in df.iterrows():
    for i in range(df.shape[0]):
        date1 = list(df.iloc[minor_index])[val_index]
        date2 = list(df.iloc[i])[val_index]
        
        #if value < arr[minor_index]:
        if checking_def(date2, date1):
            minor_index = i  # Atualiza o índice do menor valor encontrado'''
            
    return minor_index

def selection_sort(df, val_index, checking_def):
    new_arr = []
    
    while len(arr) > 0:
        minor_index = get_minor(df, val_index, checking_def)
        new_arr.append(df.pop(minor_index))

    return new_arr
