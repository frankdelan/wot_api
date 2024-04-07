async def filter_tanks(request, tank_list: list):
    idx = 0
    while idx < len(tank_list):
        if request.query_params.get('type') and tank_list[idx].type != request.query_params.get('type'):
            tank_list.pop(idx)
        elif request.query_params.get('nation') and tank_list[idx].country != request.query_params.get('nation'):
            tank_list.pop(idx)
        elif request.query_params.get('level') and tank_list[idx].level != int(request.query_params.get('level')):
            tank_list.pop(idx)
        else:
            idx += 1
    return tank_list
