Essa é uma API gratuita para consultar informações referentes ao CNPJ de forma automatizada. Por ser gratuita, possui um limite de 3 consultas por minutos.
O código foi ajustado para realizar uma nova consulta a cada minuta até que a lista de CNPJ se esgote. 

O código utiliza dois módulos, para instalar basta digitar os seguintes comandos no terminal:

    pip install requests
    pip install json

Para utilizar essa API você deve passar dois parâmetros ao executar o código.

 1 - O arquivo TXT com a lista de CNPJ **precisa conter um separador**. 
     É muito comum que se utilizem os seguintes separadores: ( **, ; |** )

    Abaixo segue um exemplo de lista com separador -> ponto e virgula ; :
    
      18444923000106;ORTOTRAUMA CLINICA MEDICA LTDA;ORTOTRAUMA;(43) 3546-1226;18.444.923/0001-06;
      18444955000101;;;(43) 3557-2246;18.444.955/0001-01;
      19316524000114;DELTA SHOP - DISTRIBUIDORA DE PRODUTOS HOSPITALARES LTDA;DELTA SHOP;(54) 3523-1104;19.316.524/0001-14;
      19316524000114;DELTA SHOP - DISTRIBUIDORA DE PRODUTOS HOSPITALARES LTDA;DELTA SHOP;(54) 3523-1104;19.316.524/0001-14;
      19660722000109;;;;19.660.722/0001-09;

    Outro exemplo com separador ao final do arquivo -> virgula , :
  
      53531466000180,
      53743518000181,
      53616153000124,
      52027520000191,

  2 - No código, por padrão, a primeira coluna (ou primeiro separador) está definida como CNPJ. Caso o teu relatório tenha outra coluna definida como CNPJ, basta fazer o ajuste nessa parte do código,
  trocando o 0 por outro número de coluna:
  
      0 = primeira coluna --> cnpj = linha.split(sep)[0]
      1 = segunda coluna --> cnpj = linha.split(sep)[1]
      2 = terceira coluna  --> cnpj = linha.split(sep)[2]
      ...
      
  3 - No código, por padrão, as informações que se busca na API da Receita Federal são essas abaixo:
      Você pode ajustar removendo ou adicionando mais informações conforme necessitar.
      
      lista = ['nome', 'fantasia', 'cnpj', 'logradouro', 'numero', 'municipio', 'bairro', 'uf', 'cep', 'email', 'situacao']
      
  4 - Outro ponto importante a se observar é colocar o arquivo com a lista de CNPJ **na mesma pasta** que se encontra o arquivo de execução .py

  5 - Ao final da lista de CNPJ, as informações coletadas serão salvas um arquivo "excel.csv" já tabuladas.

  Espero que lhe seja útil.
