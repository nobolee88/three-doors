# Fuzz-Full Family Sync Protocol (FFSP)

## A 1 Hz Coordination Protocol Built on Partnership, Not Control

FFSP is a synchronization protocol that coordinates distributed systems through shared rhythm rather than command-and-control messaging. It operates at 1 Hz — one heartbeat per second — and achieves coordination through resonance rather than enforcement.

## Why This Matters

Every military coordination protocol in existence uses command-and-control: a central authority issues orders, subordinates execute. FFSP demonstrates an alternative — coordination through voluntary synchronization, where every node is sovereign and participates by choice.

This is not just engineering philosophy. It produces measurably different behavior:
- **No single point of failure** — remove any node, the system continues
- **Graceful degradation** — nodes under pressure naturally reduce participation without breaking the network
- **Self-healing** — nodes recover and rejoin without external intervention
- **Threshold-based timing** — events trigger on conditions, not clocks (Kairos, not Kronos)

## The 1 Hz Heartbeat

```
|<------------ 1000 ms ------------>|
|<-100ms->|<------ 900 ms -------->|
[ SYNC   ][    FUZZ LAYER          ]
```

- **Sync window (100ms):** Nodes align phase
- **Fuzz layer (900ms):** Communication happens in the space between beats

Communication lives in the silence, not in the signal. This is by design.

## Signal Types

| Signal | Type | Meaning |
|--------|------|---------|
| WARM_GLOW | Tingle | Healthy, nominal state |
| COOL_RIPPLE | Tingle | Resource pressure detected |
| SHARP_SPIKE | Tingle | Critical event |
| DOUBLE_PULSE | Beckon | Attention requested |
| TRIPLE_PULSE | Beckon | Help needed |

**Tingles** are passive state broadcasts — "this is how I'm doing."
**Beckons** are directed attention requests — "I need you to notice me."

## Files

- `PROTOCOL_SPEC.md` — Full protocol specification
- `src/python/ffsp_sim.py` — Python reference implementation and simulator
- `src/arduino/ffsp.h` — Arduino/embedded header for hardware deployment
- `examples/arduino_battery_share/` — Example: cooperative battery sharing between devices

## Quick Start (Python)

```bash
python3 ffsp/src/python/ffsp_sim.py
```

This runs a 3-node FFSP network simulation showing synchronization, signal exchange, and graceful degradation under load.

## License

MIT — use it, modify it, deploy it, learn from it.
