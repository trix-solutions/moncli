import moncli
from moncli import client, BoardKind
from moncli.enums import SubscriberKind

api_key_v2 = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjEyMzQ5ODIzOCwidWlkIjoyNDEwOTk3NCwiaWFkIjoiMjAyMS0wOS0wNlQxMzo0ODoxMS42NjFaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6OTc3NTAxMCwicmduIjoidXNlMSJ9.dpfLLpz4Q6YZFzUT8ocaN8Le0VamwwuC3mSAb3xtCDw"

# api_key_v2 = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjEyMzc0MTI4NCwidWlkIjoyNDUwMTE4NiwiaWFkIjoiMjAyMS0wOS0wOFQwNjoyMTozNC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6OTg1NDUwMSwicmduIjoidXNlMSJ9.KoziMpNNz8bq3VELOf-_SUj_zaAayGE2WCkJX-pOwM8"
moncli.api.api_key  = api_key_v2
moncli.api.connection_timeout = 30


item = client.get_items(ids=[1636715900], get_column_values=True)

# client.api_key_v2=api_key

# user_id = 24109974#aswathm78@gmail.com
# id2 = 24440647#developer@intelora.co.in
# id3 = 24440701#intelora.dev@intelora.co.in
# id4 = 24441167#aswath.m@intelora.co.in
# workspace_id = "884590"

# user_ids = ["24440647","24440701","24441167"]

# kind = WorkspaceSubscriberKind.subscriber

# result = client.add_users_to_workspace(workspace_id, user_ids, kind )
# print(result)

# 24440647,24440701,24441167

