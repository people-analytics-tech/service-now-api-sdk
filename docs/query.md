# Querying

Exemplo:

```python
from datetime import datetime, timedelta
from people_analytics_itsm_sdk.sdk import Records

records = Records(table="incident")

# Definir intervalo inicial e final
start = datetime(1970, 1, 1)
end = datetime.now() - timedelta(days=20)

# Consultar registros de incidentes com número começando com 'INC0123', criados entre 1970-01-01 e 20 dias atrás
records.query.field('number').starts_with('INC0123')\
.AND()\
.field('sys_created_on').between(start, end)\
.AND()\
.field('sys_updated_on').order_descending()

data = records.filter()
```

# Query params

### field(field)
Define o campo para operar

Parâmetros: field – field (str) para operar

### order_descending()
Define a ordem decrescente do campo

### order_ascending()
Define a ordem crescente do campo

### starts_with(starts_with)
Adiciona nova condição STARTSWITH

Parâmetros: starts_with – Campo de correspondência começando com o valor fornecido

### ends_with(ends_with)
Adiciona nova condição ENDSWITH

Parâmetros: ends_with – Campo de correspondência que termina com o valor fornecido

### contains(contains)
Adiciona nova condição LIKE

Parâmetros: contém – campo de correspondência contendo o valor fornecido

### not_contains(not_contains)
Adiciona nova condição NOTLIKE

Parâmetros: not_contains – Campo de correspondência não contendo o valor fornecido

### is_empty()
Adiciona nova condição ISEMPTY

### is_not_empty()
Adiciona nova condição ISNOTEMPTY

### equals(data)
Adiciona uma nova condição IN ou = dependendo se uma lista ou string foi fornecida

Parâmetros:
data – string ou lista de valores

Raise:
QueryTypeError: se os dados forem de um tipo inesperado

### not_equals(data)
Adiciona uma nova condição NOT IN ou = dependendo se uma lista ou string foi fornecida

Parâmetros:
data – string ou lista de valores

Raise:
QueryTypeError: se os dados forem de um tipo inesperado

### greater_than(greater_than)
Adiciona nova > condição

Parâmetros:
maior_than – objeto compatível com str ou datetime (naive UTC datetime ou tz-aware datetime)

Raise:
QueryTypeError: se maior_que for de um tipo inesperado

### less_than(less_than)
Adiciona nova < condição

Parâmetros:
less_than – objeto compatível com str ou datetime (naive UTC datetime ou tz-aware datetime)

Raise:
QueryTypeError: se less_than for de um tipo inesperado

### between(start, end)
Adiciona uma nova condição BETWEEN

Parâmetros:
start – objeto compatível com int ou datetime (no fuso horário do usuário SNOW)
end – objeto compatível com int ou datetime (no fuso horário do usuário SNOW)

Raise:
QueryTypeError: se os argumentos inicial ou final forem de um tipo inválido

### AND()
Adiciona um operador and

### OR()
Adiciona um operador or

### NQ()
Adiciona um operador NQ (nova consulta)
