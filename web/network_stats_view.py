import json
import datetime
from web.models import Application, Usage, Subscriber
from django.db.models import Sum
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

LINE_GRAPH_TITLE = _('Data Use (Throughput) vs. Time').__str__()
BAR_CHART_TITLE = _('Data Use (Throughput) per Application').__str__()
PIE_LEFT_TITLE = _('Local Users and Non-Local Users').__str__() 
PIE_RIGHT_TITLE = _('Local Content and Non-Local').__str__()

AXIS_TITLE_LINE = _('Throughput').__str__()
AXIS_TITLE_BAR = _('Throughput').__str__()

UNIT_THRESHOLD = 5000;
UNIT_LINE = "units"
UNIT_BAR = "units2"


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
            'name': str(pgettext_lazy("people from a place", "Locals")),
            'y': localUserSum
        }
    )

    data3.append(
        {
            'name': str(pgettext_lazy("people from outside a place", "Others")),
            'y': nonLocalSum
        }
    )
    return data3


def get_graph4_data():
    data4 = list()
    # TODO(matt9j) This is just a stub, lookup real values

    data4.append(
        {
            'name': _("Local").__str__(),
            'y': 20
        }
    )

    data4.append(
        {
            'name': _("External").__str__(),
            'y': 80
        }
    )
    return data4


def generate_test_data():
    """ Generate fake data for the network statistics page
    """
    #max_th = Usage.objects.all().aggregate(Max('throughput'))
    #print(max_th)
    qs_agg = Usage.objects.values('timestamp').annotate(thrpt = Sum('throughput'))
    print(qs_agg)
    g1_data = []
    max_th = 0
    #BEST WAY TO GET THE MAX SO THAT ALL THE VALUES CAN BE CONVERTED TO MBPS IN THE LOOP
    #IF NEEDED?????? 
    for x in qs_agg:
        time = x['timestamp'] #values returns a dictionary
        thru = x['thrpt']
        g1_data.append([time,thru])
        if(thru > max_th):
            max_th = thru
        #print("max thru ")
        #print(max_th)
            
    data_graph1 = g1_data

    data_graph2 = get_graph2_data()

    data_graph3 = get_graph3_data()

    data_graph4 = get_graph4_data()

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

    labelSet = ({
        "graph1": json.dumps(AXIS_TITLE_LINE),
        "graph2": json.dumps(AXIS_TITLE_BAR)
    })
    
    unit_dict = ({
        'graph1': json.dumps(UNIT_LINE),
        'graph2': json.dumps(UNIT_BAR)
    })

    return {
        'totalUsers': total_users,
        'dataSets': data,
        'rows': row_builder,
        'titleSet': titles,
        'axisLabels': labelSet,
        'unitSet': unit_dict
    }
