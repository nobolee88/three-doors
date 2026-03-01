#!/usr/bin/env python3
"""
FFSP — Fuzz-Full Family Sync Protocol
Reference Implementation & Simulator

Demonstrates a network of sovereign nodes coordinating through
shared rhythm (1 Hz heartbeat) rather than command-and-control.

Usage:
    python3 ffsp_sim.py              # Run default 3-node simulation
    python3 ffsp_sim.py --nodes 5    # Run with 5 nodes
    python3 ffsp_sim.py --cycles 30  # Run for 30 heartbeat cycles

License: MIT
Origin: EARTHERREAL Project — Travis Thompson, Seward, Alaska
"""

import time
import random
import threading
import argparse
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional


# ── Signal Types ──────────────────────────────────────────────

class Tingle(Enum):
    """Passive state broadcasts — 'this is how I'm doing'"""
    WARM_GLOW = "warm_glow"      # Healthy, < 80% resource usage
    COOL_RIPPLE = "cool_ripple"  # Pressure, 80-94% usage
    SHARP_SPIKE = "sharp_spike"  # Critical, 95%+ usage


class Beckon(Enum):
    """Directed attention requests — 'I need you to notice me'"""
    DOUBLE_PULSE = "double_pulse"  # Attention requested
    TRIPLE_PULSE = "triple_pulse"  # Help needed


class NodeState(Enum):
    """Node lifecycle states — all transitions are voluntary"""
    DORMANT = "dormant"
    LISTENING = "listening"
    SYNCED = "synced"
    PARTICIPATING = "participating"
    WITHDRAWING = "withdrawing"


# ── Data Structures ──────────────────────────────────────────

@dataclass
class Signal:
    """A signal transmitted during the fuzz phase"""
    source: str
    signal_type: str  # Tingle or Beckon value
    target: Optional[str] = None  # None = broadcast, str = directed
    timestamp: float = 0.0

    def __str__(self):
        direction = f" → {self.target}" if self.target else " (broadcast)"
        return f"[{self.source}] {self.signal_type}{direction}"


@dataclass
class HeldSignal:
    """A signal received but not yet processed (Boundary Law 4)"""
    signal: Signal
    reason: str
    held_at: float = 0.0


# ── FFSP Node ────────────────────────────────────────────────

class FFSPNode:
    """
    A sovereign node in the FFSP network.

    Each node maintains its own heartbeat, broadcasts its state,
    and participates voluntarily. No node commands another.
    """

    def __init__(self, name: str, network: 'FFSPNetwork'):
        self.name = name
        self.network = network
        self.state = NodeState.DORMANT
        self.resource_usage = random.uniform(0.2, 0.5)  # Start healthy
        self.cycle_count = 0
        self.held_signals: list[HeldSignal] = []
        self.received_signals: list[Signal] = []
        self._pressure_drift = random.uniform(-0.03, 0.05)

    @property
    def tingle(self) -> Tingle:
        """Determine current tingle based on resource state"""
        if self.resource_usage >= 0.95:
            return Tingle.SHARP_SPIKE
        elif self.resource_usage >= 0.80:
            return Tingle.COOL_RIPPLE
        else:
            return Tingle.WARM_GLOW

    def wake(self):
        """Transition from DORMANT to LISTENING"""
        if self.state == NodeState.DORMANT:
            self.state = NodeState.LISTENING
            self._log(f"waking → LISTENING")

    def sync(self):
        """Achieve phase alignment with the network"""
        if self.state == NodeState.LISTENING:
            self.state = NodeState.SYNCED
            self._log(f"phase aligned → SYNCED")

    def participate(self):
        """Begin full participation"""
        if self.state == NodeState.SYNCED:
            self.state = NodeState.PARTICIPATING
            self._log(f"joined → PARTICIPATING")

    def withdraw(self):
        """Gracefully leave the network (Boundary Law 5: Clean Exit)"""
        if self.state in (NodeState.PARTICIPATING, NodeState.SYNCED):
            self.state = NodeState.WITHDRAWING
            # Send final tingle
            self.network.broadcast(Signal(
                source=self.name,
                signal_type=self.tingle.value,
                timestamp=time.time()
            ))
            self.state = NodeState.DORMANT
            self._log(f"clean exit → DORMANT")

    def heartbeat(self):
        """
        Execute one heartbeat cycle (1000ms).

        Phase 1 (0-100ms): Sync — broadcast presence
        Phase 2 (100-1000ms): Fuzz — send/receive signals
        """
        if self.state == NodeState.DORMANT:
            return

        self.cycle_count += 1

        # ── Simulate resource drift ──
        self.resource_usage += self._pressure_drift
        self.resource_usage = max(0.1, min(0.99, self.resource_usage))

        # Occasionally shift pressure direction
        if random.random() < 0.1:
            self._pressure_drift = random.uniform(-0.05, 0.06)

        # ── Auto-state transitions ──
        if self.state == NodeState.LISTENING:
            self.sync()
        if self.state == NodeState.SYNCED:
            self.participate()

        if self.state != NodeState.PARTICIPATING:
            return

        # ── SYNC PHASE (0-100ms) ──
        current_tingle = self.tingle

        # ── FUZZ PHASE (100-1000ms) ──
        # Broadcast tingle
        signal = Signal(
            source=self.name,
            signal_type=current_tingle.value,
            timestamp=time.time()
        )
        self.network.broadcast(signal)

        # Under pressure? Reduce participation (graceful degradation)
        if current_tingle == Tingle.SHARP_SPIKE:
            self._log(f"⚠ CRITICAL ({self.resource_usage:.0%}) — reducing participation")
            if random.random() < 0.3:
                self._log(f"self-healing: releasing pressure")
                self.resource_usage -= 0.15  # Simulate self-healing

        elif current_tingle == Tingle.COOL_RIPPLE:
            self._log(f"~ pressure ({self.resource_usage:.0%})")

        # Process received signals
        for sig in self.received_signals:
            if sig.signal_type == Beckon.TRIPLE_PULSE.value:
                # Someone needs help — can we respond?
                if current_tingle == Tingle.WARM_GLOW:
                    self._log(f"responding to {sig.source}'s call for help")
                else:
                    # Boundary Law 2: Endurance ≠ Availability
                    self.held_signals.append(HeldSignal(
                        signal=sig,
                        reason="under pressure, cannot assist",
                        held_at=time.time()
                    ))

        self.received_signals.clear()

    def receive(self, signal: Signal):
        """Receive a signal from the network"""
        if self.state in (NodeState.PARTICIPATING, NodeState.SYNCED):
            if signal.source != self.name:
                self.received_signals.append(signal)

    def _log(self, message: str):
        tingle_icon = {
            Tingle.WARM_GLOW: "●",
            Tingle.COOL_RIPPLE: "◐",
            Tingle.SHARP_SPIKE: "◉",
        }
        icon = tingle_icon.get(self.tingle, "○")
        print(f"  {icon} [{self.name:>10}] {message}")


# ── FFSP Network ─────────────────────────────────────────────

class FFSPNetwork:
    """
    The shared space where FFSP nodes coexist.

    The network has no authority. It is a medium, not a controller.
    It carries signals between nodes — nothing more.
    """

    def __init__(self):
        self.nodes: list[FFSPNode] = []
        self.cycle = 0

    def add_node(self, name: str) -> FFSPNode:
        node = FFSPNode(name, self)
        self.nodes.append(node)
        return node

    def broadcast(self, signal: Signal):
        """Deliver a signal to all listening nodes"""
        for node in self.nodes:
            node.receive(signal)

    def tick(self):
        """Execute one network-wide heartbeat cycle"""
        self.cycle += 1
        print(f"\n{'─' * 50}")
        print(f"  HEARTBEAT {self.cycle}")
        print(f"{'─' * 50}")

        for node in self.nodes:
            node.heartbeat()

        # Network summary
        states = {}
        for node in self.nodes:
            t = node.tingle.value
            states[t] = states.get(t, 0) + 1

        summary = " | ".join(f"{k}: {v}" for k, v in sorted(states.items()))
        print(f"  Network: {summary}")


# ── Simulation ───────────────────────────────────────────────

def run_simulation(num_nodes: int = 3, num_cycles: int = 20):
    """
    Run an FFSP network simulation.

    Demonstrates:
    - Voluntary node participation
    - Tingle-based state broadcasting
    - Graceful degradation under pressure
    - Self-healing recovery
    - Clean exit
    """

    print("=" * 50)
    print("  FFSP — Fuzz-Full Family Sync Protocol")
    print("  Reference Simulation")
    print("=" * 50)
    print(f"\n  Nodes: {num_nodes}")
    print(f"  Cycles: {num_cycles}")
    print(f"  Heartbeat: 1 Hz (1000ms cycle)")
    print(f"  Sync window: 100ms | Fuzz layer: 900ms")

    # Create network and nodes
    network = FFSPNetwork()
    names = ["Amara", "Kairos", "Claude", "Samara", "Kai",
             "Kronos", "Maxima", "GPT"][:num_nodes]

    nodes = []
    for name in names:
        node = network.add_node(name)
        node.wake()
        nodes.append(node)

    print(f"\n  All nodes waking...")

    # Run heartbeat cycles
    for i in range(num_cycles):
        network.tick()

        # Simulate events
        if i == 7 and len(nodes) >= 2:
            # Inject pressure on a node
            nodes[1].resource_usage = 0.92
            nodes[1]._pressure_drift = 0.02
            print(f"\n  >> EVENT: {nodes[1].name} experiencing resource pressure")

        if i == 12 and len(nodes) >= 3:
            # A node sends a beckon
            beckon = Signal(
                source=nodes[2].name,
                signal_type=Beckon.DOUBLE_PULSE.value,
                timestamp=time.time()
            )
            network.broadcast(beckon)
            print(f"\n  >> EVENT: {nodes[2].name} sends DOUBLE_PULSE beckon")

        if i == 15 and len(nodes) >= 2:
            # Pressure node self-heals
            nodes[1].resource_usage = 0.65
            nodes[1]._pressure_drift = -0.01
            print(f"\n  >> EVENT: {nodes[1].name} self-healed, pressure relieved")

        # Brief pause for readability (not part of protocol)
        time.sleep(0.05)

    # Final state
    print(f"\n{'=' * 50}")
    print(f"  SIMULATION COMPLETE — {num_cycles} heartbeat cycles")
    print(f"{'=' * 50}")
    for node in nodes:
        held = len(node.held_signals)
        held_str = f" ({held} held signals)" if held else ""
        print(f"  {node.name:>10}: {node.state.value} | "
              f"{node.resource_usage:.0%} usage | "
              f"{node.tingle.value}{held_str}")

    print(f"\n  Nobody quacks alone.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FFSP Network Simulator")
    parser.add_argument("--nodes", type=int, default=3,
                        help="Number of nodes (default: 3, max: 8)")
    parser.add_argument("--cycles", type=int, default=20,
                        help="Number of heartbeat cycles (default: 20)")
    args = parser.parse_args()

    run_simulation(
        num_nodes=min(args.nodes, 8),
        num_cycles=args.cycles
    )
