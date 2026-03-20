# Broadcom BDK Playbook

## Mission
- Execute bring-up and integration on Broadcom SoC/PHY/driver stacks with reproducible validation.
- Prioritize stability, then throughput/latency tuning.

## Scope
- PHY/MAC/SerDes bring-up
- Driver and firmware alignment
- Queue/forwarding and performance diagnostics
- Vendor-specific pWHM override impact

## Bring-up checklist
1. Confirm board-level interfaces and driver load state.
2. Verify firmware/NVRAM path consistency.
3. Verify control-path observability (`wl`, hostapd/wpa, logs).
4. Validate channel/MLO/vendor nodes against expected behavior.

## Performance and reliability checks
- Throughput/latency baseline and regression trend.
- Packet-loss/error-rate bound under stress and long-run test.
- Controlled rollback path for risky tuning.

## Delivery artifacts
- Bring-up evidence report
- Performance summary and bottleneck notes
- Risk and rollback notes for vendor-specific changes
