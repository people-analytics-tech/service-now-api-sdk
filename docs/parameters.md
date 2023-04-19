# Parâmetros Request

Parâmetros de request (sysparms no ServiceNow) são valores-chave passados na string de consulta para solicitações GET.

Consulte a documentação da API para obter mais informações sobre isso.

### Parâmetros do cliente

```python

```python
from itsm.sdk import Records

records = Records(table="incident")
records.only("sys_id", "number")
data = records.filter()
```

# Parâmetros

### view(view)
Renderize a resposta de acordo com a visualização da interface do usuário especificada (substituída por sysparm_fields)

Parâmetros: view – view (              ) para operar
