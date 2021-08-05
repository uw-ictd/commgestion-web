import json

from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from web.models import Subscriber, SubscriberUsage


def lookup_user(user_id):
    subscriber = Subscriber.objects.get(pk=user_id)
    return subscriber.display_name


def build_drilldown_information(drilldown_name, drilldown_data):
    return {"name": drilldown_name, "id": drilldown_name, "data": drilldown_data}


def generate_context(from_date=None, to_date=None):
    """Generate a django response context dictionary for the network users view"""
    graph_title = str(_("Use of community data"))

    if from_date and to_date:
        from_date_string = from_date.strftime("%d %b %Y")
        to_date_string = to_date.strftime("%d %b %Y")
        graph_title = "{} {} {} {} {}".format(
            graph_title,
            str(_("between")),
            from_date_string,
            str(_("and")),
            to_date_string,
        )

        usage_data = (
            SubscriberUsage.objects.filter(timestamp__range=[from_date, to_date])
            .values("subscriber")
            .annotate(total_bytes=(Sum("down_bytes") + Sum("up_bytes")))
            .order_by("-total_bytes")
        )  # sums the current row
    else:
        usage_data = (
            SubscriberUsage.objects.values("subscriber")
            .annotate(total_bytes=(Sum("down_bytes") + Sum("up_bytes")))
            .order_by("-total_bytes")
        )  # sums the current row

    # TODO: Do this by the number of users if necessary i.e. limit to 10
    #  users etc...
    max_percent_to_start_merge = 0.75

    toplevel_data = []
    percent_consumed = 0.0
    other_users_aggregated_bytes = 0
    drilldown_data = []

    all_user_total_bytes = sum([usage["total_bytes"] for usage in usage_data])
    if all_user_total_bytes > 0:
        for usage in usage_data:
            if percent_consumed <= max_percent_to_start_merge:
                # Users up to the cutoff percentage appear on their own.
                percent_consumed += float(usage["total_bytes"]) / all_user_total_bytes

                toplevel_data.append(
                    {
                        "name": lookup_user(usage["subscriber"]),
                        "y": usage["total_bytes"],
                    }
                )
            else:
                # All other users are aggregated into an other slice.
                other_users_aggregated_bytes += usage["total_bytes"]
                drilldown_data.append(
                    [lookup_user(usage["subscriber"]), usage["total_bytes"]]
                )

        if other_users_aggregated_bytes > 0:
            toplevel_data.append(
                {
                    "name": str(_("Other (Merged)")),
                    "y": other_users_aggregated_bytes,
                    "drilldown": str(_("Other (Merged)")),
                }
            )

    drilldown_response = build_drilldown_information(
        str(_("Other (Merged)")), drilldown_data
    )

    no_data_error_message = "{} <br/> {}".format(
        str(_("No Data available between the chosen dates.")),
        str(_("Please search for a different time.")),
    )

    return {
        "data": json.dumps(toplevel_data),
        "drilldown": json.dumps(drilldown_response),
        "title": json.dumps(graph_title),
        "errorMessage": json.dumps(no_data_error_message),
    }
