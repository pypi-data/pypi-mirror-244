from django.apps import AppConfig


class MqttConfig(AppConfig):
    name = "NEMO_mqtt"

    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        from NEMO_mqtt import interlocks  # unused but required import

        pass
