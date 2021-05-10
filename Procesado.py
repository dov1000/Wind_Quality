
# coding: utf-8

#Codigo de procesamiento de datos, revisamos que todos tengan la misma cantidad de columnas, el formato de la fecha; se unen todos los archivos para formar una sola tabla y se cambia el nombre. 


import numpy as np
import pandas as pd
import os


#obtengo los archivos en las direcciones
location = os.getcwd()
files = []
no = []
for file in os.listdir(location):
    string = str(file)
    if "ipynb" in string: 
        no.append(string)
    elif "py" in string:
        no.append(string)
    elif "windog" in string:
        no.append(string)
    else: 
        files.append(string)


# In[36]:


#cargo los archivos como entradas de una matriz
Datos = []
for data in files:
    d = pd.read_csv(data, skiprows = {0,2,3},low_memory=False)
    Datos.append(d)
    del d


for i in range(len(files)):
    print('Archivo: ' +  str(files[i]) + ' Columnas: ' + str(Datos[i].shape[1]) )

# In[38]:


#concateno todos los datos
Union = pd.concat(Datos).drop_duplicates()
#.reset_index(drop=True)


x=[]
count = -1
for string in Union['TIMESTAMP']:
    count = count+1
    try: 
        y = pd.to_datetime(string)
        x.append(y)
    except ValueError:
        print('ERROR at index {}: {!r}'.format(count, string))

# In[39]:


#cambio a formato de fecha y ordeno
Union['TIMESTAMP'] = pd.to_datetime(Union.TIMESTAMP)
Union = Union.sort_values(by='TIMESTAMP')


# In[ ]:
#Quito los simbolos extraños.
name = ''.join([i for i in location[-24:] if not i.isdigit()])
for each in ['\\','_','-','/','']:
	if each in name:
		name = name.replace(each,'')

Union.to_csv(name+'_'+'union', index = False)

