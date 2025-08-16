# Web-Scraping---BancoCentral_Balancetes_IFs
Este código tem como objetivo realizar a extração de dados de instituições financeiras disponíveis no site do Banco Central do Brasil.
Os dados obtidos correspondem aos balancetes reportados pelas instituições ao BACEN, através dos CADOCs 4010 e 4016.

O funcionamento do código inclui:

Obtenção dos dados: o script acessa um endpoint do Banco Central que retorna os arquivos correspondentes ao CNPJ da instituição e ao período desejado.

Iteração por instituições e períodos: é possível definir uma lista de instituições financeiras e um intervalo de meses/anos para coleta.

Extração e processamento: os arquivos baixados (normalmente em formato ZIP) são extraídos em memória, processados e convertidos em um formato amigável para análise com pandas.

Salvamento dos dados: os arquivos podem ser armazenados tanto na forma bruta quanto processada, permitindo flexibilidade para análises futuras.

Com essa abordagem, é possível construir um repositório de dados estruturados de balancetes financeiros, pronto para análises, dashboards ou qualquer outra aplicação que exija dados consistentes do BACEN.
