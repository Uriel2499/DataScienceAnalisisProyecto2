import pandas as pd

sldb = pd.read_csv('synergy_logistics_database.csv')

# División de los datos para trabajar por separado las exportaciones y las importaciones

exports = sldb['direction'] == 'Exports'
exports_df = sldb[exports]

imports = sldb['direction'] == 'Imports'
imports_df = sldb[imports]

# Se crean dataframes independientes para cada método de transporte utilizado en exportación

sea_ex = sldb['transport_mode'] == 'Sea'
sea_exports = exports_df[sea_ex]

rail_ex = sldb['transport_mode'] == 'Rail'
rail_exports = exports_df[rail_ex]

road_ex = sldb['transport_mode'] == 'Road'
road_exports = exports_df[road_ex]

air_ex = sldb['transport_mode'] == 'Air'
air_exports = exports_df[air_ex]

# Se crean dataframes independientes para cada método de transporte utilizado en exportación

sea_im = sldb['transport_mode'] == 'Sea'
sea_imports = imports_df[sea_im]

rail_im = sldb['transport_mode'] == 'Rail'
rail_imports = imports_df[rail_im]

road_im = sldb['transport_mode'] == 'Road'
road_imports = imports_df[road_im]

air_im = sldb['transport_mode'] == 'Air'
air_imports = imports_df[air_im]

# Se hacen conteos de la cantidad de ventas por año, exportaciones e importaciones por país y métodos de transporte utilizados en exportación e importación

freq_exports_year = exports_df['year'].value_counts()
freq_imports_year = imports_df['year'].value_counts()

freq_exports_country = exports_df['origin'].value_counts()
freq_imports_country = imports_df['origin'].value_counts()

freq_exports_transport_mode = exports_df['transport_mode'].value_counts()
freq_imports_transport_mode = imports_df['transport_mode'].value_counts()

# Sumatoria del total de ganancias obtenidas para cada método de transporte utilizado en exportación

prof_sea_ex = sea_exports['total_value'].sum()
prof_rail_ex = rail_exports['total_value'].sum()
prof_road_ex = road_exports['total_value'].sum()
prof_air_ex = air_exports['total_value'].sum()
total_ex = prof_sea_ex+prof_rail_ex+prof_road_ex+prof_air_ex

# Sumatoria del total de ganancias obtenidas para cada método de transporte utilizado en importación

prof_sea_im = sea_imports['total_value'].sum()
prof_rail_im = rail_imports['total_value'].sum()
prof_road_im = road_imports['total_value'].sum()
prof_air_im = air_imports['total_value'].sum()
total_im = prof_sea_im + prof_rail_im + prof_road_im + prof_air_im

# Suma del total de ganancias para cada método de transporte

prof_sea = prof_sea_ex + prof_sea_im
prof_rail = prof_rail_ex + prof_rail_im
prof_road = prof_road_ex + prof_road_im
prof_air = prof_air_ex + prof_air_im

# Se ingresa el total de ganancias de cada método de transporte a un diccionario para agruparla de mayor a menor

prof = {'Sea': prof_sea, 'Rail': prof_rail, 'Road': prof_road, 'Air': prof_air}
prof_sorted = sorted(prof.items(), key=lambda x: x[1], reverse=True)

# Separación de las tuplas para la impresión de resultados

place = prof_sorted[0]
second = prof_sorted[1]
third = prof_sorted[2]
fourth = prof_sorted[3]

# Cálculo de los paises pertenecientes el 80% de exportaciones e importaciones

country_value_ex = pd.DataFrame(exports_df.groupby(['origin']).sum())
top_country_value_ex = country_value_ex.sort_values(
    'total_value', ascending=False)
country_value_im = pd.DataFrame(imports_df.groupby(['origin']).sum())
top_country_value_im = country_value_im.sort_values(
    'total_value', ascending=False)
top_country_value_ex['porcentaje'] = (
    country_value_ex['total_value']/country_value_ex['total_value'].sum())*100
top_country_value_ex['acumulado'] = top_country_value_ex.cumsum()['porcentaje']
top_country_value_im['porcentaje'] = (
    country_value_im['total_value']/country_value_im['total_value'].sum())*100
top_country_value_im['acumulado'] = top_country_value_im.cumsum()['porcentaje']
top_percent_80_ex = top_country_value_ex[top_country_value_ex['acumulado'] < 80]
top_percent_80_im = top_country_value_im[top_country_value_im['acumulado'] < 80]
top_percent_80_ex = top_percent_80_ex.drop(['register_id', 'year'], axis=1)
top_percent_80_im = top_percent_80_im.drop(['register_id', 'year'], axis=1)

# Se imprimen los datos deseados

print('\n Exportaciones por año: \n')
print(freq_exports_year)
print('\n Importaciones por año: \n')
print(freq_imports_year)
print('\n Top 10 exportaciones por país: \n')
print(freq_exports_country.head(10))
print('\n Top 10 importaciones por país: \n')
print(freq_imports_country.head(10))
print('\n Métodos de transporte más usados en exportación: \n')
print(freq_exports_transport_mode)
print('\n Métodos de transporte más usados en importación: \n')
print(freq_imports_transport_mode)
print('\n Top del total de ganancias obtenidas por cada método de transporte: \n')
for i in range(0, len(prof_sorted), 1):
    place = prof_sorted[i]
    print(i+1, ". ", place[0], " ", place[1])
print('\n Ganancias totales de exportaciones e importaciones: \n')
print('Exportaciones: ', total_ex)
print('Importaciones: ', total_im)
print('\n Países que representan el 80 por ciento de exportaciones: \n')
print(top_percent_80_ex)
print('\n Países que representan el 80 por ciento de importaciones: \n')
print(top_percent_80_im)
