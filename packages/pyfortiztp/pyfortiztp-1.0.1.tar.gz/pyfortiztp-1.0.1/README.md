# pyfortiztp
Python API client library for Fortinet's [FortiZTP](https://fortiztp.forticloud.com).

The FortiZTP Cloud API provides:
 - Retrieve provisioning status of FortiGates, FortiAPs, and FortiSwitch.
 - Provision or un-provision devices to the cloud or on-premise targets.

## Installation
To install run `pip install pyfortiztp`.

Alternatively, you can clone the repo and run `python setup.py install`.

## Quick Start
To begin, import pyfortiztp and instantiate the API.

We need to provide our API credentials to our FortiCloud account.

Optionally, its possible to set the following settings:
- `client_id` which defaults to `fortiztp`.
- `forticloud_host` which defaults to `https://customerapiauth.fortinet.com`
- `fortiztp_host` which defaults to `https://fortiztp.forticloud.com`

**Code**
```
fortiztp = pyfortiztp.api(
    userid = "<your forticloud userid>",
    password = "<your forticloud password>"
)
```

## Examples
### Retrieve a single device.
**Code**
```
device = fortiztp.devices.all(deviceSN="FGT60FTK1234ABCD")
print(device)
```

**Output**
```
{
    "deviceSN": "FGT60FTK1234ABCD",
    "deviceType": "FortiGate",
    "provisionStatus": "unprovisioned",
    "provisionTarget": null,
    "region": "global,europe,JP,US",
    "externalControllerSn": null,
    "externalControllerIp": null,
    "platform": null
}
```

### Provision one or more devices to FortiManager.
`deviceSN` is a list of serial numbers. In this example, we only test with a single serial number.

**Code**
```
update = fortiztp.devices.update(
    deviceSN = ["FGT60FTK1234ABCD"],
    deviceType = "FortiGate",
    provisionStatus = "provisioned",
    provisionTarget = "FortiManager",
    externalControllerIp = "<external IP of your fortimanager>",
    externalControllerSn = "<serial number of your fortimanager>"
)
print(update)
```

**Output**
```
204
```

> **Note:** The FortiZTP API returns the HTTP response "204 No Content" on success.

### Unprovision one or more devices from FortiManager.
`deviceSN` is a list of serial numbers. In this example, we only test with a single serial number.

**Code**
```
update = fortiztp.devices.update(
    deviceSN = ["FGT60FTK1234ABCD"],
    deviceType = "FortiGate",
    provisionStatus = "unprovisioned",
    provisionTarget = "FortiManager",
    externalControllerIp = "<external IP of your fortimanager>",
    externalControllerSn = "<serial number of your fortimanager>"
)
print(update)
```

**Output**
```
204
```

### Error messages.
Error messages are provided as is, from the FortiZTP API.

**Code**
```
update = fortiztp.devices.update(
    deviceSN = ["FGT60FTK1234ABCD", "testSN"],
    deviceType = "FortiGate",
    provisionStatus = "provisioned",
    provisionTarget = "FortiManager"
)
print(update)
```

**Output**
```
{
    "error": "invalid_request",
    "error_description": "Device testSN doesn't exist in this account"
}
```