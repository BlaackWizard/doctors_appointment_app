async def paginate(query_function, page: int, limit: int, **filters):
    offset = (page - 1) * limit
    results = await query_function(limit=limit, offset=offset, **filters)
    return results
