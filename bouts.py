# Abre el archivo de entrada para lectura
import matplotlib.pyplot as plt
import numpy as np
import math
from datetime import datetime, timedelta

#Raton 1,2,3 dias: 0-17:00 1-6120  1-16:55 7047-13028  2-16:52 13184-19333  3-15:30 19863-26534  4-17:00 29054-35174  5-17:00 37694-43814

titulo_grafico= 'Raton 1 Dia 2'
archivo_datos='velocidadraton1.txt'
archivo_salida='raton1dia2.txt'
hora_inicial = "17:00:00"
largo_baudios=500
datos_baudio=300
lista_dato_inicial=[1,7047,13184,19863,29054,37694]
lista_dato_final=[6120,13028,19333,26534,35174,43814]
dato_inicial=lista_dato_inicial[1]
dato_final=lista_dato_final[1]



# Abre el archivo de texto en modo lectura
with open(archivo_datos, "rt") as file:
	f = file.read()
x=np.loadtxt(archivo_datos,unpack=True)


Velocidad_baud = np.zeros(shape=(largo_baudios,datos_baudio))
velocidad_gauss = []
posicion=np.zeros(shape=(largo_baudios))
numero_baud = 1
i = 0
flag_baud = 0

f1 = open (archivo_salida,'w')

#///////////////////////////////CALCULO HORAS DIA//////////////////////////////////////////////////
def sumar_tiempo(hora_inicial, segundos_a_sumar):
    # Convertir la hora inicial en un objeto datetime
    hora_formato = "%H:%M:%S"
    hora_objeto = datetime.strptime(hora_inicial, hora_formato)
    
    # Calcular el delta de tiempo usando los segundos a sumar
    delta_tiempo = timedelta(seconds=segundos_a_sumar)
    
    # Sumar el delta de tiempo a la hora inicial
    nueva_hora = hora_objeto + delta_tiempo
    
    # Si la nueva hora supera las 24 horas, empezar desde 00:00:00
    if nueva_hora >= datetime.strptime("23:59:59", hora_formato):
        nueva_hora -= timedelta(days=1)
    
    # Formatear la nueva hora en formato HH:MM:SS
    nueva_hora_formateada = nueva_hora.strftime(hora_formato)
    
    return nueva_hora_formateada
#//////////////////////////////////////////////////////////////////////////////////////////////////

## <  > []\
#//////////////////////////////ARREGLO DATOS///////////////////////////////////////////////////////
for j in range (1,len(x)):
    if (j<dato_final-dato_inicial):
        j=dato_inicial+j
        
        if x[j] > 2:
            velocidad_gauss.append(x[j])
            Velocidad_baud[numero_baud][i]=x[j]
            posicion[numero_baud]=j-dato_inicial
            i+=1
            flag_baud=0
        if (x[j] < 2) and (flag_baud==0):
            numero_baud+=1
            flag_baud=1
            i=0

#//////////////////////////////////////////////////////////////////////////////////////////////////
k=0
num_datos=0
cantidad_datos = []
horarios = []
suma_velocidad=0
velocidad_promedio=0
velocidad_max=0
duracion=0
indice_hora=0

#velocidad promedio
vel_17 = [0]
vel_18 = [0]
vel_19 = [0]
vel_20 = [0]
vel_21 = [0]
vel_22 = [0]
vel_23 = [0]
vel_24 = [0]
vel_1 = [0]
vel_2 = [0]
vel_3 = [0]
vel_4 = [0]
vel_5 = [0]
vel_6 = [0]
vel_7 = [0]
vel_8 = [0]
velocidad_por_hora=[]


#//////////////////////////////CALCULO Y GUARDO////////////////////////////////////////////////////
plt.figure(figsize=(18, 6))
for baud in range (largo_baudios):
    for datos in Velocidad_baud[baud]:
        if (datos>2):
            suma_velocidad+=datos
            num_datos+=1
        else:
            continue
    if (num_datos>0): 
        cantidad_datos.append(num_datos)
        velocidad_promedio=suma_velocidad/num_datos
        velocidad_max=max(Velocidad_baud[baud])  
        nueva_hora = sumar_tiempo(hora_inicial, posicion[baud]*10)
        if ("17:00:00"<=nueva_hora<="18:00:00"):
            vel_17.append(velocidad_promedio)
        if ("18:00:00"<=nueva_hora<="19:00:00"):
            vel_18.append(velocidad_promedio)
        if ("19:00:00"<=nueva_hora<="20:00:00"):
            vel_19.append(velocidad_promedio)
        if ("20:00:00"<=nueva_hora<="21:00:00"):
            vel_20.append(velocidad_promedio)
        if ("21:00:00"<=nueva_hora<="22:00:00"):
            vel_21.append(velocidad_promedio)
        if ("22:00:00"<=nueva_hora<="23:00:00"):
            vel_22.append(velocidad_promedio)
        if ("23:00:00"<=nueva_hora<="23:59:59"):
            vel_23.append(velocidad_promedio)
        if ("00:00:00"<=nueva_hora<="01:00:00"):
            vel_24.append(velocidad_promedio)
        if ("01:00:00"<=nueva_hora<="02:00:00"):
            vel_1.append(velocidad_promedio)
        if ("02:00:00"<=nueva_hora<="03:00:00"):
            vel_2.append(velocidad_promedio)
        if ("03:00:00"<=nueva_hora<="04:00:00"):
            vel_3.append(velocidad_promedio)
        if ("04:00:00"<=nueva_hora<="05:00:00"):
            vel_4.append(velocidad_promedio)
        if ("05:00:00"<=nueva_hora<="06:00:00"):
            vel_5.append(velocidad_promedio)
        if ("06:00:00"<=nueva_hora<="07:00:00"):
            vel_6.append(velocidad_promedio)
        if ("07:00:00"<=nueva_hora<="08:00:00"):
            vel_7.append(velocidad_promedio)
        if ("08:00:00"<=nueva_hora<="09:00:00"):
            vel_8.append(velocidad_promedio)
        horarios.append(nueva_hora)
        f1.write(str(baud) + "  " + str(num_datos*10) + "  " + str(velocidad_promedio) + "  " + str(velocidad_max)+ "  " + str(nueva_hora)+ "\n")
        
        #//////////////////////////////////GRAFICO/////////////////////////////////////////////////////////
        # Crear una figura y un eje para el gráfico
        #plt.plot(nueva_hora,velocidad_promedio,'go--', linewidth=2)
        bar = plt.bar(nueva_hora, velocidad_promedio, width=num_datos/40, align='center', color='b', alpha= 0.7)
        plt.text(bar[0].get_x() + bar[0].get_width() / 2, bar[0].get_height() /2, str(num_datos), ha='center', va='bottom', color='r')
        # Agregar los valores de num_datos sobre las barras
        num_datos=0
        suma_velocidad=0
        k=k+1

#plt.plot(hora_media,velocidad_media,'go--',linewidth=2)
plt.xlabel('Horario')
plt.ylabel('Velocidad')
plt.title('Velocidad con respecto al Horario: ' + str(titulo_grafico))
plt.xticks(rotation=90, fontsize=9)

#print("Listo")
# Mostrar el gráfico
plt.show()


h=["17:30:00","18:30:00","19:30:00","20:30:00","21:30:00","22:30:00","23:30:00","00:30:00","01:30:00","02:30:00","03:30:00","04:30:00","05:30:00","06:30:00","07:30:00","08:30:00"]
velocidad_por_hora.append(np.mean(vel_17))
velocidad_por_hora.append(np.mean(vel_18))
velocidad_por_hora.append(np.mean(vel_19))
velocidad_por_hora.append(np.mean(vel_20))
velocidad_por_hora.append(np.mean(vel_21))
velocidad_por_hora.append(np.mean(vel_22))
velocidad_por_hora.append(np.mean(vel_23))
velocidad_por_hora.append(np.mean(vel_24))
velocidad_por_hora.append(np.mean(vel_1))
velocidad_por_hora.append(np.mean(vel_2))
velocidad_por_hora.append(np.mean(vel_3))
velocidad_por_hora.append(np.mean(vel_4))
velocidad_por_hora.append(np.mean(vel_5))
velocidad_por_hora.append(np.mean(vel_6))
velocidad_por_hora.append(np.mean(vel_7))
velocidad_por_hora.append(np.mean(vel_8))
plt.figure(figsize=(10, 6))
plt.plot(h[:],velocidad_por_hora[:],'go--', linewidth=2)
plt.xticks(rotation=90, fontsize=9)
plt.show()



numero_iteraciones = dato_final - dato_inicial
horas_del_dia = []

for k in range(1, numero_iteraciones+1):
    hora = sumar_tiempo(hora_inicial, k*10)
    horas_del_dia.append(hora)



media=np.mean(velocidad_gauss)
desviacion_estandar = np.std(velocidad_gauss)

x = np.linspace(min(velocidad_gauss), max(velocidad_gauss), 100)
y = (1 / (desviacion_estandar * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - media) / desviacion_estandar)**2)

# Graficar los datos y la distribución gaussiana
plt.figure(figsize=(10, 6))
plt.plot(x, y)

plt.xlabel('Velocidad Media')
plt.title('Distribución Gaussiana de Velocidad')
plt.grid()
plt.show()