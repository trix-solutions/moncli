DEFAULT_BOARD_QUERY_FIELDS = [
    'id', 
    'name', 
    'board_folder_id', 
    'board_kind', 
    'description', 
    #'items.id', 
    #'owner.id', 
    'permissions',
    'pos',
    'state']

DEFAULT_ITEM_QUERY_FIELDS = [
    'id',
    'name',
    'board.id',
    'board.name',
    'creator_id',
    'group.id',
    'state',
    'subscribers.id'
]