#Control de calidad de datos de viento. 
#Después de correr el script "Procesado",el archivo resultante se utiliza para identificar  los datos anómalos, no representativos y faltantes. 
#Imprime cada uno de los casos en consola y genera archivos con la información para cada uno de las alturas. 



import numpy as np
import pandas as pd
import datetime as dt


#importo Datos
Data = pd.read_csv('TajoGris_union')


# In[3]:


#Formato de tiempo y ordeno
Data['TIMESTAMP'] = pd.to_datetime(Data.TIMESTAMP)
Data = Data.sort_values(by='TIMESTAMP')


# In[4]:


#indexo por fecha y hora
Data.index = pd.DatetimeIndex(Data['TIMESTAMP'])


# In[5]:


#Elimino duplicados
Data = Data.drop_duplicates('TIMESTAMP')


# In[6]:


#lista de todo el rango de tiempo
all_days = pd.date_range(Data.index.min(), Data.index.max(),freq='10min')


# In[7]:


#compruebo que el rango de todos los días sea igual o mayor a la cantidad de datos que tengo y completo la matriz
if len(all_days) >=  Data.shape[0] :
    Complete_Data = Data.reindex(all_days)


# In[8]:


#Obtengo todas las fechas en las que no se hicieron mediciones
nan_rows = Complete_Data[Complete_Data.isnull().T.any().T]


# In[9]:


#Conteo mensual de datos faltantes
faltantes_mensuales = nan_rows.isnull().groupby(pd.Grouper(freq='1M')).sum().astype(int)
faltantes_mensuales.index = faltantes_mensuales.index.strftime('%B %Y')
faltantes_mensuales['NaN'] = faltantes_mensuales['TIMESTAMP']
faltantes_mensuales = faltantes_mensuales['NaN']
faltantes_mensuales


# In[10]:


#cantidad de fechas faltantes
faltantes_tot = nan_rows.shape[0]
faltantes_tot


# In[13]:


#for i in range(Complete_Data['Temperatura_Avg'].shape[0]):
#    if isinstance(Complete_Data.loc[:,'Temperatura_Avg'].iloc[i],float) == False:
 #       Complete_Data.loc[:,'Temperatura_Avg'].iloc[i] = float(Complete_Data.loc[:,'Temperatura_Avg'].iloc[i])


# In[14]:


#identificamos cuales entradas no están en el formato correcto
x= []
for i in range(Complete_Data['Temperatura_Avg'].shape[0]):
    if isinstance(Complete_Data.loc[:,'Temperatura_Avg'].iloc[i],float) == False:
        x.append(i)
#convertimos a float las columnas 41 y 43 según el error al importar los datos
y = len(x)
for i in range(0,y):
    Complete_Data.loc[:,'Temperatura_Avg'].iloc[x[i]] = float(Complete_Data.loc[:,'Temperatura_Avg'].iloc[x[i]])
z= []
for i in range(Complete_Data['Presion_Avg'].shape[0]):
    if isinstance(Complete_Data.loc[:,'Presion_Avg'].iloc[i],float) == False:
        z.append(i)
v = len(z)
for i in range(0,v):
    Complete_Data.loc[:,'Presion_Avg'].iloc[z[i]] = float(Complete_Data.loc[:,'Presion_Avg'].iloc[z[i]])
del x
del y
del z
del v


# In[40]:


def Velocidad60N(var):
    no_representativos = []
    anomalos = []
    vacio = []
    fechas = []
    tabla = []
    new = var
    start = []
    end = []
    j = -1
    idx = len(new.index)
    headers = list(new.T.index)
    dates = new.index
    for i in dates:
        j = j+1
        if new.loc[:,'Vel_60NORTE_Avg'].loc[i] < 0.4:
            fechas.append(str(i))
            if j < idx - 1 :
                if j==0:
                    if i + dt.timedelta(minutes=10) == dates[j+1] :
                        if new.loc[:,'Vel_60NORTE_Avg'].iloc[j+1] < 0.4 :
                            start.append(i)
                    else: 
                        string = str(i) + ' no representativo'
                        print(string)
                        no_representativos.append(str(i))
                        del string
                elif i + dt.timedelta(minutes=10) == dates[j+1] :
                    if new.loc[:,'Vel_60NORTE_Avg'].iloc[j+1] < 0.4 :
                        start.append(i)
                    elif i - dt.timedelta(minutes=10) == dates[j-1]:
                        if new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1] < 0.4:
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                            no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' no representativo'
                        no_representativos.append(str(i))
                        print(string)
                        del string
                elif  i - dt.timedelta(minutes=10) == dates[j-1]: 
                    if new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1] < 0.4 :
                        end.append(i)
                        string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                        no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                        print(string)
                        del string
                        start = []
                        end = []
                else:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
            elif j == idx -1:
                if i - dt.timedelta(minutes=10) != dates[j-1]:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
                else:
                    end.append(i)
                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                    no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                    print(string)
                    start = []
                    end = []
                    del string
        elif ('Vel_40NORTE_Avg' in list(headers)) == True :
            fechas.append(str(i))
            if j < idx - 1 :
                if pd.isna(new.loc[:,'Vel_60NORTE_Avg'].loc[i]) == True:
                    if j==0:
                        if i + dt.timedelta(minutes=10) == dates[j+1]:
                            if pd.isna(new.loc[:,'Vel_60NORTE_Avg'].iloc[j+1]) == True :
                                start.append(i)
                        else:
                            string = str(i) + ' Sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif i + dt.timedelta(minutes=10) == dates[j+1]:
                        if pd.isna(new.loc[:,'Vel_60NORTE_Avg'].iloc[j+1]) == True :
                            start.append(i)
                        elif i - dt.timedelta(minutes=10) == dates[j-1]:
                            if pd.isna(new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1]) == True:
                                end.append(i)
                                string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                                vacio.append(str(start[0]) + ' a ' + str(end[0]))
                                print(string)
                                start = []
                                end = []
                                del string
                        else:
                            string = str(i) + ' sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif  i - dt.timedelta(minutes=10) == dates[j-1] : 
                        if pd.isna(new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1]) == True :
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                            vacio.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' sin dato'
                        print(str(i) + ' sin dato')
                        vacio.append(str(i))
                        del string
                elif new.loc[:,'Vel_60NORTE_Avg'].loc[i] < new.loc[:,'Vel_20NORTE_Avg'].loc[i] or new.loc[:,'Vel_60NORTE_Avg'].loc[i] < new.loc[:,'Vel_40NORTE_Avg'].loc[i] :
                    if j==0:
                        if i + dt.timedelta(minutes=10) == dates[j+1] and new.loc[:,'Vel_60NORTE_Avg'].iloc[j+1] > 0.4 :
                            if new.loc[:,'Vel_60NORTE_Avg'].iloc[j+1] < new.loc[:,'Vel_20NORTE_Avg'].iloc[j+1] or new.loc[:,'Vel_60NORTE_Avg'].iloc[j+1] < new.loc[:,'Vel_40NORTE_Avg'].iloc[j+1] :
                                start.append(i)
                        else:
                            string = str(i) + ' Dato anómalo'
                            anomalos.append(str(i))
                            print(string)
                            del string
                    elif i + dt.timedelta(minutes=10) == dates[j+1] and new.loc[:,'Vel_60NORTE_Avg'].iloc[j+1] > 0.4 :
                        if new.loc[:,'Vel_60NORTE_Avg'].iloc[j+1] < new.loc[:,'Vel_20NORTE_Avg'].iloc[j+1] or new.loc[:,'Vel_60NORTE_Avg'].iloc[j+1] < new.loc[:,'Vel_40NORTE_Avg'].iloc[j+1] :
                            start.append(i)
                        elif i - dt.timedelta(minutes=10) == dates[j-1] and new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1]> 0.4:
                            if new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1] < new.loc[:,'Vel_20NORTE_Avg'].iloc[j-1] or new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1] < new.loc[:,'Vel_40NORTE_Avg'].iloc[j-1]: 
                                end.append(i)
                                if len(start) > 6 :
                                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' datos anómalos'
                                    anomalos.append(str(start[0]) + ' a ' + str(end[0]))
                                    print(string)
                                    start = []
                                    end = []
                                    del string
                                else:
                                    start = []
                                    end = []
                        else:
                            string = str(i) + ' Dato anómalo'
                            anomalos.append(str(i))
                            print(string)
                            del string
                    elif  i - dt.timedelta(minutes=10) == dates[j-1] and new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1]> 0.4: 
                        if new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1] < new.loc[:,'Vel_20NORTE_Avg'].iloc[j-1] or new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1] < new.loc[:,'Vel_40NORTE_Avg'].iloc[j-1]:
                            try:
                                end.append(i)
                                if len(start) > 6 :
                                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' datos anómalos'
                                    anomalos.append(str(start[0]) + ' a ' + str(end[0]))
                                    print(string)
                                    start = []
                                    end = []
                                    del string
                                else:
                                    start = []
                                    end = []
                            except IndexError:
                                print(str(i) + ' error en índice')
                    else:
                        string = str(i) + ' Dato anómalo'
                        anomalos.append(str(i))
                        print(string)
                        del string
            elif j == idx -1: 
                if new.loc[:,'Vel_60NORTE_Avg'].loc[i] < new.loc[:,'Vel_20NORTE_Avg'].loc[i] or new.loc[:,'Vel_60NORTE_Avg'].loc[i] < new.loc[:,'Vel_40NORTE_Avg'].loc[i] :
                    if i - dt.timedelta(minutes=10) != dates[j-1] and new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1]> 0.4:
                        print(str(i) + ' Dato anómalo')
                    else:
                        end.append(i)
                        if len(start) > 6 :
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' datos anómalos'
                            anomalos.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                        else:
                            start = []
                            end = [] 
                elif pd.isna(new.loc[:,'Vel_60NORTE_Avg'].loc[i]) == True:
                    print('Sin medición')
    tabla.append(fechas)
    tabla.append(anomalos)
    tabla.append(no_representativos)
    tabla.append(vacio)
    return tabla


# In[17]:


def Velocidad60S(var):
    no_representativos = []
    anomalos = []
    vacio = []
    fechas = []
    tabla = []
    new = var
    start = []
    end = []
    j = -1
    idx = len(new.index)
    headers = list(new.T.index)
    dates = new.index
    for i in dates:
        j = j+1
        if new.loc[:,'Vel_60NORTE_Avg'].loc[i] < 0.4:
            fechas.append(str(i))
            if j < idx - 1 :
                if j==0:
                    if i + dt.timedelta(minutes=10) == dates[j+1] :
                        if new.loc[:,'Vel_60NORTE_Avg'].iloc[j+1] < 0.4 :
                            start.append(i)
                    else: 
                        string = str(i) + ' no representativo'
                        print(string)
                        no_representativos.append(str(i))
                        del string
                elif i + dt.timedelta(minutes=10) == dates[j+1] :
                    if new.loc[:,'Vel_60NORTE_Avg'].iloc[j+1] < 0.4 :
                        start.append(i)
                    elif i - dt.timedelta(minutes=10) == dates[j-1]:
                        if new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1] < 0.4:
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                            no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' no representativo'
                        no_representativos.append(str(i))
                        print(string)
                        del string
                elif  i - dt.timedelta(minutes=10) == dates[j-1]: 
                    if new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1] < 0.4 :
                        end.append(i)
                        string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                        no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                        print(string)
                        del string
                        start = []
                        end = []
                else:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
            elif j == idx -1:
                if i - dt.timedelta(minutes=10) != dates[j-1]:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
                else:
                    end.append(i)
                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                    no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                    print(string)
                    start = []
                    end = []
                    del string
        elif ('Vel_40NORTE_Avg' in list(headers)) == True :
            fechas.append(str(i))
            if j < idx - 1 :
                if pd.isna(new.loc[:,'Vel_60NORTE_Avg'].loc[i]) == True:
                    if j==0:
                        if i + dt.timedelta(minutes=10) == dates[j+1]:
                            if pd.isna(new.loc[:,'Vel_60NORTE_Avg'].iloc[j+1]) == True :
                                start.append(i)
                        else:
                            string = str(i) + ' Sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif i + dt.timedelta(minutes=10) == dates[j+1]:
                        if pd.isna(new.loc[:,'Vel_60NORTE_Avg'].iloc[j+1]) == True :
                            start.append(i)
                        elif i - dt.timedelta(minutes=10) == dates[j-1]:
                            if pd.isna(new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1]) == True:
                                end.append(i)
                                string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                                vacio.append(str(start[0]) + ' a ' + str(end[0]))
                                print(string)
                                start = []
                                end = []
                                del string
                        else:
                            string = str(i) + ' sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif  i - dt.timedelta(minutes=10) == dates[j-1] : 
                        if pd.isna(new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1]) == True :
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                            vacio.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' sin dato'
                        print(str(i) + ' sin dato')
                        vacio.append(str(i))
                        del string
                elif new.loc[:,'Vel_60NORTE_Avg'].loc[i] < new.loc[:,'Vel_20NORTE_Avg'].loc[i] or new.loc[:,'Vel_60NORTE_Avg'].loc[i] < new.loc[:,'Vel_40NORTE_Avg'].loc[i] :
                    if j==0:
                        if i + dt.timedelta(minutes=10) == dates[j+1] and new.loc[:,'Vel_60NORTE_Avg'].iloc[j+1] > 0.4 :
                            if new.loc[:,'Vel_60NORTE_Avg'].iloc[j+1] < new.loc[:,'Vel_20NORTE_Avg'].iloc[j+1] or new.loc[:,'Vel_60NORTE_Avg'].iloc[j+1] < new.loc[:,'Vel_40NORTE_Avg'].iloc[j+1] :
                                start.append(i)
                        else:
                            string = str(i) + ' Dato anómalo'
                            anomalos.append(str(i))
                            print(string)
                            del string
                    elif i + dt.timedelta(minutes=10) == dates[j+1] and new.loc[:,'Vel_60NORTE_Avg'].iloc[j+1] > 0.4 :
                        if new.loc[:,'Vel_60NORTE_Avg'].iloc[j+1] < new.loc[:,'Vel_20NORTE_Avg'].iloc[j+1] or new.loc[:,'Vel_60NORTE_Avg'].iloc[j+1] < new.loc[:,'Vel_40NORTE_Avg'].iloc[j+1] :
                            start.append(i)
                        elif i - dt.timedelta(minutes=10) == dates[j-1] and new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1]> 0.4:
                            if new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1] < new.loc[:,'Vel_20NORTE_Avg'].iloc[j-1] or new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1] < new.loc[:,'Vel_40NORTE_Avg'].iloc[j-1]: 
                                end.append(i)
                                if len(start) > 6 :
                                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' datos anómalos'
                                    anomalos.append(str(start[0]) + ' a ' + str(end[0]))
                                    print(string)
                                    start = []
                                    end = []
                                    del string
                                else:
                                    start = []
                                    end = []
                        else:
                            string = str(i) + ' Dato anómalo'
                            anomalos.append(str(i))
                            print(string)
                            del string
                    elif  i - dt.timedelta(minutes=10) == dates[j-1] and new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1]> 0.4: 
                        if new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1] < new.loc[:,'Vel_20NORTE_Avg'].iloc[j-1] or new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1] < new.loc[:,'Vel_40NORTE_Avg'].iloc[j-1]:
                            try:
                                end.append(i)
                                if len(start) > 6 :
                                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' datos anómalos'
                                    anomalos.append(str(start[0]) + ' a ' + str(end[0]))
                                    print(string)
                                    start = []
                                    end = []
                                    del string
                                else:
                                    start = []
                                    end = []
                            except IndexError:
                                print(str(i) + ' error en índice')
                    else:
                        string = str(i) + ' Dato anómalo'
                        anomalos.append(str(i))
                        print(string)
                        del string
            elif j == idx -1: 
                if new.loc[:,'Vel_60NORTE_Avg'].loc[i] < new.loc[:,'Vel_20NORTE_Avg'].loc[i] or new.loc[:,'Vel_60NORTE_Avg'].loc[i] < new.loc[:,'Vel_40NORTE_Avg'].loc[i] :
                    if i - dt.timedelta(minutes=10) != dates[j-1] and new.loc[:,'Vel_60NORTE_Avg'].iloc[j-1]> 0.4:
                        print(str(i) + ' Dato anómalo')
                    else:
                        end.append(i)
                        if len(start) > 6 :
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' datos anómalos'
                            anomalos.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                        else:
                            start = []
                            end = [] 
                elif pd.isna(new.loc[:,'Vel_60NORTE_Avg'].loc[i]) == True:
                    print('Sin medición')
    tabla.append(fechas)
    tabla.append(anomalos)
    tabla.append(no_representativos)
    tabla.append(vacio)
    return tabla


# In[18]:


def Velocidad40N(var):
    no_representativos = []
    anomalos = []
    vacio = []
    fechas = []
    tabla = []
    new = var
    start = []
    end = []
    j = -1
    idx = len(new.index)
    headers = list(new.T.index)
    dates = new.index
    for i in dates:
        j = j+1
        if new.loc[:,'Vel_40NORTE_Avg'].loc[i] < 0.4:
            fechas.append(str(i))
            if j < idx - 1 :
                if j==0:
                    if i + dt.timedelta(minutes=10) == dates[j+1] :
                        if new.loc[:,'Vel_40NORTE_Avg'].iloc[j+1] < 0.4 :
                            start.append(i)
                    else: 
                        string = str(i) + ' no representativo'
                        print(string)
                        no_representativos.append(str(i))
                        del string
                elif i + dt.timedelta(minutes=10) == dates[j+1] :
                    if new.loc[:,'Vel_40NORTE_Avg'].iloc[j+1] < 0.4 :
                        start.append(i)
                    elif i - dt.timedelta(minutes=10) == dates[j-1]:
                        if new.loc[:,'Vel_40NORTE_Avg'].iloc[j-1] < 0.4:
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                            no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' no representativo'
                        no_representativos.append(str(i))
                        print(string)
                        del string
                elif  i - dt.timedelta(minutes=10) == dates[j-1]: 
                    if new.loc[:,'Vel_40NORTE_Avg'].iloc[j-1] < 0.4 :
                        end.append(i)
                        string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                        no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                        print(string)
                        del string
                        start = []
                        end = []
                else:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
            elif j == idx -1:
                if i - dt.timedelta(minutes=10) != dates[j-1]:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
                else:
                    end.append(i)
                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                    no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                    print(string)
                    start = []
                    end = []
                    del string
        elif ('Vel_20NORTE_Avg' in list(headers)) == True :
            fechas.append(str(i))
            if j < idx - 1 :
                if pd.isna(new.loc[:,'Vel_40NORTE_Avg'].loc[i]) == True:
                    if j==0:
                        if i + dt.timedelta(minutes=10) == dates[j+1]:
                            if pd.isna(new.loc[:,'Vel_40NORTE_Avg'].iloc[j+1]) == True :
                                start.append(i)
                        else:
                            string = str(i) + ' Sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif i + dt.timedelta(minutes=10) == dates[j+1]:
                        if pd.isna(new.loc[:,'Vel_40NORTE_Avg'].iloc[j+1]) == True :
                            start.append(i)
                        elif i - dt.timedelta(minutes=10) == dates[j-1]:
                            if pd.isna(new.loc[:,'Vel_40NORTE_Avg'].iloc[j-1]) == True:
                                end.append(i)
                                string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                                vacio.append(str(start[0]) + ' a ' + str(end[0]))
                                print(string)
                                start = []
                                end = []
                                del string
                        else:
                            string = str(i) + ' sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif  i - dt.timedelta(minutes=10) == dates[j-1] : 
                        if pd.isna(new.loc[:,'Vel_40NORTE_Avg'].iloc[j-1]) == True :
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                            vacio.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' sin dato'
                        print(str(i) + ' sin dato')
                        vacio.append(str(i))
                        del string
                elif new.loc[:,'Vel_40NORTE_Avg'].loc[i] < new.loc[:,'Vel_20NORTE_Avg'].loc[i] :
                    if j==0:
                        if i + dt.timedelta(minutes=10) == dates[j+1] and new.loc[:,'Vel_40NORTE_Avg'].iloc[j+1] > 0.4 :
                            if new.loc[:,'Vel_40NORTE_Avg'].iloc[j+1] < new.loc[:,'Vel_20NORTE_Avg'].iloc[j+1] :
                                start.append(i)
                        else:
                            string = str(i) + ' Dato anómalo'
                            anomalos.append(str(i))
                            print(string)
                            del string
                    elif i + dt.timedelta(minutes=10) == dates[j+1] and new.loc[:,'Vel_40NORTE_Avg'].iloc[j+1] > 0.4 :
                        if new.loc[:,'Vel_40NORTE_Avg'].iloc[j+1] < new.loc[:,'Vel_20NORTE_Avg'].iloc[j+1] :
                            start.append(i)
                        elif i - dt.timedelta(minutes=10) == dates[j-1] and new.loc[:,'Vel_40NORTE_Avg'].iloc[j-1]> 0.4:
                            if new.loc[:,'Vel_40NORTE_Avg'].iloc[j-1] < new.loc[:,'Vel_20NORTE_Avg'].iloc[j-1]: 
                                end.append(i)
                                if len(start) > 6 :
                                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' datos anómalos'
                                    anomalos.append(str(start[0]) + ' a ' + str(end[0]))
                                    print(string)
                                    start = []
                                    end = []
                                    del string
                                else:
                                    start = []
                                    end = []
                        else:
                            string = str(i) + ' Dato anómalo'
                            anomalos.append(str(i))
                            print(string)
                            del string
                    elif  i - dt.timedelta(minutes=10) == dates[j-1] and new.loc[:,'Vel_40NORTE_Avg'].iloc[j-1]> 0.4: 
                        if new.loc[:,'Vel_40NORTE_Avg'].iloc[j-1] < new.loc[:,'Vel_20NORTE_Avg'].iloc[j-1]:
                            try:
                                end.append(i)
                                if len(start) > 6 :
                                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' datos anómalos'
                                    anomalos.append(str(start[0]) + ' a ' + str(end[0]))
                                    print(string)
                                    start = []
                                    end = []
                                    del string
                                else:
                                    start = []
                                    end = []
                            except IndexError:
                                print(str(i) + ' error en índice')
                    else:
                        string = str(i) + ' Dato anómalo'
                        anomalos.append(str(i))
                        print(string)
                        del string
            elif j == idx -1: 
                if new.loc[:,'Vel_40NORTE_Avg'].loc[i] < new.loc[:,'Vel_20NORTE_Avg'].loc[i] :
                    if i - dt.timedelta(minutes=10) != dates[j-1] and new.loc[:,'Vel_40NORTE_Avg'].iloc[j-1]> 0.4:
                        print(str(i) + ' Dato anómalo')
                    else:
                        end.append(i)
                        if len(start) > 6 :
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' datos anómalos'
                            anomalos.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                        else:
                            start = []
                            end = [] 
                elif pd.isna(new.loc[:,'Vel_40NORTE_Avg'].loc[i]) == True:
                    print('Sin medición')
    tabla.append(fechas)
    tabla.append(anomalos)
    tabla.append(no_representativos)
    tabla.append(vacio)
    return tabla


# In[19]:


def Velocidad40S(var):
    no_representativos = []
    anomalos = []
    vacio = []
    fechas = []
    tabla = []
    new = var
    start = []
    end = []
    j = -1
    idx = len(new.index)
    headers = list(new.T.index)
    dates = new.index
    for i in dates:
        j = j+1
        if new.loc[:,'Vel_40SUR_Avg'].loc[i] < 0.4:
            fechas.append(str(i))
            if j < idx - 1 :
                if j==0:
                    if i + dt.timedelta(minutes=10) == dates[j+1] :
                        if new.loc[:,'Vel_40SUR_Avg'].iloc[j+1] < 0.4 :
                            start.append(i)
                    else: 
                        string = str(i) + ' no representativo'
                        print(string)
                        no_representativos.append(str(i))
                        del string
                elif i + dt.timedelta(minutes=10) == dates[j+1] :
                    if new.loc[:,'Vel_40SUR_Avg'].iloc[j+1] < 0.4 :
                        start.append(i)
                    elif i - dt.timedelta(minutes=10) == dates[j-1]:
                        if new.loc[:,'Vel_40SUR_Avg'].iloc[j-1] < 0.4:
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                            no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' no representativo'
                        no_representativos.append(str(i))
                        print(string)
                        del string
                elif  i - dt.timedelta(minutes=10) == dates[j-1]: 
                    if new.loc[:,'Vel_40SUR_Avg'].iloc[j-1] < 0.4 :
                        end.append(i)
                        string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                        no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                        print(string)
                        del string
                        start = []
                        end = []
                else:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
            elif j == idx -1:
                if i - dt.timedelta(minutes=10) != dates[j-1]:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
                else:
                    end.append(i)
                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                    no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                    print(string)
                    start = []
                    end = []
                    del string
        elif ('Vel_20NORTE_Avg' in list(headers)) == True :
            fechas.append(str(i))
            if j < idx - 1 :
                if pd.isna(new.loc[:,'Vel_40SUR_Avg'].loc[i]) == True:
                    if j==0:
                        if i + dt.timedelta(minutes=10) == dates[j+1]:
                            if pd.isna(new.loc[:,'Vel_40SUR_Avg'].iloc[j+1]) == True :
                                start.append(i)
                        else:
                            string = str(i) + ' Sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif i + dt.timedelta(minutes=10) == dates[j+1]:
                        if pd.isna(new.loc[:,'Vel_40SUR_Avg'].iloc[j+1]) == True :
                            start.append(i)
                        elif i - dt.timedelta(minutes=10) == dates[j-1]:
                            if pd.isna(new.loc[:,'Vel_40SUR_Avg'].iloc[j-1]) == True:
                                end.append(i)
                                string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                                vacio.append(str(start[0]) + ' a ' + str(end[0]))
                                print(string)
                                start = []
                                end = []
                                del string
                        else:
                            string = str(i) + ' sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif  i - dt.timedelta(minutes=10) == dates[j-1] : 
                        if pd.isna(new.loc[:,'Vel_40SUR_Avg'].iloc[j-1]) == True :
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                            vacio.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' sin dato'
                        print(str(i) + ' sin dato')
                        vacio.append(str(i))
                        del string
                elif new.loc[:,'Vel_40SUR_Avg'].loc[i] < new.loc[:,'Vel_20NORTE_Avg'].loc[i] :
                    if j==0:
                        if i + dt.timedelta(minutes=10) == dates[j+1] and new.loc[:,'Vel_40SUR_Avg'].iloc[j+1] > 0.4 :
                            if new.loc[:,'Vel_40SUR_Avg'].iloc[j+1] < new.loc[:,'Vel_20NORTE_Avg'].iloc[j+1] :
                                start.append(i)
                        else:
                            string = str(i) + ' Dato anómalo'
                            anomalos.append(str(i))
                            print(string)
                            del string
                    elif i + dt.timedelta(minutes=10) == dates[j+1] and new.loc[:,'Vel_40SUR_Avg'].iloc[j+1] > 0.4 :
                        if new.loc[:,'Vel_40SUR_Avg'].iloc[j+1] < new.loc[:,'Vel_20NORTE_Avg'].iloc[j+1] :
                            start.append(i)
                        elif i - dt.timedelta(minutes=10) == dates[j-1] and new.loc[:,'Vel_40SUR_Avg'].iloc[j-1]> 0.4:
                            if new.loc[:,'Vel_40SUR_Avg'].iloc[j-1] < new.loc[:,'Vel_20NORTE_Avg'].iloc[j-1]: 
                                end.append(i)
                                if len(start) > 6 :
                                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' datos anómalos'
                                    anomalos.append(str(start[0]) + ' a ' + str(end[0]))
                                    print(string)
                                    start = []
                                    end = []
                                    del string
                                else:
                                    start = []
                                    end = []
                        else:
                            string = str(i) + ' Dato anómalo'
                            anomalos.append(str(i))
                            print(string)
                            del string
                    elif  i - dt.timedelta(minutes=10) == dates[j-1] and new.loc[:,'Vel_40SUR_Avg'].iloc[j-1]> 0.4: 
                        if new.loc[:,'Vel_40SUR_Avg'].iloc[j-1] < new.loc[:,'Vel_20NORTE_Avg'].iloc[j-1]:
                            try:
                                end.append(i)
                                if len(start) > 6 :
                                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' datos anómalos'
                                    anomalos.append(str(start[0]) + ' a ' + str(end[0]))
                                    print(string)
                                    start = []
                                    end = []
                                    del string
                                else:
                                    start = []
                                    end = []
                            except IndexError:
                                print(str(i) + ' error en índice')
                    else:
                        string = str(i) + ' Dato anómalo'
                        anomalos.append(str(i))
                        print(string)
                        del string
            elif j == idx -1: 
                if new.loc[:,'Vel_40SUR_Avg'].loc[i] < new.loc[:,'Vel_20NORTE_Avg'].loc[i] :
                    if i - dt.timedelta(minutes=10) != dates[j-1] and new.loc[:,'Vel_40SUR_Avg'].iloc[j-1]> 0.4:
                        print(str(i) + ' Dato anómalo')
                    else:
                        end.append(i)
                        if len(start) > 6 :
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' datos anómalos'
                            anomalos.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                        else:
                            start = []
                            end = [] 
                elif pd.isna(new.loc[:,'Vel_40SUR_Avg'].loc[i]) == True:
                    print('Sin medición')
    tabla.append(fechas)
    tabla.append(anomalos)
    tabla.append(no_representativos)
    tabla.append(vacio)
    return tabla


# In[20]:


def Velocidad20N(var):
    no_representativos = []
    anomalos = []
    vacio = []
    fechas = []
    tabla = []
    new = var
    start = []
    end = []
    j = -1
    idx = len(new.index)
    headers = list(new.T.index)
    dates = new.index
    for i in dates:
        j = j+1
        if new.loc[:,'Vel_20NORTE_Avg'].loc[i] < 0.4:
            fechas.append(str(i))
            if j < idx - 1 :
                if j==0:
                    if i + dt.timedelta(minutes=10) == dates[j+1] :
                        if new.loc[:,'Vel_20NORTE_Avg'].iloc[j+1] < 0.4 :
                            start.append(i)
                    else: 
                        string = str(i) + ' no representativo'
                        print(string)
                        no_representativos.append(str(i))
                        del string
                elif i + dt.timedelta(minutes=10) == dates[j+1] :
                    if new.loc[:,'Vel_20NORTE_Avg'].iloc[j+1] < 0.4 :
                        start.append(i)
                    elif i - dt.timedelta(minutes=10) == dates[j-1]:
                        if new.loc[:,'Vel_20NORTE_Avg'].iloc[j-1] < 0.4:
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                            no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' no representativo'
                        no_representativos.append(str(i))
                        print(string)
                        del string
                elif  i - dt.timedelta(minutes=10) == dates[j-1]: 
                    if new.loc[:,'Vel_20NORTE_Avg'].iloc[j-1] < 0.4 :
                        end.append(i)
                        string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                        no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                        print(string)
                        del string
                        start = []
                        end = []
                else:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
            elif j == idx -1:
                if i - dt.timedelta(minutes=10) != dates[j-1]:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
                else:
                    end.append(i)
                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                    no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                    print(string)
                    start = []
                    end = []
                    del string
        elif ('Vel_20NORTE_Avg' in list(headers)) == True :
            fechas.append(str(i))
            if j < idx - 1 :
                if pd.isna(new.loc[:,'Vel_20NORTE_Avg'].loc[i]) == True:
                    if j==0:
                        if i + dt.timedelta(minutes=10) == dates[j+1]:
                            if pd.isna(new.loc[:,'Vel_20NORTE_Avg'].iloc[j+1]) == True :
                                start.append(i)
                        else:
                            string = str(i) + ' Sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif i + dt.timedelta(minutes=10) == dates[j+1]:
                        if pd.isna(new.loc[:,'Vel_20NORTE_Avg'].iloc[j+1]) == True :
                            start.append(i)
                        elif i - dt.timedelta(minutes=10) == dates[j-1]:
                            if pd.isna(new.loc[:,'Vel_20NORTE_Avg'].iloc[j-1]) == True:
                                end.append(i)
                                string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                                vacio.append(str(start[0]) + ' a ' + str(end[0]))
                                print(string)
                                start = []
                                end = []
                                del string
                        else:
                            string = str(i) + ' sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif  i - dt.timedelta(minutes=10) == dates[j-1] : 
                        if pd.isna(new.loc[:,'Vel_20NORTE_Avg'].iloc[j-1]) == True :
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                            vacio.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' sin dato'
                        print(str(i) + ' sin dato')
                        vacio.append(str(i))
                        del string
    tabla.append(fechas)
    tabla.append(anomalos)
    tabla.append(no_representativos)
    tabla.append(vacio)
    return tabla


# In[21]:


Complete_Data.T.index


# In[23]:


def Temperatura(var):
    no_representativos = []
    anomalos = []
    vacio = []
    fechas = []
    tabla = []
    new = var
    start = []
    end = []
    j = -1
    idx = len(new.index)
    headers = list(new.T.index)
    dates = new.index
    for i in dates:
        j = j+1
        if new.loc[:,'Temperatura_Avg'].loc[i] < 0 or new.loc[:,'Temperatura_Avg'].loc[i] >50:
            fechas.append(str(i))
            if j < idx - 1 :
                if j==0:
                    if i + dt.timedelta(minutes=10) == dates[j+1] :
                        if new.loc[:,'Temperatura_Avg'].iloc[j+1] < 0 or new.loc[:,'Temperatura_Avg'].iloc[j+1] >50 :
                            start.append(i)
                    else: 
                        string = str(i) + ' no representativo'
                        print(string)
                        no_representativos.append(str(i))
                        del string
                elif i + dt.timedelta(minutes=10) == dates[j+1] :
                    if new.loc[:,'Temperatura_Avg'].iloc[j+1] < 0 or new.loc[:,'Temperatura_Avg'].iloc[j+1] >50 :
                        start.append(i)
                    elif i - dt.timedelta(minutes=10) == dates[j-1]:
                        if new.loc[:,'Temperatura_Avg'].iloc[j-1] < 0 or new.loc[:,'Temperatura_Avg'].iloc[j-1] >50:
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                            no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' no representativo'
                        no_representativos.append(str(i))
                        print(string)
                        del string
                elif  i - dt.timedelta(minutes=10) == dates[j-1]: 
                    if new.loc[:,'Temperatura_Avg'].iloc[j-1] < 0 or new.loc[:,'Temperatura_Avg'].iloc[j-1] >50 :
                        end.append(i)
                        string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                        no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                        print(string)
                        del string
                        start = []
                        end = []
                else:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
            elif j == idx -1:
                if i - dt.timedelta(minutes=10) != dates[j-1]:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
                else:
                    end.append(i)
                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                    no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                    print(string)
                    start = []
                    end = []
                    del string
        elif ('Temperatura_Avg' in list(headers)) == True :
            fechas.append(str(i))
            if j < idx - 1 :
                if pd.isna(new.loc[:,'Temperatura_Avg'].loc[i]) == True:
                    if j==0:
                        if i + dt.timedelta(minutes=10) == dates[j+1]:
                            if pd.isna(new.loc[:,'Temperatura_Avg'].iloc[j+1]) == True :
                                start.append(i)
                        else:
                            string = str(i) + ' Sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif i + dt.timedelta(minutes=10) == dates[j+1]:
                        if pd.isna(new.loc[:,'Temperatura_Avg'].iloc[j+1]) == True :
                            start.append(i)
                        elif i - dt.timedelta(minutes=10) == dates[j-1]:
                            if pd.isna(new.loc[:,'Temperatura_Avg'].iloc[j-1]) == True:
                                end.append(i)
                                string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                                vacio.append(str(start[0]) + ' a ' + str(end[0]))
                                print(string)
                                start = []
                                end = []
                                del string
                        else:
                            string = str(i) + ' sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif  i - dt.timedelta(minutes=10) == dates[j-1] : 
                        if pd.isna(new.loc[:,'Temperatura_Avg'].iloc[j-1]) == True :
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                            vacio.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' sin dato'
                        print(str(i) + ' sin dato')
                        vacio.append(str(i))
                        del string
    tabla.append(fechas)
    tabla.append(anomalos)
    tabla.append(no_representativos)
    tabla.append(vacio)
    return tabla


# In[24]:


def Presion(var):
    no_representativos = []
    anomalos = []
    vacio = []
    fechas = []
    tabla = []
    new = var
    start = []
    end = []
    j = -1
    idx = len(new.index)
    headers = list(new.T.index)
    dates = new.index
    for i in dates:
        j = j+1
        if new.loc[:,'Presion_Avg'].loc[i] < 0 or new.loc[:,'Presion_Avg'].loc[i] >1000:
            fechas.append(str(i))
            if j < idx - 1 :
                if j==0:
                    if i + dt.timedelta(minutes=10) == dates[j+1] :
                        if new.loc[:,'Presion_Avg'].iloc[j+1] < 0 or new.loc[:,'Presion_Avg'].iloc[j+1] >1000 :
                            start.append(i)
                    else: 
                        string = str(i) + ' no representativo'
                        print(string)
                        no_representativos.append(str(i))
                        del string
                elif i + dt.timedelta(minutes=10) == dates[j+1] :
                    if new.loc[:,'Presion_Avg'].iloc[j+1] < 0 or new.loc[:,'Presion_Avg'].iloc[j+1] >1000 :
                        start.append(i)
                    elif i - dt.timedelta(minutes=10) == dates[j-1]:
                        if new.loc[:,'Presion_Avg'].iloc[j-1] < 0 or new.loc[:,'Presion_Avg'].iloc[j-1] >1000:
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                            no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' no representativo'
                        no_representativos.append(str(i))
                        print(string)
                        del string
                elif  i - dt.timedelta(minutes=10) == dates[j-1]: 
                    if new.loc[:,'Presion_Avg'].iloc[j-1] < 0 or new.loc[:,'Presion_Avg'].iloc[j-1] >1000 :
                        end.append(i)
                        string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                        no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                        print(string)
                        del string
                        start = []
                        end = []
                else:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
            elif j == idx -1:
                if i - dt.timedelta(minutes=10) != dates[j-1]:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
                else:
                    end.append(i)
                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                    no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                    print(string)
                    start = []
                    end = []
                    del string
        elif ('Presion_Avg' in list(headers)) == True :
            fechas.append(str(i))
            if j < idx - 1 :
                if pd.isna(new.loc[:,'Presion_Avg'].loc[i]) == True:
                    if j==0:
                        if i + dt.timedelta(minutes=10) == dates[j+1]:
                            if pd.isna(new.loc[:,'Presion_Avg'].iloc[j+1]) == True :
                                start.append(i)
                        else:
                            string = str(i) + ' Sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif i + dt.timedelta(minutes=10) == dates[j+1]:
                        if pd.isna(new.loc[:,'Presion_Avg'].iloc[j+1]) == True :
                            start.append(i)
                        elif i - dt.timedelta(minutes=10) == dates[j-1]:
                            if pd.isna(new.loc[:,'Presion_Avg'].iloc[j-1]) == True:
                                end.append(i)
                                string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                                vacio.append(str(start[0]) + ' a ' + str(end[0]))
                                print(string)
                                start = []
                                end = []
                                del string
                        else:
                            string = str(i) + ' sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif  i - dt.timedelta(minutes=10) == dates[j-1] : 
                        if pd.isna(new.loc[:,'Presion_Avg'].iloc[j-1]) == True :
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                            vacio.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' sin dato'
                        print(str(i) + ' sin dato')
                        vacio.append(str(i))
                        del string
    tabla.append(fechas)
    tabla.append(anomalos)
    tabla.append(no_representativos)
    tabla.append(vacio)
    return tabla


# In[25]:


def HumedadRel(var):
    no_representativos = []
    anomalos = []
    vacio = []
    fechas = []
    tabla = []
    new = var
    start = []
    end = []
    j = -1
    idx = len(new.index)
    headers = list(new.T.index)
    dates = new.index
    for i in dates:
        j = j+1
        if new.loc[:,'Humedad_rel_Avg'].loc[i] < 0 or new.loc[:,'Humedad_rel_Avg'].loc[i] >100:
            fechas.append(str(i))
            if j < idx - 1 :
                if j==0:
                    if i + dt.timedelta(minutes=10) == dates[j+1] :
                        if new.loc[:,'Humedad_rel_Avg'].iloc[j+1] < 0 or new.loc[:,'Humedad_rel_Avg'].iloc[j+1] >100 :
                            start.append(i)
                    else: 
                        string = str(i) + ' no representativo'
                        print(string)
                        no_representativos.append(str(i))
                        del string
                elif i + dt.timedelta(minutes=10) == dates[j+1] :
                    if new.loc[:,'Humedad_rel_Avg'].iloc[j+1] < 0 or new.loc[:,'Humedad_rel_Avg'].iloc[j+1] >100 :
                        start.append(i)
                    elif i - dt.timedelta(minutes=10) == dates[j-1]:
                        if new.loc[:,'Humedad_rel_Avg'].iloc[j-1] < 0 or new.loc[:,'Humedad_rel_Avg'].iloc[j-1] >100:
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                            no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' no representativo'
                        no_representativos.append(str(i))
                        print(string)
                        del string
                elif  i - dt.timedelta(minutes=10) == dates[j-1]: 
                    if new.loc[:,'Humedad_rel_Avg'].iloc[j-1] < 0 or new.loc[:,'Humedad_rel_Avg'].iloc[j-1] >100 :
                        end.append(i)
                        string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                        no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                        print(string)
                        del string
                        start = []
                        end = []
                else:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
            elif j == idx -1:
                if i - dt.timedelta(minutes=10) != dates[j-1]:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
                else:
                    end.append(i)
                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                    no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                    print(string)
                    start = []
                    end = []
                    del string
        elif ('Humedad_rel_Avg' in list(headers)) == True :
            fechas.append(str(i))
            if j < idx - 1 :
                if pd.isna(new.loc[:,'Humedad_rel_Avg'].loc[i]) == True:
                    if j==0:
                        if i + dt.timedelta(minutes=10) == dates[j+1]:
                            if pd.isna(new.loc[:,'Humedad_rel_Avg'].iloc[j+1]) == True :
                                start.append(i)
                        else:
                            string = str(i) + ' Sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif i + dt.timedelta(minutes=10) == dates[j+1]:
                        if pd.isna(new.loc[:,'Humedad_rel_Avg'].iloc[j+1]) == True :
                            start.append(i)
                        elif i - dt.timedelta(minutes=10) == dates[j-1]:
                            if pd.isna(new.loc[:,'Humedad_rel_Avg'].iloc[j-1]) == True:
                                end.append(i)
                                string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                                vacio.append(str(start[0]) + ' a ' + str(end[0]))
                                print(string)
                                start = []
                                end = []
                                del string
                        else:
                            string = str(i) + ' sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif  i - dt.timedelta(minutes=10) == dates[j-1] : 
                        if pd.isna(new.loc[:,'Humedad_rel_Avg'].iloc[j-1]) == True :
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                            vacio.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' sin dato'
                        print(str(i) + ' sin dato')
                        vacio.append(str(i))
                        del string
    tabla.append(fechas)
    tabla.append(anomalos)
    tabla.append(no_representativos)
    tabla.append(vacio)
    return tabla


# In[31]:


def Lluvia(var):
    no_representativos = []
    anomalos = []
    vacio = []
    fechas = []
    tabla = []
    new = var
    start = []
    end = []
    j = -1
    idx = len(new.index)
    headers = list(new.T.index)
    dates = new.index
    for i in dates:
        j = j+1
        if new.loc[:,'Lluvia_Tot'].loc[i] < 0 or new.loc[:,'Lluvia_Tot'].loc[i] >500:
            fechas.append(str(i))
            if j < idx - 1 :
                if j==0:
                    if i + dt.timedelta(minutes=10) == dates[j+1] :
                        if new.loc[:,'Lluvia_Tot'].iloc[j+1] < 0 or new.loc[:,'Lluvia_Tot'].iloc[j+1] >500 :
                            start.append(i)
                    else: 
                        string = str(i) + ' no representativo'
                        print(string)
                        no_representativos.append(str(i))
                        del string
                elif i + dt.timedelta(minutes=10) == dates[j+1] :
                    if new.loc[:,'Lluvia_Tot'].iloc[j+1] < 0 or new.loc[:,'Lluvia_Tot'].iloc[j+1] >500 :
                        start.append(i)
                    elif i - dt.timedelta(minutes=10) == dates[j-1]:
                        if new.loc[:,'Lluvia_Tot'].iloc[j-1] < 0 or new.loc[:,'Lluvia_Tot'].iloc[j-1] >500:
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                            no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' no representativo'
                        no_representativos.append(str(i))
                        print(string)
                        del string
                elif  i - dt.timedelta(minutes=10) == dates[j-1]: 
                    if new.loc[:,'Lluvia_Tot'].iloc[j-1] < 0 or new.loc[:,'Lluvia_Tot'].iloc[j-1] >500 :
                        end.append(i)
                        string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                        no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                        print(string)
                        del string
                        start = []
                        end = []
                else:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
            elif j == idx -1:
                if i - dt.timedelta(minutes=10) != dates[j-1]:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
                else:
                    end.append(i)
                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                    no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                    print(string)
                    start = []
                    end = []
                    del string
        elif ('Lluvia_Tot' in list(headers)) == True :
            fechas.append(str(i))
            if j < idx - 1 :
                if pd.isna(new.loc[:,'Lluvia_Tot'].loc[i]) == True:
                    if j==0:
                        if i + dt.timedelta(minutes=10) == dates[j+1]:
                            if pd.isna(new.loc[:,'Lluvia_Tot'].iloc[j+1]) == True :
                                start.append(i)
                        else:
                            string = str(i) + ' Sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif i + dt.timedelta(minutes=10) == dates[j+1]:
                        if pd.isna(new.loc[:,'Lluvia_Tot'].iloc[j+1]) == True :
                            start.append(i)
                        elif i - dt.timedelta(minutes=10) == dates[j-1]:
                            if pd.isna(new.loc[:,'Lluvia_Tot'].iloc[j-1]) == True:
                                end.append(i)
                                string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                                vacio.append(str(start[0]) + ' a ' + str(end[0]))
                                print(string)
                                start = []
                                end = []
                                del string
                        else:
                            string = str(i) + ' sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif  i - dt.timedelta(minutes=10) == dates[j-1] : 
                        if pd.isna(new.loc[:,'Lluvia_Tot'].iloc[j-1]) == True :
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                            vacio.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' sin dato'
                        print(str(i) + ' sin dato')
                        vacio.append(str(i))
                        del string
    tabla.append(fechas)
    tabla.append(anomalos)
    tabla.append(no_representativos)
    tabla.append(vacio)
    return tabla


# In[28]:


def Bateria(var):
    no_representativos = []
    anomalos = []
    vacio = []
    fechas = []
    tabla = []
    new = var
    start = []
    end = []
    j = -1
    idx = len(new.index)
    headers = list(new.T.index)
    dates = new.index
    for i in dates:
        j = j+1
        if new.loc[:,'Tension_bateria_Avg'].loc[i] < 0 or new.loc[:,'Tension_bateria_Avg'].loc[i] >30:
            fechas.append(str(i))
            if j < idx - 1 :
                if j==0:
                    if i + dt.timedelta(minutes=10) == dates[j+1] :
                        if new.loc[:,'Tension_bateria_Avg'].iloc[j+1] < 0 or new.loc[:,'Tension_bateria_Avg'].iloc[j+1] >30 :
                            start.append(i)
                    else: 
                        string = str(i) + ' no representativo'
                        print(string)
                        no_representativos.append(str(i))
                        del string
                elif i + dt.timedelta(minutes=10) == dates[j+1] :
                    if new.loc[:,'Tension_bateria_Avg'].iloc[j+1] < 0 or new.loc[:,'Tension_bateria_Avg'].iloc[j+1] >30 :
                        start.append(i)
                    elif i - dt.timedelta(minutes=10) == dates[j-1]:
                        if new.loc[:,'Tension_bateria_Avg'].iloc[j-1] < 0 or new.loc[:,'Tension_bateria_Avg'].iloc[j-1] >30:
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                            no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' no representativo'
                        no_representativos.append(str(i))
                        print(string)
                        del string
                elif  i - dt.timedelta(minutes=10) == dates[j-1]: 
                    if new.loc[:,'Tension_bateria_Avg'].iloc[j-1] < 0 or new.loc[:,'Tension_bateria_Avg'].iloc[j-1] >30 :
                        end.append(i)
                        string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                        no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                        print(string)
                        del string
                        start = []
                        end = []
                else:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
            elif j == idx -1:
                if i - dt.timedelta(minutes=10) != dates[j-1]:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
                else:
                    end.append(i)
                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                    no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                    print(string)
                    start = []
                    end = []
                    del string
        elif ('Tension_bateria_Avg' in list(headers)) == True :
            fechas.append(str(i))
            if j < idx - 1 :
                if pd.isna(new.loc[:,'Tension_bateria_Avg'].loc[i]) == True:
                    if j==0:
                        if i + dt.timedelta(minutes=10) == dates[j+1]:
                            if pd.isna(new.loc[:,'Tension_bateria_Avg'].iloc[j+1]) == True :
                                start.append(i)
                        else:
                            string = str(i) + ' Sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif i + dt.timedelta(minutes=10) == dates[j+1]:
                        if pd.isna(new.loc[:,'Tension_bateria_Avg'].iloc[j+1]) == True :
                            start.append(i)
                        elif i - dt.timedelta(minutes=10) == dates[j-1]:
                            if pd.isna(new.loc[:,'Tension_bateria_Avg'].iloc[j-1]) == True:
                                end.append(i)
                                string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                                vacio.append(str(start[0]) + ' a ' + str(end[0]))
                                print(string)
                                start = []
                                end = []
                                del string
                        else:
                            string = str(i) + ' sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif  i - dt.timedelta(minutes=10) == dates[j-1] : 
                        if pd.isna(new.loc[:,'Tension_bateria_Avg'].iloc[j-1]) == True :
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                            vacio.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' sin dato'
                        print(str(i) + ' sin dato')
                        vacio.append(str(i))
                        del string
    tabla.append(fechas)
    tabla.append(anomalos)
    tabla.append(no_representativos)
    tabla.append(vacio)
    return tabla


# In[60]:


vel60N = Velocidad60N(Complete_Data)
vel60S = Velocidad60S(Complete_Data)
vel40N = Velocidad40N(Complete_Data)
vel40S = Velocidad40S(Complete_Data)
vel20N = Velocidad20N(Complete_Data)
lluvia = Lluvia(Complete_Data)
temp = Temperatura(Complete_Data)
humid = HumedadRel(Complete_Data)
bateria = Bateria(Complete_Data)
presion = Presion(Complete_Data)


# In[61]:


#Creo DataFrames
vel60N_anom = pd.DataFrame([vel60N[1]], index = ['Anómalos'])
vel60N_norep = pd.DataFrame([vel60N[2]], index = ['No_Representativos'])
vel60N_vaci = pd.DataFrame([vel60N[3]], index = ['Vacios'])
vel60S_anom = pd.DataFrame([vel60S[1]], index = ['Anómalos'])
vel60S_norep = pd.DataFrame([vel60S[2]], index = ['No_Representativos'])
vel60S_vaci = pd.DataFrame([vel60S[3]], index = ['Vacios'])
vel40N_anom = pd.DataFrame([vel40N[1]], index = ['Anómalos'])
vel40N_norep = pd.DataFrame([vel40N[2]], index = ['No_Representativos'])
vel40N_vaci = pd.DataFrame([vel40N[3]], index = ['Vacios'])
vel40S_anom = pd.DataFrame([vel40S[1]], index = ['Anómalos'])
vel40S_norep = pd.DataFrame([vel40S[2]], index = ['No_Representativos'])
vel40S_vaci = pd.DataFrame([vel40S[3]], index = ['Vacios'])
vel20N_anom = pd.DataFrame([vel20N[1]], index = ['Anómalos'])
vel20N_norep = pd.DataFrame([vel20N[2]], index = ['No_Representativos'])
vel20N_vaci = pd.DataFrame([vel20N[3]], index = ['Vacios'])


# In[65]:


vel60N_anom.T.to_csv('vel60N' +'_'+'anomalos', index = False)
vel60N_norep.T.to_csv('vel60N' +'_'+'no_represent', index = False)
vel60N_vaci.T.to_csv('vel60N' +'_'+'vacios', index = False)
vel60S_anom.T.to_csv('vel60S' +'_'+'anomalos', index = False)
vel60S_norep.T.to_csv('vel60S' +'_'+'no_represent', index = False)
vel60S_vaci.T.to_csv('vel60S' +'_'+'vacios', index = False)
vel40N_anom.T.to_csv('vel40N' +'_'+'anomalos', index = False)
vel40N_norep.T.to_csv('vel40N' +'_'+'no_represent', index = False)
vel40N_vaci.T.to_csv('vel40N' +'_'+'vacios', index = False)
vel40S_anom.T.to_csv('vel40S' +'_'+'anomalos', index = False)
vel40S_norep.T.to_csv('vel40S' +'_'+'no_represent', index = False)
vel40S_vaci.T.to_csv('vel40S' +'_'+'vacios', index = False)
vel20N_anom.T.to_csv('vel20N' +'_'+'anomalos', index = False)
vel20N_norep.T.to_csv('vel20N' +'_'+'no_represent', index = False)
vel20N_vaci.T.to_csv('vel20N' +'_'+'vacios', index = False)


def Direccion80(var):
    no_representativos = []
    anomalos = []
    vacio = []
    fechas = []
    tabla = []
    new = var
    start = []
    end = []
    j = -1
    idx = len(new.index)
    headers = list(new.T.index)
    dates = new.index
    for i in dates:
        j = j+1
        if new.loc[:,'Prom_Dir_78.5SUR'].loc[i] < 0 or new.loc[:,'Prom_Dir_78.5SUR'].loc[i] >360:
            fechas.append(str(i))
            if j < idx - 1 :
                if j==0:
                    if i + dt.timedelta(minutes=10) == dates[j+1] :
                        if new.loc[:,'Prom_Dir_78.5SUR'].iloc[j+1] < 0 or new.loc[:,'Prom_Dir_78.5SUR'].iloc[j+1] >360 :
                            start.append(i)
                    else: 
                        string = str(i) + ' no representativo'
                        print(string)
                        no_representativos.append(str(i))
                        del string
                elif i + dt.timedelta(minutes=10) == dates[j+1] :
                    if new.loc[:,'Prom_Dir_78.5SUR'].iloc[j+1] < 0 or new.loc[:,'Prom_Dir_78.5SUR'].iloc[j+1] >360 :
                        start.append(i)
                    elif i - dt.timedelta(minutes=10) == dates[j-1]:
                        if new.loc[:,'Prom_Dir_78.5SUR'].iloc[j-1] < 0 or new.loc[:,'Prom_Dir_78.5SUR'].iloc[j-1] >360:
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                            no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' no representativo'
                        no_representativos.append(str(i))
                        print(string)
                        del string
                elif  i - dt.timedelta(minutes=10) == dates[j-1]: 
                    if new.loc[:,'Prom_Dir_78.5SUR'].iloc[j-1] < 0 or new.loc[:,'Prom_Dir_78.5SUR'].iloc[j-1] >360 :
                        end.append(i)
                        string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                        no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                        print(string)
                        del string
                        start = []
                        end = []
                else:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
            elif j == idx -1:
                if i - dt.timedelta(minutes=10) != dates[j-1]:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
                else:
                    end.append(i)
                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                    no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                    print(string)
                    start = []
                    end = []
                    del string
        elif ('Prom_Dir_78.5SUR' in list(headers)) == True :
            fechas.append(str(i))
            if j < idx - 1 :
                if pd.isna(new.loc[:,'Prom_Dir_78.5SUR'].loc[i]) == True:
                    if j==0:
                        if i + dt.timedelta(minutes=10) == dates[j+1]:
                            if pd.isna(new.loc[:,'Prom_Dir_78.5SUR'].iloc[j+1]) == True :
                                start.append(i)
                        else:
                            string = str(i) + ' Sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif i + dt.timedelta(minutes=10) == dates[j+1]:
                        if pd.isna(new.loc[:,'Prom_Dir_78.5SUR'].iloc[j+1]) == True :
                            start.append(i)
                        elif i - dt.timedelta(minutes=10) == dates[j-1]:
                            if pd.isna(new.loc[:,'Prom_Dir_78.5SUR'].iloc[j-1]) == True:
                                end.append(i)
                                string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                                vacio.append(str(start[0]) + ' a ' + str(end[0]))
                                print(string)
                                start = []
                                end = []
                                del string
                        else:
                            string = str(i) + ' sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif  i - dt.timedelta(minutes=10) == dates[j-1] : 
                        if pd.isna(new.loc[:,'Prom_Dir_78.5SUR'].iloc[j-1]) == True :
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                            vacio.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' sin dato'
                        print(str(i) + ' sin dato')
                        vacio.append(str(i))
                        del string
    tabla.append(fechas)
    tabla.append(anomalos)
    tabla.append(no_representativos)
    tabla.append(vacio)
    return tabla


# In[17]:


def Direccion60(var):
    no_representativos = []
    anomalos = []
    vacio = []
    fechas = []
    tabla = []
    new = var
    start = []
    end = []
    j = -1
    idx = len(new.index)
    headers = list(new.T.index)
    dates = new.index
    for i in dates:
        j = j+1
        if new.loc[:,'Prom_Dir_58.5SUR'].loc[i] < 0 or new.loc[:,'Prom_Dir_58.5SUR'].loc[i] >360:
            fechas.append(str(i))
            if j < idx - 1 :
                if j==0:
                    if i + dt.timedelta(minutes=10) == dates[j+1] :
                        if new.loc[:,'Prom_Dir_58.5SUR'].iloc[j+1] < 0 or new.loc[:,'Prom_Dir_58.5SUR'].iloc[j+1] >360 :
                            start.append(i)
                    else: 
                        string = str(i) + ' no representativo'
                        print(string)
                        no_representativos.append(str(i))
                        del string
                elif i + dt.timedelta(minutes=10) == dates[j+1] :
                    if new.loc[:,'Prom_Dir_58.5SUR'].iloc[j+1] < 0 or new.loc[:,'Prom_Dir_58.5SUR'].iloc[j+1] >360 :
                        start.append(i)
                    elif i - dt.timedelta(minutes=10) == dates[j-1]:
                        if new.loc[:,'Prom_Dir_58.5SUR'].iloc[j-1] < 0 or new.loc[:,'Prom_Dir_58.5SUR'].iloc[j-1] >360:
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                            no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' no representativo'
                        no_representativos.append(str(i))
                        print(string)
                        del string
                elif  i - dt.timedelta(minutes=10) == dates[j-1]: 
                    if new.loc[:,'Prom_Dir_58.5SUR'].iloc[j-1] < 0 or new.loc[:,'Prom_Dir_58.5SUR'].iloc[j-1] >360 :
                        end.append(i)
                        string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                        no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                        print(string)
                        del string
                        start = []
                        end = []
                else:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
            elif j == idx -1:
                if i - dt.timedelta(minutes=10) != dates[j-1]:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
                else:
                    end.append(i)
                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                    no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                    print(string)
                    start = []
                    end = []
                    del string
        elif ('Prom_Dir_58.5SUR' in list(headers)) == True :
            fechas.append(str(i))
            if j < idx - 1 :
                if pd.isna(new.loc[:,'Prom_Dir_58.5SUR'].loc[i]) == True:
                    if j==0:
                        if i + dt.timedelta(minutes=10) == dates[j+1]:
                            if pd.isna(new.loc[:,'Prom_Dir_58.5SUR'].iloc[j+1]) == True :
                                start.append(i)
                        else:
                            string = str(i) + ' Sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif i + dt.timedelta(minutes=10) == dates[j+1]:
                        if pd.isna(new.loc[:,'Prom_Dir_58.5SUR'].iloc[j+1]) == True :
                            start.append(i)
                        elif i - dt.timedelta(minutes=10) == dates[j-1]:
                            if pd.isna(new.loc[:,'Prom_Dir_58.5SUR'].iloc[j-1]) == True:
                                end.append(i)
                                string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                                vacio.append(str(start[0]) + ' a ' + str(end[0]))
                                print(string)
                                start = []
                                end = []
                                del string
                        else:
                            string = str(i) + ' sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif  i - dt.timedelta(minutes=10) == dates[j-1] : 
                        if pd.isna(new.loc[:,'Prom_Dir_58.5SUR'].iloc[j-1]) == True :
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                            vacio.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' sin dato'
                        print(str(i) + ' sin dato')
                        vacio.append(str(i))
                        del string
    tabla.append(fechas)
    tabla.append(anomalos)
    tabla.append(no_representativos)
    tabla.append(vacio)
    return tabla


# In[19]:


def Direccion40(var):
    no_representativos = []
    anomalos = []
    vacio = []
    fechas = []
    tabla = []
    new = var
    start = []
    end = []
    j = -1
    idx = len(new.index)
    headers = list(new.T.index)
    dates = new.index
    for i in dates:
        j = j+1
        if new.loc[:,'Prom_Dir_38.5SUR'].loc[i] < 0 or new.loc[:,'Prom_Dir_38.5SUR'].loc[i] >360:
            fechas.append(str(i))
            if j < idx - 1 :
                if j==0:
                    if i + dt.timedelta(minutes=10) == dates[j+1] :
                        if new.loc[:,'Prom_Dir_38.5SUR'].iloc[j+1] < 0 or new.loc[:,'Prom_Dir_38.5SUR'].iloc[j+1] >360 :
                            start.append(i)
                    else: 
                        string = str(i) + ' no representativo'
                        print(string)
                        no_representativos.append(str(i))
                        del string
                elif i + dt.timedelta(minutes=10) == dates[j+1] :
                    if new.loc[:,'Prom_Dir_38.5SUR'].iloc[j+1] < 0 or new.loc[:,'Prom_Dir_38.5SUR'].iloc[j+1] >360 :
                        start.append(i)
                    elif i - dt.timedelta(minutes=10) == dates[j-1]:
                        if new.loc[:,'Prom_Dir_38.5SUR'].iloc[j-1] < 0 or new.loc[:,'Prom_Dir_38.5SUR'].iloc[j-1] >360:
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                            no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' no representativo'
                        no_representativos.append(str(i))
                        print(string)
                        del string
                elif  i - dt.timedelta(minutes=10) == dates[j-1]: 
                    if new.loc[:,'Prom_Dir_38.5SUR'].iloc[j-1] < 0 or new.loc[:,'Prom_Dir_38.5SUR'].iloc[j-1] >360 :
                        end.append(i)
                        string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                        no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                        print(string)
                        del string
                        start = []
                        end = []
                else:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
            elif j == idx -1:
                if i - dt.timedelta(minutes=10) != dates[j-1]:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
                else:
                    end.append(i)
                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                    no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                    print(string)
                    start = []
                    end = []
                    del string
        elif ('Prom_Dir_38.5SUR' in list(headers)) == True :
            fechas.append(str(i))
            if j < idx - 1 :
                if pd.isna(new.loc[:,'Prom_Dir_38.5SUR'].loc[i]) == True:
                    if j==0:
                        if i + dt.timedelta(minutes=10) == dates[j+1]:
                            if pd.isna(new.loc[:,'Prom_Dir_38.5SUR'].iloc[j+1]) == True :
                                start.append(i)
                        else:
                            string = str(i) + ' Sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif i + dt.timedelta(minutes=10) == dates[j+1]:
                        if pd.isna(new.loc[:,'Prom_Dir_38.5SUR'].iloc[j+1]) == True :
                            start.append(i)
                        elif i - dt.timedelta(minutes=10) == dates[j-1]:
                            if pd.isna(new.loc[:,'Prom_Dir_38.5SUR'].iloc[j-1]) == True:
                                end.append(i)
                                string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                                vacio.append(str(start[0]) + ' a ' + str(end[0]))
                                print(string)
                                start = []
                                end = []
                                del string
                        else:
                            string = str(i) + ' sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif  i - dt.timedelta(minutes=10) == dates[j-1] : 
                        if pd.isna(new.loc[:,'Prom_Dir_38.5SUR'].iloc[j-1]) == True :
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                            vacio.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' sin dato'
                        print(str(i) + ' sin dato')
                        vacio.append(str(i))
                        del string
    tabla.append(fechas)
    tabla.append(anomalos)
    tabla.append(no_representativos)
    tabla.append(vacio)
    return tabla


# In[20]:


def Direccion20(var):
    no_representativos = []
    anomalos = []
    vacio = []
    fechas = []
    tabla = []
    new = var
    start = []
    end = []
    j = -1
    idx = len(new.index)
    headers = list(new.T.index)
    dates = new.index
    for i in dates:
        j = j+1
        if new.loc[:,'Prom_Dir_38SUR'].loc[i] < 0 or new.loc[:,'Prom_Dir_38SUR'].loc[i] >360:
            fechas.append(str(i))
            if j < idx - 1 :
                if j==0:
                    if i + dt.timedelta(minutes=10) == dates[j+1] :
                        if new.loc[:,'Prom_Dir_38SUR'].iloc[j+1] < 0 or new.loc[:,'Prom_Dir_38SUR'].iloc[j+1] >360 :
                            start.append(i)
                    else: 
                        string = str(i) + ' no representativo'
                        print(string)
                        no_representativos.append(str(i))
                        del string
                elif i + dt.timedelta(minutes=10) == dates[j+1] :
                    if new.loc[:,'Prom_Dir_38SUR'].iloc[j+1] < 0 or new.loc[:,'Prom_Dir_38SUR'].iloc[j+1] >360 :
                        start.append(i)
                    elif i - dt.timedelta(minutes=10) == dates[j-1]:
                        if new.loc[:,'Prom_Dir_38SUR'].iloc[j-1] < 0 or new.loc[:,'Prom_Dir_38SUR'].iloc[j-1] >360:
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                            no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' no representativo'
                        no_representativos.append(str(i))
                        print(string)
                        del string
                elif  i - dt.timedelta(minutes=10) == dates[j-1]: 
                    if new.loc[:,'Prom_Dir_38SUR'].iloc[j-1] < 0 or new.loc[:,'Prom_Dir_38SUR'].iloc[j-1] >360 :
                        end.append(i)
                        string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                        no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                        print(string)
                        del string
                        start = []
                        end = []
                else:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
            elif j == idx -1:
                if i - dt.timedelta(minutes=10) != dates[j-1]:
                    string = str(i) + ' no representativo'
                    no_representativos.append(str(i))
                    print(string)
                    del string
                else:
                    end.append(i)
                    string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' no representativos'
                    no_representativos.append(str(start[0]) + ' a ' + str(end[0]))
                    print(string)
                    start = []
                    end = []
                    del string
        elif ('Prom_Dir_38SUR' in list(headers)) == True :
            fechas.append(str(i))
            if j < idx - 1 :
                if pd.isna(new.loc[:,'Prom_Dir_38SUR'].loc[i]) == True:
                    if j==0:
                        if i + dt.timedelta(minutes=10) == dates[j+1]:
                            if pd.isna(new.loc[:,'Prom_Dir_38SUR'].iloc[j+1]) == True :
                                start.append(i)
                        else:
                            string = str(i) + ' Sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif i + dt.timedelta(minutes=10) == dates[j+1]:
                        if pd.isna(new.loc[:,'Prom_Dir_38SUR'].iloc[j+1]) == True :
                            start.append(i)
                        elif i - dt.timedelta(minutes=10) == dates[j-1]:
                            if pd.isna(new.loc[:,'Prom_Dir_38SUR'].iloc[j-1]) == True:
                                end.append(i)
                                string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                                vacio.append(str(start[0]) + ' a ' + str(end[0]))
                                print(string)
                                start = []
                                end = []
                                del string
                        else:
                            string = str(i) + ' sin dato'
                            print(string)
                            vacio.append(str(i))
                            del string
                    elif  i - dt.timedelta(minutes=10) == dates[j-1] : 
                        if pd.isna(new.loc[:,'Prom_Dir_38SUR'].iloc[j-1]) == True :
                            end.append(i)
                            string = 'Desde ' + str(start[0]) + ' hasta ' + str(end[0]) + ' sin datos'
                            vacio.append(str(start[0]) + ' a ' + str(end[0]))
                            print(string)
                            start = []
                            end = []
                            del string
                    else:
                        string = str(i) + ' sin dato'
                        print(str(i) + ' sin dato')
                        vacio.append(str(i))
                        del string
    tabla.append(fechas)
    tabla.append(anomalos)
    tabla.append(no_representativos)
    tabla.append(vacio)
    return tabla


#Se crean las tablas y luego se 

if 'Prom_Dir_38SUR' in Complete_Data.T.index:
    dir20 = Direccion20(Complete_Data)
    dir20_vaci = pd.DataFrame([dir20[3]], index = ['Vacios'])
    dir20_vaci.T.to_csv('dir20' +'_'+'vacios', index = False)
if 'Prom_Dir_38.5SUR' in Complete_Data.T.index:
    dir40 = Direccion40(Complete_Data)
    dir40_vaci = pd.DataFrame([dir40[3]], index = ['Vacios'])
    dir40_vaci.T.to_csv('dir40' +'_'+'vacios', index = False)
if 'Prom_Dir_58.5SUR' in Complete_Data.T.index:
    dir60 = Direccion60(Complete_Data)
    dir60_vaci = pd.DataFrame([dir60[3]], index = ['Vacios'])
    dir60_vaci.T.to_csv('dir60' +'_'+'vacios', index = False)
if 'Prom_Dir_78.5SUR' in Complete_Data.T.index:
    dir80 = Direccion80(Complete_Data)
    dir80_vaci = pd.DataFrame([dir80[3]], index = ['Vacios'])
    dir80_vaci.T.to_csv('dir80' +'_'+'vacios', index = False)


