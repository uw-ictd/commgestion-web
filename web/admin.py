from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from .models import HostUsage, Subscriber, UserDefinedHost, HostMapping, SubscriberUsage

admin.site.site_header = 'Community Cellular Admin'  # Updates the written text
admin.site.index_title = 'Community Cellular'  # Tab Title content
admin.site.site_title = 'Application Administration Panel'  # Tab title | sub_title


@admin.register(HostUsage)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('host', 'total_kbytes', 'timestamp')


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('user', 'msisdn', 'display_name', 'imsi', 'is_local', 'role', 'authorization_status',
                    'last_time_online', 'rate_limit_kbps', 'equipment', 'created', 'subscription_date', 'subscription_status')


@admin.register(UserDefinedHost)
class UserDefinedHostAdmin(admin.ModelAdmin):
    list_display = ('name', 'view_user_defined_host')

    @staticmethod
    def view_user_defined_host(self):
        return format_html('<a class="button" target="_blank" href="https://{}">View</a>'.format(self.name))

@admin.register(SubscriberUsage)
class UserAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'total_kbytes', 'timestamp')
    
@admin.register(HostMapping)
class HostMappingAdmin(admin.ModelAdmin):
    list_display = ('host', 'captured_host')

