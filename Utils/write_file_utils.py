import csv
from typing import List
import json

def write_csv(csv_name: str, headers: List[str], data: List[str]):
    
    '''
    '''
    
    try:       
        with open(f'./csv/{csv_name}.csv', mode='w', newline='') as csv_file:
            writter = csv.DictWriter(csv_file, fieldnames=headers)
            writter.writeheader()
            writter.writerows(data)
        print(f'Se escrió correctamente el archivo: {csv_name}.csv en la carpeta csv')
        
    except:      
        print('Ha ocurrido un error, no se ha escrito el archivo correctamente')
        
def write_json(json_name: str, data: List[str]):
    
    '''
    '''
    
    try:
        with open(f'./csv/{json_name}.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f'Se escrió correctamente el archivo: {json_name}.json en la carpeta csv')
            
    except:
        print('Ha ocurrido un error, no se ha escrito el archivo correctamente')
        
    
    
        