# FILMES E SÉRIES DE LONGA DURAÇÃO SÃO OS PIORES AVALIADOS

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal as d

from google.colab import drive
drive.mount('/content/drive/')

df = pd.read_csv('/content/drive/My Drive/IMDB/imdb.csv', sep=',')
df.drop(columns=["Certificate",	"Nudity",	"Violence",	"Profanity",
        "Alcohol",	"Frightening", "Name"], axis=1, inplace=True)
df

df['Rate'] = df['Rate'].astype(float)
df.dtypes

coluna = []
duration = []
ep = []


for i in range(len(df['Date'])):
    # ---------- Convertendo Votos de String para Int
    partes = df['Votes'][i].split(',')
    coluna.append(int(''.join(partes)))

    # ---------- Convertendo Duration de String para Int
    if df['Duration'][i].strip() == 'None':
        duration.append(0)
    else:
        duration.append(int(df['Duration'][i].strip()))

    if df['Episodes'][i].strip() == '-':
        ep.append(0)
    else:
        ep.append(int(df['Episodes'][i].strip()))


df['Votes'] = coluna
df['Duration'] = duration
df['Episodes'] = ep
df.dtypes

intervalo = []

for i in range(len(df['Date'])):
    # ---------- Criando uma coluna classificando os intervalos ----------
    if df['Duration'][i] > 0 and df['Duration'][i] <= 60:  # Intervalo 1 = t > 0 e t <= 60
        intervalo.append(1)

    elif df['Duration'][i] > 60 and df['Duration'][i] <= 120:  # Intervalo 2 = t > 60 e t <= 120
        intervalo.append(2)

    elif df['Duration'][i] > 120 and df['Duration'][i] <= 180:  # Intervalo 3 = t > 120 e t <=180
        intervalo.append(3)

    elif df['Duration'][i] > 180 and df['Duration'][i] <= 240:  # Intervalo 4 = t > 180 e t <= 240
        intervalo.append(4)

    else:
        intervalo.append(0)  # Intervalo 0 = Intervalo que não sera trabalhado
df['Interval'] = intervalo

filmes = df[df['Type'] == 'Film']

filmes = filmes[filmes['Rate'] != 0]  # Removendo filmes nao avaliados

series = df[df['Type'] == 'Series']

plt.scatter(series['Episodes'], series['Votes'])
plt.title("Outliers da duração - Series")
plt.xlabel("Duração em Episodios")
plt.ylabel("N Voto")
plt.show()
plt.savefig("outliers_da_duracao_series.png", dpi=200)


series = df[df['Type'] == 'Series']
# Cortando da tabela as series com mais de 2000 episodios
series = series[series['Episodes'] <= 2000]

series = series[series['Rate'] != 0]

filmes.reset_index(inplace=True)
filmes.drop('index', axis=1, inplace=True)

series.reset_index(inplace=True)
series.drop('index', axis=1, inplace=True)

SGenero = {}

for i in range(len(series['Date'])):
    for x in series['Genre'][i].split(','):
        if SGenero.get(x.strip()):
            SGenero[x.strip()][0] += 1
            SGenero[x.strip()][1] += series['Rate'][i]
        else:
            SGenero[x.strip()] = [1, series['Rate'][i]]
# print(SGenero)

FGenero = {}

for i in range(len(filmes['Date'])):
    for x in filmes['Genre'][i].split(','):
        if FGenero.get(x.strip()):
            FGenero[x.strip()][0] += 1
            FGenero[x.strip()][1] += filmes['Rate'][i]
        else:
            FGenero[x.strip()] = [1, filmes['Rate'][i]]
# print(FGenero)
for genero, lista in SGenero.items():
    SGenero[genero].append(lista[1]/lista[0])

for genero, lista in FGenero.items():
    FGenero[genero].append(lista[1]/lista[0])
print(FGenero)
print(SGenero)

xF = []
rotulos = []
maior_rotulo = []
maior_xF = []
for genero, lista in FGenero.items():
    if lista[0] >= 100:
        rotulos.append(genero)
        xF.append(lista[2])
# print(rotulos)
for i in range(5):
    maior_xF.append(max(xF))
    maior_rotulo.append(rotulos[xF.index(max(xF))])
    rotulos.pop(rotulos.index(maior_rotulo[i]))
    xF.pop(xF.index(max(xF)))
minimoX = []
minimoRotulo = []
minimoX.append(min(xF))
minimoRotulo.append(rotulos[xF.index(min(xF))])
print(maior_rotulo)
print(maior_xF)
plt.title("Generos Com Melhores Medias de Avaliação - Filmes")
plt.bar(maior_rotulo, maior_xF, label="Maiores")
plt.bar(minimoRotulo, minimoX, label='Menor')
plt.legend()
plt.ylim([1, 9])
plt.show()
print(FGenero)
# Os cinco generos com melhores medias de avaliação, e a pior media

xF = []
rotulos = []
maior_rotulo = []
maior_xF = []
for genero, lista in SGenero.items():
    if lista[0] >= 100:
        rotulos.append(genero)
        xF.append(lista[2])
# print(rotulos)

for i in range(5):
    maior_xF.append(max(xF))
    maior_rotulo.append(rotulos[xF.index(max(xF))])
    rotulos.pop(rotulos.index(maior_rotulo[i]))
    xF.pop(xF.index(max(xF)))
minimoX = []
minimoRotulo = []
minimoX.append(min(xF))
minimoRotulo.append(rotulos[xF.index(min(xF))])


print(maior_rotulo)
print(maior_xF)

plt.title("Generos Com Melhores Medias de Avaliação - Series")
plt.bar(maior_rotulo, maior_xF, label="Maiores")
plt.bar(minimoRotulo, minimoX, label='Menor')
plt.legend()
plt.ylim([1, 10])
plt.show()
print(FGenero)
# Os cinco generos com melhores medias de avaliação, e a pior media


plt.scatter(filmes['Duration'], filmes['Votes'])
plt.title("Gráfico Random")
plt.xlabel("Duração")
plt.ylabel("N Voto")
plt.show()


plt.scatter(series['Episodes'], series['Votes'])
plt.title("Scatterplot sem Outliers da duração - Series")
plt.xlabel("Duração em Episodios")
plt.ylabel("N Voto")
plt.show()


plt.scatter(series['Votes'], series['Rate'])
plt.title("Gráfico Random")
plt.xlabel("N Voto")
plt.ylabel("Rate")
plt.show()


# Lista com sublistas para cada intervalo sendo [n1, n2], n1 é a soma das avaliações e o n2 é a contagem
ilm_mean_interv = [[0, 0], [0, 0], [0, 0], [0, 0]]
for i in range(len(filmes['Rate'])):
    if filmes['Interval'][i] == 1:
        film_mean_interv[0][0] += d(str(filmes['Rate'][i]))
        film_mean_interv[0][1] += 1
    elif filmes['Interval'][i] == 2:
        film_mean_interv[1][0] += d(str(filmes['Rate'][i]))
        film_mean_interv[1][1] += 1
    elif filmes['Interval'][i] == 3:
        film_mean_interv[2][0] += d(str(filmes['Rate'][i]))
        film_mean_interv[2][1] += 1
    elif filmes['Interval'][i] == 4:
        film_mean_interv[3][0] += d(str(filmes['Rate'][i]))
        film_mean_interv[3][1] += 1
for i in range(len(film_mean_interv)):
    # Adiciona um terceiro elemento da sublista do intervalo,
    film_mean_interv[i].append(film_mean_interv[i][0]/film_mean_interv[i][1])

print(f'''Media intervalo 1: {film_mean_interv[0][2]}
Media intervalo 2: {film_mean_interv[1][2]}
Media intervalo 3: {film_mean_interv[2][2]}
Media intervalo 4: {film_mean_interv[3][2]}''')
plt.title("Media de Avaliação por Intervalo - Filmes")
plt.xlabel("Duração em Minutos")
plt.ylabel("Avaliação")
plt.bar(['1 a 60', '61 a 120', '121 a 180', '181 a 240'], [film_mean_interv[0]
        [2], film_mean_interv[1][2], film_mean_interv[2][2], film_mean_interv[3][2]])
plt.show()


intervalo = []

for i in range(len(series['Date'])):
    # ---------- Criando uma coluna classificando os intervalos ----------
    # Intervalo 1 = ep > 0 e ep <= 500
    if series['Episodes'][i] > 0 and series['Episodes'][i] <= 500:
        intervalo.append(1)

    # Intervalo 2 = ep > 500 e ep <= 1000
    elif series['Episodes'][i] > 500 and series['Episodes'][i] <= 1000:
        intervalo.append(2)

    # Intervalo 3 = ep > 1000 e ep <=1500
    elif series['Episodes'][i] > 1000 and series['Episodes'][i] <= 1500:
        intervalo.append(3)

    # Intervalo 4 = ep > 1500 e t <= 2000
    elif series['Episodes'][i] > 1500 and series['Episodes'][i] <= 2000:
        intervalo.append(4)

    else:
        intervalo.append(0)  # Intervalo 0 = Intervalo que não sera trabalhado
series['Interval'] = intervalo


series_mean_interv = [[], [], [], []]
for i in range(len(series['Rate'])):
    if series['Interval'][i] == 1:
        series_mean_interv[0].append(series['Rate'][i])
    elif series['Interval'][i] == 2:
        series_mean_interv[1].append(series['Rate'][i])
    elif series['Interval'][i] == 3:
        series_mean_interv[2].append(series['Rate'][i])
    elif series['Interval'][i] == 4:
        series_mean_interv[3].append(series['Rate'][i])

print(f'''Media intervalo 1: {sum(series_mean_interv[0])/len(series_mean_interv[0])}
Media intervalo 2: {sum(series_mean_interv[1])/len(series_mean_interv[1])}
Media intervalo 3: {sum(series_mean_interv[2])/len(series_mean_interv[2])}
Media intervalo 4: {sum(series_mean_interv[3])/len(series_mean_interv[3])}''')
plt.title("Media de Avaliação por Intervalo - Séries")
plt.xlabel("Quantidade de Episodios")
plt.ylabel("Avaliação")
plt.bar(['1 a 500', '501 a 1000', '1001 a 1500', '1501 a 2000'], [sum(series_mean_interv[0])/len(series_mean_interv[0]), sum(series_mean_interv[1]) /
        len(series_mean_interv[1]), sum(series_mean_interv[2])/len(series_mean_interv[2]), sum(series_mean_interv[3])/len(series_mean_interv[3])])
plt.show()


filmes.corr()
# Correlação entre os dados da tabela Filmes

series.corr()
# Correlação entre os dados da tabela Filmes

series.dtypes
series.describe()
series['Date'].mode()
# NÃO TEMOS VALORES NaN a moda da Series não sabemos oque aconteceu
series.isnull().sum()
