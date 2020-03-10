def get_point(request):
    # TODO: Validate the point

    # get the point
    point = request.args.get('point', '')

    lat = float(point.split(',')[0])
    lon = float(point.split(',')[1])
    return lat, lon
