import json
import datetime


def generate_test_data():
    """ Generate fake data for the network statistics page
    """
    data_graph1 = [
        [datetime.datetime(2019, 8, 1, 6, 20), 29.9],
        [datetime.datetime(2019, 8, 1, 6, 21), 71.5],
        [datetime.datetime(2019, 8, 1, 6, 22), 106.4],
        [datetime.datetime(2019, 8, 1, 6, 23), 29.9],
        [datetime.datetime(2019, 8, 1, 6, 24), 71.5],
        [datetime.datetime(2019, 8, 1, 6, 25), 106.4],
        [datetime.datetime(2019, 8, 1, 6, 26), 29.9],
        [datetime.datetime(2019, 8, 1, 6, 27), 71.5],
        [datetime.datetime(2019, 8, 1, 6, 28), 106.4]
    ]

    data_graph2 = [
        {
            'name': "Chrome",
            'y': 62.74,
        },
        {
            'name': "Firefox",
            'y': 10.57,
        },
        {
            'name': "Internet Explorer",
            'y': 7.23,
        },
        {
            'name': "Safari",
            'y': 5.58,
        },
        {
            'name': "Edge",
            'y': 4.02,
        },
        {
            'name': "Opera",
            'y': 1.92,
        },
        {
            'name': "Other",
            'y': 7.62,
        }
    ]

    data_graph3 = [
        {
            'name': "Locales",
            'y': 62,
        },
        {
            'name': "Extranjeros",
            'y': 38,
        },
    ]

    data_graph4 = [
        {
            'name': "Locales",
            'y': 62,
            #'drilldown': "Locales"
        },
        {
            'name': "No Locales",
            'y': 38,
            #'drilldown': "No Locales"
        },
    ]

    # ToDo(frankie0) Pull in actual data from the database helpers.
    # This is the original javascript code copied over below...
    '''um.graphTwoQuery().then(r=> {
        for (let i = 0; i < r.length; i++) {
            let temp = {
                "name": r[i]["dataValues"]["name"],
                "y": r[i]["dataValues"]["y"]
            }
            data_graph2.push(temp);
            //finalArray.push(temp);
            //finalArray.push(JSON.parse(r[i]["dataValues"]));
        }
        console.log("final: " + data_graph2);
    });'''
    # ToDo Need to query for the total users:
    total_users = 1337;

    row_builder = [
        ["thru-vs-time", "thru-by-app"],
        ["graph-3", "graph-4"]
    ]

    def datetime_string_converter(obj):
        if isinstance(obj, datetime.datetime):
            return str(obj)

    data = json.dumps({
        "graph1": json.dumps(data_graph1, default=datetime_string_converter),
        "graph2": json.dumps(data_graph2, default=datetime_string_converter),
        "graph3": json.dumps(data_graph3, default=datetime_string_converter),
        "graph4": json.dumps(data_graph4, default=datetime_string_converter)
    }, default=datetime_string_converter)

    return {
        'totalUsers': total_users,
        'dataSets': data,
        'rows': row_builder,
    }
