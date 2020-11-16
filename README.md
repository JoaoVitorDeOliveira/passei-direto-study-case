# Passei Direto Estudo de Caso

Criação da arquitetura de BI em um estudo de caso criado pela Passei Direto.
Fiz toda a arquitetura utilizando ferramentas gratuitas para não expor dados sensíveis nem gastos inesperados.

# Funcionamento
Eu criei uma instância do airflow em nuvem que pode ser acessada por esse link com o fluxo de extração de dados.

https://airflow-etl-manual.herokuapp.com/admin/airflow/tree?dag_id=Passei_Direto

> Quando acessar pela primeira vez pode levar em torno de 20 a 30 segundos para carregar a página pois a máquina pode estar em repouso.

E o DW pode ser conectado usando essas credenciais(ex: DBeaver), ele é limitado por 10 mil linhas, no código eu limito em 500 inserts por dimensão.
```
user = "hkmwrxkewkhzrh",
password = "a8f37ea49b38f2d3d07d853b15ed59e0a7b5edaea657c3450c970dd8b9038a57",
host = "ec2-54-91-178-234.compute-1.amazonaws.com",
port = "5432",
database = "de6eje61ar0ot3"
```
Caso queira trocar para um banco local basta inserir as credencias em ```passei-direto-study-case/src/database_access/postgres_connect.py``` e rodar o DDL na base que se encontra em ```passei-direto-study-case/sql/DDL/```.

Usei como lake o Google Drive, criei uma conta gmail para isso. Caso queiram adicionar dados segue as credenciais.
```
pdcasestudy@gmail.com
passeidireto2020
```


Para rodar a aplicação local basta criar um **ambiente virtual python** e instalar as dependencias com o ```pip```.
```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Tentei integrar um cluster spark do databricks gratuito em nuvem porém sem sucesso, o sparkJob pode ser rodado localmente dentro do ambiente virtual.
```
{SPARK_PATH}/bin/spark-submit /src/spark_job.py
```
Também criei um shell-script local para automatizar os jobs, basta rodar ```./src/automation.sh``` dentro do ambiente virtual.

Por fim subi uma instância do **streamlit** para consumir os dados gerados pelo spark e gerar gráficos e análises.

https://secure-scrubland-89533.herokuapp.com


# Modelagem Lógica e Física do DataWarehouse
Fiz o desenho da modelagem com o programa StarUML, com base nos arquivos transacionais usei uma modelagem SnowFlake separando 
o DataWarehouse em duas áreas, STAGE e Dimensional. 

## Área Stage
![alt text](https://github.com/JoaoVitorDeOliveira/passei-direto-study-case/blob/master/media/MODELO_STAGE.jpg)

## Área Dimensional
![alt text](https://github.com/JoaoVitorDeOliveira/passei-direto-study-case/blob/master/media/MODELO_LOGICO.jpg)

A área de Stage serve para trazer os dados da forma mais "crua" possível para minimizar possíveis falhas na ingestão dos dados
para a tabela, deixar a transformação do lado do DW e diminuir trabalho no banco transacional.

Com os dados salvos na Stage, conseguimos transformar os dados e levar para os modelos dimensionais através de Querys otimizadas usando
Slow Changing Dimension, Casts e Coalesce.

O banco de dados utilizado foi o Postgress instalado em uma EC2 pela Heroku(falo mais sobre eles mais pra frente).

# DataStore
Nesse cenário, eu decidi usar o Google drive como DataLake(para substituir o S3),separando em 3 zonas, **Analitycs** (com dados processados pelo spark para consumo de ferramentas de vizualização ou para Cientistas de Dados), **Raw** (onde chega os dados puros de várias fontes, nesse caso os eventos) e **Transactional** (onde vem os dados transacionais cia CDC ou substituindo o banco transacional).

![alt text](https://github.com/JoaoVitorDeOliveira/passei-direto-study-case/blob/master/media/googledrive_lake.png)



# SparkJob
O Job busca os dados gerados por eventos dos usuários e concatena com os dados do DW para entender o comportamento e buscar insights dos dados, nesse job estou gerando 3 arquivos CSVs e salvando na zona Analitycs do Drive, **country.csv** mostra a quantidade de usuários que estão ou são de outros países e que utilizam a PD, **full.csv** mostra a quantidade de usuários pelo tipo e o ultimo **full.csv** mostra um dataset completo com informações de eventos concatenadas com do transacional.




# Heroku e Airflow
> Quando acessar pela primeira vez pode levar em torno de 20 a 30 segundos para carregar a página pois a máquina pode estar em repouso

Para deixar mais fácil a análise da arquitetura eu usei a plataforma como serviço heroku, eles consedem até 5 aplicações e banco de dados em EC2 gratuitas com o limite de 10 mil registros salvos. Para orquestrar o consumo dos dados e manter atualizado a base estou usando o Airflow.


# Streamlit
Para demonstrar como os dados na zona analitycs podem ser consumidos po ruma possível ferramenta de vizualização ou um cientista, eu estou usando o Streamlit(uma ferramenta open source para análise de dados e publicação web https://www.streamlit.io), nesse caso mostro os países de fora que tiveram mais de 100 acessos em novembro de 2017.
![alt text](https://github.com/JoaoVitorDeOliveira/passei-direto-study-case/blob/master/media/streamlit.png)

