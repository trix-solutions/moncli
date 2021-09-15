import moncli
from moncli import client 

api_key_v2="eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjEyMzc0MTI4NCwidWlkIjoyNDUwMTE4NiwiaWFkIjoiMjAyMS0wOS0wOFQwNjoyMTozNC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6OTg1NDUwMSwicmduIjoidXNlMSJ9.KoziMpNNz8bq3VELOf-_SUj_zaAayGE2WCkJX-pOwM8"
moncli.api.api_key = api_key_v2
moncli.api.connection_timeout= 30

boards= client.get_boards()[0]
print(boards)
columns = boards.get_columns()[0]


print(columns)
# print(columns)
x = boards.change_column_title(title='no title 3', column=columns)
