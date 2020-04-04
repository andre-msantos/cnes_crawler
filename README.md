CNES CRAWLER
====
O objetivo deste repositório criar um cralwer para obter dados direto do site do [CNES](http://cnes2.datasus.gov.br/). A disponibilidade dos dados via DBC e CSV possuí um delay em relação as informações mostradas no site do CNES, por isso, para ter a informação mais atualizada foi desenvolvido esse crawler. O output gera utilizado no projeto [COVID-19](https://github.com/andrelnunes/COVID-19)

# Setup para rodar o script
1. Instale python 3.6 ou superior;
2. (Opcional) Crie um ambiente virtual;
3. Instale as dependências com `pip install -r requirements.txt`

Para rodar: `python crawlercnes.py`

[[Codigo]](/crawlercnes.py)

# Premissas
## Códigos IBGE
Existem dois arquivos CSV com os códigos dos municípios para auxiliar no crawler. Um apenas com os códigos IBGE de [capitais](/capitais.csv) e outro com todos os [municípios](/municipios.csv). Para mudar entre eles basta (des)comentar a linha específica que carrega o arquivo.

## Códigos dos tipos de leito
Leitos normais: `'01', '02', '03', '04', '05', '07', '08', '09', '11', '12','13', '14', '15', '16', '31', '32', '33', '34', '35', '36','37', '38', '40', '41', '42', '44', '46', '48', '49', '66','67', '69', '70', '71', '72', '88', '90', '95'`
Leitos UTI: `'75','74','76','85','86','83'`
Leitos UTI Covid: `'51'`

Para alterar esses premissas basta alterar as listas das variáveis `codes_normal_beds`, `codes_icu_beds`, `codes_icu_beds_covid`

# Output
Esse script irá gerar um arquivo com a seguinte estrutura

| codibge | qtd_leitos | qtd_uti | qtd_uti_covid |
|:-------:|:----------:|:-------:|:-------------:|
|  330455 |    11308   |  2457   |      212      |
|  355030 |    21855   |  3507   |       0       |
|  410690 |    3818    |  477    |      167      |

# Fonte dos dados
1. [CNES](http://cnes2.datasus.gov.br/)
