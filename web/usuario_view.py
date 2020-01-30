import json

from web.models import Subscriber, Usage


def generate_test_data():
    usageData = Usage.objects.all()
    data = []
    for usage in usageData:
        data.append(
            {
                'name': usage.get_username(),
                'y': usage.throughput,
            }
        )
    # data = [
    #     {
    #         'name': 'Usuario 1',
    #         'y': 61.41,
    #     }, {
    #         'name': 'Usuario 2',
    #         'y': 11.84
    #     }, {
    #         'name': 'Usuario 3',
    #         'y': 10.85
    #     }, {
    #         'name': 'Usuario 4',
    #         'y': 4.67
    #     }, {
    #         'name': 'Usuario 5',
    #         'y': 4.18
    #     }, {
    #         'name': 'Other',
    #         'y': 7.05
    #     }]
    return {'data': json.dumps(data)}