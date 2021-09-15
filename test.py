import moncli
from moncli import client 

api_key_v2="eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjEyMzc0MTI4NCwidWlkIjoyNDUwMTE4NiwiaWFkIjoiMjAyMS0wOS0wOFQwNjoyMTozNC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6OTg1NDUwMSwicmduIjoidXNlMSJ9.KoziMpNNz8bq3VELOf-_SUj_zaAayGE2WCkJX-pOwM8"
moncli.api.api_key = api_key_v2
moncli.api.connection_timeout= 30

boards= client.get_boards()
print(boards[0])
columns = boards[0].get_columns()


print(columns[0])
# print(columns)
x = boards[0].change_column_title('Newest Title 3', columns[0])
print(type(x))