from django.contrib import admin
from django import forms
from django.contrib.admin import register

# NEMO Imports
from NEMO_mqtt.models import MqttInterlockServer, MqttInterlock


class MqttInterlockServerAdminForm(forms.ModelForm):
    class Meta:
        model = MqttInterlockServer
        widgets = {"password": forms.PasswordInput(render_value=True)}
        fields = "__all__"

    # def clean(self):
    #     TODO
    #     if any(self.errors):
    #         return
    #     cleaned_data = super().clean()
    #     category = cleaned_data["category"]
    #     from NEMO import interlocks
    #     interlocks.get(category, False).clean_interlock_card(self)
    #     return cleaned_data


@register(MqttInterlockServer)
class MqttInterlockServerAdmin(admin.ModelAdmin):
    form = MqttInterlockServerAdminForm
    list_display = (
        "get_server_enabled",
        "card",
        "server",
        "port",
        "user",
        "client_id",
        "auth_mode",
        "tls_verify",
    )

    @admin.display(boolean=True, ordering="interlock__card__enabled", description="Server Enabled")
    def get_server_enabled(self, obj):
        return obj.card.enabled


class MqttInterlockAdminForm(forms.ModelForm):
    class Meta:
        model = MqttInterlockServer
        widgets = {"password": forms.PasswordInput(render_value=True)}
        fields = "__all__"

    pass


@register(MqttInterlock)
class MqttInterlockAdmin(admin.ModelAdmin):
    form = MqttInterlockAdminForm
    list_display = (
        "interlock",
        "get_interlock_enabled",
        "command_topic",
        "state_topic",
        "on_payload",
        "off_payload",
        "qos",
        "get_interlock_tool",
        "get_interlock_door",
        "get_interlock_state",
        "get_interlock_most_recent_reply",
    )

    @admin.display(boolean=True, ordering="interlock__card__enabled", description="Server Enabled")
    def get_interlock_enabled(self, obj):
        return obj.interlock.card.enabled

    @admin.display(ordering="interlock__tool", description="Tool")
    def get_interlock_tool(self, obj):
        return obj.interlock.tool

    @admin.display(ordering="interlock__door", description="Door")
    def get_interlock_door(self, obj):
        return obj.interlock.door

    @admin.display(ordering="interlock__state", description="State")
    def get_interlock_state(self, obj):
        return "%s" % obj.interlock.get_state_display()

    @admin.display(ordering="interlock__most_recent_reply", description="Latest reply")
    def get_interlock_most_recent_reply(self, obj):
        return obj.interlock.most_recent_reply
