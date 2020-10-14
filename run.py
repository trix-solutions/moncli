api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI5MTU5Mjc4LCJ1aWQiOjc4ODIzNjEsImlhZCI6IjIwMTktMTItMjdUMTc6MTk6MTcuMDAwWiIsInBlciI6Im1lOndyaXRlIn0.VIpW-i9_Kv5tkmuTY8PX9hZqmzvJP4cSAit-6PaiqOg'
user_name = 'andrew.shatz@trix.solutions'

from moncli import MondayClient

client = MondayClient(user_name, None, api_key)

item = client.get_items(ids=[700337067])[0]
column_values = item.get_column_values()

file_column = column_values[4]
item.remove_files(file_column)

print('Done')