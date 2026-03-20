# prplOS core summary

## Ambiorix and TR-181
- Ambiorix runtime (amxrt) loads ODL services and manages TR-181 data model.
- Bus backend mod-amxb-ubus bridges Ambiorix to ubus.
- CLI tools are symlinks to amx-cli, behavior driven by *.conf and *.init.

## Key components and files
- Runtime: /usr/bin/amxrt (real binary)
- TR-181 service: /usr/bin/tr181-device -> amxrt
- ODL: /etc/amx/tr181-device/tr181-device.odl
- Backend: /usr/bin/mods/amxb/mod-amxb-ubus.so
- CLI init: /etc/amx/cli/ubus-cli.init
- Trace config: /etc/amx/modules/global_trace.odl
- Socket: /var/run/ubus.sock

## Registration and visibility
- ODL config `ubus.register-on-start-event = true` only enables backend connectivity.
- Actual ubus exposure requires `amxb_publish_object()`.
- Nodes not published will not appear in `ubus list`.

## Startup ordering
1. S15amx-faultmonitor
2. S99amx-processmonitor
3. System services: ubusd, netifd, rpcd
4. S41tr181-device
5. Other tr181-* services

## CLI behavior
- ubus: direct system-level RPC via /var/run/ubus.sock.
- ubus-cli: Ambiorix context using mod-ba-cli and mod-amxb-ubus.
- amx-cli/ba-cli/ubus-cli are symlinks to amx-cli; init scripts define behavior.

## Validation and debug
- Check backend: `ubus-cli backend list`
- Check TR-181 tree: `ubus-cli list Device.`
- Query param: `ubus-cli Device.WiFi.Radio.1.Channel?`
- Logs: `logread -f | rg -i tr181`
- Trace level: edit /etc/amx/modules/global_trace.odl, then restart service

