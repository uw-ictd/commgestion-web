import json
import datetime
from web.models import Application, Usage, Subscriber
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

LINE_GRAPH_TITLE = _('Data Use (Throughput) vs. Time').__str__()
BAR_CHART_TITLE = _('Data Use (Throughput) per Application').__str__()
PIE_LEFT_TITLE = _('Local Users and Non-Local Users').__str__() 
PIE_RIGHT_TITLE = _('Local Content and Non-Local').__str__()

def get_graph2_data():
    query_set = Application.objects.all()
    data = []
    for x in query_set:
        obj = {
            'name': x.host,
            'y': x.throughput
        }
        data.append(obj)
    return data

def get_graph3_data():
    data3 = []
    localUserSum = Subscriber.objects.filter(is_local=True).count()
    nonLocalSum = Subscriber.objects.all().count() - localUserSum

    data3.append(
        {
            'name': "Locales",
            'y': localUserSum
        }
    )

    data3.append(
        {
            'name': "No Locales",
            'y': nonLocalSum
        }
    )
    return data3

def generate_test_data():
    """ Generate fake data for the network statistics page
    """   
    qs_agg = Usage.objects.values('timestamp').annotate(thrpt = Sum('throughput'))   
    g1_data = []
    for x in qs_agg:
        time = x['timestamp'] #values returns a dictionary
        thru = x['thrpt']
        g1_data.append([time,thru])
    
    data_graph1 = g1_data
 
    data_graph2 = get_graph2_data()

    data_graph3 = get_graph3_data()

    data_graph4 = get_graph3_data()

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
    
    titles = ({
        "graph1": json.dumps(LINE_GRAPH_TITLE),
        "graph2": json.dumps(BAR_CHART_TITLE),
        "graph3": json.dumps(PIE_LEFT_TITLE),
        "graph4": json.dumps(PIE_RIGHT_TITLE)
    })
    

    return {
        'totalUsers': total_users,
        'dataSets': data,
        'rows': row_builder,
        'titleSet': titles
    }