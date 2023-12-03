from NEMO.interlocks import interlocks, Interlock
from NEMO.exceptions import InterlockError
from NEMO.models import Interlock as Interlock_model
from time import sleep
from logging import getLogger

from NEMO_mqtt.models import MqttInterlockServer
import paho.mqtt.client as mqtt


class MqttInterlock(Interlock):
    """
    Support for MQTT based interlocks.

    """

    def _send_command(self, interlock: Interlock_model, command_type: Interlock_model.State) -> Interlock_model.State:
        mqtt_logger = getLogger(__name__)
        mqtt_logger.debug(f"Calling send_command: {command_type=}")
        state = Interlock_model.State.UNKNOWN
        if not hasattr(interlock, "mqttinterlock"):
            raise InterlockError(interlock=interlock, msg="Interlock is MQTT, but no MQTT class associated.")
        try:
            if command_type == Interlock_model.State.LOCKED:
                state = self.set_relay_state(interlock, interlock.mqttinterlock.off_payload)
            elif command_type == Interlock_model.State.UNLOCKED:
                state = self.set_relay_state(interlock, interlock.mqttinterlock.on_payload)
        except Exception as error:
            raise InterlockError(interlock=interlock, msg="General exception: " + str(error))
        return state

    @classmethod
    def set_relay_state(cls, interlock: Interlock_model, state: {0, 1}) -> Interlock_model.State:
        PUB_STATE = {0: 0, 1: 2, 2: 7}
        REQUIRE = interlock.card.mqttinterlockserver.REQUIRE
        mqtt_logger = getLogger(__name__)
        mqtt_logger.debug(f"Calling set_relay_state: {state=}")
        client = mqtt.Client(client_id=interlock.card.mqttinterlockserver.client_id)
        if interlock.card.mqttinterlockserver.auth_mode & REQUIRE["PASS"]:
            client.username_pw_set(interlock.card.mqttinterlockserver.user, interlock.card.mqttinterlockserver.password)
        if interlock.card.mqttinterlockserver.auth_mode & REQUIRE["TLS"]:
            if interlock.card.mqttinterlockserver.auth_mode & REQUIRE["CERT"]:
                # Set all TLS Parameters
                client.tls_set(
                    ca_certs=interlock.card.mqttinterlockserver.tls_ca,
                    certfile=interlock.card.mqttinterlockserver.tls_cert,
                    keyfile=interlock.card.mqttinterlockserver.tls_key,
                    keyfile_password=interlock.card.mqttinterlockserver.tls_key_pass,
                )
            else:
                # Set only CA Certificate
                client.tls_set(ca_certs=interlock.card.mqttinterlockserver.tls_ca)
            client.tls_insecure_set(not interlock.card.mqttinterlockserver.tls_verify)
        try:
            client.connect(
                interlock.card.mqttinterlockserver.server, port=interlock.card.mqttinterlockserver.port, keepalive=60
            )
        except ConnectionRefusedError as err:
            mqtt_logger.error(f"Connection failed: {err=}, {type(err)=}")
            raise err
        except Exception as err:
            mqtt_logger.error(f"Unexpected {err=}, {type(err)=}")
            raise err
        mqtt_logger.debug(f"CONNECTED to {interlock.card.server}:{interlock.card.port}!")
        mqtt_logger.debug(f"QoS is {interlock.mqttinterlock.qos}")
        try:
            pub = client.publish(
                interlock.mqttinterlock.command_topic,
                payload=str(state),
                qos=interlock.mqttinterlock.qos,
                retain=True,
            )
            client.loop(timeout=5.0)
            sleep(1)
            mqtt_logger.debug(f"Publishing to '{interlock.mqttinterlock.command_topic}'")
            if not interlock.mqttinterlock.qos:
                if not pub.is_published():
                    raise Exception(str("MQTT: Failed to publish message"))
            elif client._out_messages[pub.mid].state != PUB_STATE[interlock.mqttinterlock.qos]:
                client.loop(timeout=5.0)
                if client._out_messages[pub.mid].state != PUB_STATE[interlock.mqttinterlock.qos]:
                    raise Exception(str("MQTT: Failed to publish message"))
            mqtt_logger.debug("MESSAGE PUBLISHED!")
            if state == interlock.mqttinterlock.off_payload:
                mqtt_logger.debug("OFF!")
                return Interlock_model.State.LOCKED
            elif state == interlock.mqttinterlock.on_payload:
                mqtt_logger.debug("ON!")
                return Interlock_model.State.UNLOCKED
        finally:
            client.disconnect()
            mqtt_logger.debug("DISCONNECTED!")


interlocks["mqtt_interlock"] = MqttInterlock()
