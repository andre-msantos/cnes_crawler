import pandas as pd
import time

#capitais
list_munic = pd.read_csv('capitais.csv')

#munic
#list_munic = pd.read_csv('municipios.csv')

def getDataMunic(codibge):
	#get cod UF
	ufibge = codibge[:2]
	
	#delay to get
	time.sleep(1)
	
	#get data from URL
	url = "http://cnes2.datasus.gov.br/Mod_Ind_Tipo_Leito.asp?VEstado={}&VMun={}".format(ufibge, codibge)
		
	try:
		dfmunic = pd.read_html(url, header=0)[3]
			
		#filter data from beds
		dfmunic = dfmunic[dfmunic.Codigo.str.isdigit()]
	
		#add codibge
		dfmunic.insert(0, 'codibge', codibge)
	except IndexError:
		data = [[codibge, '00', 0, 0, 0, 0]]
		dfmunic = pd.DataFrame(data, columns = ['codibge','Codigo','Descrição','Existente','Sus','Não Sus'])
	
	return dfmunic

dfmerge = pd.DataFrame(columns = ['codibge','Codigo','Descrição','Existente','Sus','Não Sus'])

for codibge in list_munic['codibge']:
	dfmerge = pd.concat( [dfmerge, getDataMunic( str(codibge) )],ignore_index = True )

# convert columns
dfmerge['Existente'] = pd.to_numeric(dfmerge['Existente'])
dfmerge['Sus'] = pd.to_numeric(dfmerge['Existente'])
dfmerge['Não Sus'] = pd.to_numeric(dfmerge['Existente'])

#assumptions normal beds
codes_normal_beds = ['01', '02', '03', '04', '05', '07', '08', '09', '11', '12','13', '14', '15', '16', '31', '32', '33', '34', '35', '36','37', '38', '40', '41', '42', '44', '46', '48', '49', '66','67', '69', '70', '71', '72', '88', '90', '95']

#assumptions ICU beds
codes_icu_beds = ['75','74','76','85','86','83']

#assumptions ICU beds COVID-19
codes_icu_beds_covid = ['51']

#df beds
df_normal_beds = dfmerge[dfmerge.Codigo.isin(codes_normal_beds)]['Existente'].groupby(dfmerge['codibge']).sum().to_frame(name = 'qtd_leitos').reset_index()

#df beds icu
df_icu_beds = dfmerge[dfmerge.Codigo.isin(codes_icu_beds)]['Existente'].groupby(dfmerge['codibge']).sum().to_frame(name = 'qtd_uti').reset_index()

#df beds icu covid
df_icu_beds_covid = dfmerge[dfmerge.Codigo.isin(codes_icu_beds_covid)]['Existente'].groupby(dfmerge['codibge']).sum().to_frame(name = 'qtd_uti_covid').reset_index()

#concat df_normal_beds, df_icu_beds
df_all = pd.merge(df_normal_beds, df_icu_beds, on='codibge', how='outer')

#concat df_all, df_icu_beds_covid
df_all = pd.merge(df_all, df_icu_beds_covid, on='codibge', how='outer')

#replace NaN
df_all.fillna(0, inplace=True)

#save csv
df_all.to_csv('ibgeleitos.csv',index=False)
