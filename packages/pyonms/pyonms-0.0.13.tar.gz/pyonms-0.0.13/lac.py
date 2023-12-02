from pyonms import PyONMS
from pyonms.models import event

hostname = "https://10.2.250.16:8443/opennms"
username = "frontierapi"
password = "frontierapi"


# Create a OpenNMS server connection object.  If the given hostname doesn't match the SSL certificate, you can add `verify_ssl=False` to bypass certificate checking.
server = PyONMS(hostname=hostname, username=username, password=password)

# Replace this next line with however you get alerts from Zabbix
zabbix_alert = zabbix.get_alert(zabbix_alert_id)


# Lookup the IP in OpenNMS, which will tell us the node ID (assuming there's only one node that has the IP address)
onms_interface = server.ips.get_ips(ip=zabbix_alert.ip_address, primary="P")

# Create an event object.
payload = event.Event(
    uei="uei.opennms.org/restapi/frontier/event",
    severity=event.Severity.MAJOR,
    description="event description text",
    ipAddress=zabbix_alert.ip_address,
    nodeId=onms_interface[0].nodeId,
)

# Send the event
send_status = server.events.send_event(payload)
if send_status:
    print("Event created successfully")
else:
    print("Error sending event")
