from django.db import models
from NEMO.models import BaseModel, InterlockCard, Interlock


class MqttInterlockServer(BaseModel):
    REQUIRE = {
        "PASS": 1,
        "TLS": 2,
        "CERT": 4,
    }
    AUTH_MODES = [
        (0, "Anonymous"),
        (REQUIRE["PASS"], "Cleartext User/Pass"),
        (REQUIRE["TLS"], "TLS Anonymous"),
        (REQUIRE["TLS"] + REQUIRE["PASS"], "TLS User/Pass"),
        (REQUIRE["CERT"] + REQUIRE["TLS"], "TLS Certificates"),
        (REQUIRE["CERT"] + REQUIRE["TLS"] + REQUIRE["PASS"], "TLS Certificate with User/Pass"),
    ]
    card = models.OneToOneField(InterlockCard, on_delete=models.CASCADE)
    server = models.CharField(max_length=100, default="", verbose_name="MQTT server address")
    port = models.PositiveIntegerField(verbose_name="MQTT server port")
    user = models.CharField(
        max_length=100, default=None, blank=True, null=True, verbose_name="MQTT Username for authentication"
    )
    password = models.CharField(
        max_length=100, default=None, blank=True, null=True, verbose_name="MQTT Password for authentication"
    )
    client_id = models.CharField(
        max_length=100, default=None, blank=True, null=True, verbose_name="MQTT Client ID for the connection"
    )
    auth_mode = models.PositiveSmallIntegerField(choices=AUTH_MODES, default=0, verbose_name="MQTT Authentication Mode")
    tls_verify = models.BooleanField(default=True, verbose_name="Verify server certificate. Disable only for testing.")
    tls_ca = models.CharField(
        max_length=100,
        default=None,
        blank=True,
        null=True,
        verbose_name="Path of file containing Root CA for MQTT Server",
    )
    tls_cert = models.CharField(
        max_length=100, default=None, blank=True, null=True, verbose_name="Path of file containing the user certificate"
    )
    tls_key = models.CharField(
        max_length=100, default=None, blank=True, null=True, verbose_name="Path of file containing the user keyfile"
    )
    tls_key_pass = models.CharField(
        max_length=100, default=None, blank=True, null=True, verbose_name="Password for user keyfile"
    )


class MqttInterlock(BaseModel):
    QOS_OPTIONS = [
        (0, "0 - None"),
        (1, "1 - At Least Once"),
        (2, "2 - Exactly Once"),
    ]
    interlock = models.OneToOneField(Interlock, on_delete=models.CASCADE)
    command_topic = models.CharField(max_length=100, default="", verbose_name="Command Topic")
    state_topic = models.CharField(max_length=100, default="", verbose_name="State topic")
    on_payload = models.TextField(default="ON", verbose_name="ON Payload")
    off_payload = models.TextField(default="OFF", verbose_name="OFF Payload")
    qos = models.PositiveSmallIntegerField(choices=QOS_OPTIONS, default=2, verbose_name="QoS")
