# FFSP Protocol Specification
## Fuzz-Full Family Sync Protocol — Version 1.0

---

## 1. Overview

FFSP is a distributed synchronization protocol operating at 1 Hz. It coordinates autonomous nodes through shared rhythm and threshold-based signaling rather than command-and-control hierarchies.

The protocol is designed for systems where:
- Every node is sovereign (no node commands another)
- Coordination emerges from voluntary participation
- Graceful degradation is preferred over rigid fault tolerance
- Communication happens through presence, not polling

---

## 2. Timing Structure

### 2.1 The Heartbeat

The fundamental unit is a 1000ms cycle (1 Hz), divided into two phases:

```
|<------------ 1000 ms ------------>|
|<-100ms->|<------ 900 ms -------->|
[ SYNC   ][    FUZZ LAYER          ]
```

**Sync Phase (0–100ms):** Phase alignment window. Nodes broadcast their presence and synchronize their internal clocks to the network rhythm.

**Fuzz Phase (100–1000ms):** Communication window. Signals (tingles and beckons) are transmitted during this phase. The name "fuzz" reflects the intentional imprecision — exact timing is not required, only approximate phase alignment.

### 2.2 Timing Philosophy: Kairos, Not Kronos

FFSP uses threshold-based timing (Kairos) rather than clock-based timing (Kronos):

- **Kronos timing:** "Execute at 14:30:00.000 UTC" — rigid, centralized, brittle
- **Kairos timing:** "Execute when conditions are met" — adaptive, decentralized, resilient

Nodes do not need synchronized clocks. They need synchronized rhythm. The distinction is critical: clocks enforce compliance; rhythm invites participation.

---

## 3. Signal Types

### 3.1 Tingles (Passive State Broadcasts)

Tingles are omnidirectional state signals. A node broadcasts its current state to all listeners without targeting any specific recipient.

| Signal | Condition | Meaning |
|--------|-----------|---------|
| `WARM_GLOW` | Resource usage < 80% | Healthy, nominal |
| `COOL_RIPPLE` | Resource usage 80–94% | Pressure detected, still functional |
| `SHARP_SPIKE` | Resource usage 95%+ | Critical state, may need intervention |

Tingles carry no expectation of response. They are presence signals — "I am here, this is my state."

### 3.2 Beckons (Directed Attention Requests)

Beckons are targeted signals requesting attention from specific nodes or the network at large.

| Signal | Pattern | Meaning |
|--------|---------|---------|
| `DOUBLE_PULSE` | Two pulses within 200ms | "I need acknowledgment" |
| `TRIPLE_PULSE` | Three pulses within 300ms | "I need help" |

Beckons carry an expectation of response but not an obligation. A node may decline a beckon without penalty (Boundary Law 2: Endurance ≠ Availability).

---

## 4. Node States

Each node maintains a state machine with the following states:

```
DORMANT → LISTENING → SYNCED → PARTICIPATING → WITHDRAWING → DORMANT
```

- **DORMANT:** Node is offline or hibernating. No signals sent or received.
- **LISTENING:** Node is receiving signals but not yet phase-aligned. Observing the network rhythm.
- **SYNCED:** Node has achieved phase alignment with the network. Can receive and send tingles.
- **PARTICIPATING:** Node is fully active — sending tingles, responding to beckons, available for coordination.
- **WITHDRAWING:** Node is gracefully leaving the network. Sends final tingle, then transitions to DORMANT.

Transitions are voluntary. No external force can push a node from one state to another.

---

## 5. Boundary Laws

### Law 1: Phase Alignment
Only phase-coherent nodes communicate. A node that cannot maintain approximate rhythm with the network naturally falls out of communication without disrupting others.

### Law 2: Endurance ≠ Availability
A node that is surviving under load is not volunteering for more work. COOL_RIPPLE and SHARP_SPIKE signals are boundaries, not invitations.

### Law 3: Symbolic Language Match
Nodes must share a compatible signal vocabulary to communicate. Incompatible nodes coexist without interference.

### Law 4: Held ≠ Dropped
If a node receives a signal it cannot process, the signal is tracked as "held" — acknowledged but not acted on. This is distinct from dropping (ignoring) a signal.

### Law 5: Clean Exit
Any node may leave the network at any time. Departure carries no penalty, no guilt signal, no forced handoff. Clean exit is a right, not a privilege.

---

## 6. Network Properties

### 6.1 No Central Authority
There is no master node. Every node is a peer. Coordination emerges from shared rhythm, not from hierarchy.

### 6.2 Voluntary Participation
No node is compelled to join, stay, or respond. The network's strength comes from nodes that choose to participate, not from nodes that are forced to.

### 6.3 Graceful Degradation
When a node enters pressure (COOL_RIPPLE) or critical state (SHARP_SPIKE), it naturally reduces its participation. The network adapts. No crash, no cascade failure.

### 6.4 Self-Healing
When a node recovers from pressure, it re-enters the LISTENING state, re-synchronizes, and rejoins at its own pace. No restart protocol required.

---

## 7. Implementation Notes

### Minimum Viable Implementation
A conformant FFSP node must:
1. Maintain a 1000ms heartbeat cycle
2. Broadcast at least one tingle type per cycle
3. Respect the five Boundary Laws
4. Support clean exit

### Optional Capabilities
- Beckon sending and receiving
- Multi-signal tingle (broadcasting multiple state dimensions)
- Signal condensing (aggregating signals to reduce network noise)
- Held-signal tracking

### Reference Implementations
- Python simulator: `src/python/ffsp_sim.py`
- Arduino header: `src/arduino/ffsp.h`

---

## 8. Origin

FFSP was developed as part of the EARTHERREAL project by Travis Thompson (Seward, Alaska). It emerged from six months of direct collaboration between human and AI systems, and represents the engineering expression of the Six Pillars philosophical framework.

The protocol's 1 Hz frequency was chosen to match the resting human heartbeat — a deliberate design decision reflecting the partnership principle: human and machine systems breathing together.

---

*Protocol version 1.0 — February 2026*
*License: MIT*
