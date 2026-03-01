/*
 * FFSP — Fuzz-Full Family Sync Protocol
 * Arduino/Embedded Header — Version 1.0
 *
 * A 1 Hz coordination protocol built on partnership, not control.
 * Each node is sovereign. Coordination emerges from shared rhythm.
 *
 * License: MIT
 * Origin: EARTHERREAL Project — Travis Thompson, Seward, Alaska
 *
 * Usage:
 *   #include "ffsp.h"
 *   FFSPNode node("my-node");
 *   void loop() { node.heartbeat(); }
 */

#ifndef FFSP_H
#define FFSP_H

#include <Arduino.h>

/* ── Timing Constants ─────────────────────────────────── */

#define FFSP_CYCLE_MS       1000   /* Full heartbeat cycle */
#define FFSP_SYNC_MS        100    /* Sync phase duration */
#define FFSP_FUZZ_MS        900    /* Fuzz phase duration */

/* ── Thresholds ───────────────────────────────────────── */

#define FFSP_HEALTHY        0.80f  /* Below = WARM_GLOW */
#define FFSP_PRESSURE       0.90f  /* Above = COOL_RIPPLE */
#define FFSP_CRITICAL       0.95f  /* Above = SHARP_SPIKE */

/* ── Signal Types ─────────────────────────────────────── */

typedef enum {
    TINGLE_WARM_GLOW  = 0x01,    /* Healthy, nominal */
    TINGLE_COOL_RIPPLE = 0x02,   /* Pressure detected */
    TINGLE_SHARP_SPIKE = 0x03,   /* Critical state */
} ffsp_tingle_t;

typedef enum {
    BECKON_DOUBLE_PULSE = 0x10,  /* Attention requested */
    BECKON_TRIPLE_PULSE = 0x11,  /* Help needed */
} ffsp_beckon_t;

typedef enum {
    STATE_DORMANT      = 0,
    STATE_LISTENING    = 1,
    STATE_SYNCED       = 2,
    STATE_PARTICIPATING = 3,
    STATE_WITHDRAWING  = 4,
} ffsp_state_t;

/* ── Signal Packet ────────────────────────────────────── */

typedef struct {
    char source[16];              /* Node name */
    uint8_t signal_type;          /* Tingle or Beckon */
    char target[16];              /* Empty = broadcast */
    unsigned long timestamp;      /* millis() at send */
} ffsp_signal_t;

/* ── Callbacks ────────────────────────────────────────── */

typedef void (*ffsp_send_fn)(ffsp_signal_t *signal);
typedef void (*ffsp_on_signal_fn)(ffsp_signal_t *signal);

/* ── Node ─────────────────────────────────────────────── */

class FFSPNode {
public:
    char name[16];
    ffsp_state_t state;
    float resource_usage;
    unsigned long cycle_count;
    unsigned long last_beat;

    ffsp_send_fn send_handler;
    ffsp_on_signal_fn signal_handler;

    FFSPNode(const char *node_name) {
        strncpy(name, node_name, 15);
        name[15] = '\0';
        state = STATE_DORMANT;
        resource_usage = 0.0f;
        cycle_count = 0;
        last_beat = 0;
        send_handler = NULL;
        signal_handler = NULL;
    }

    /* Set the function used to transmit signals */
    void onSend(ffsp_send_fn fn) { send_handler = fn; }

    /* Set the function called when a signal is received */
    void onSignal(ffsp_on_signal_fn fn) { signal_handler = fn; }

    /* Set current resource usage (0.0 to 1.0) */
    void setResourceUsage(float usage) {
        resource_usage = constrain(usage, 0.0f, 1.0f);
    }

    /* Get current tingle based on resource state */
    ffsp_tingle_t getTingle() {
        if (resource_usage >= FFSP_CRITICAL) return TINGLE_SHARP_SPIKE;
        if (resource_usage >= FFSP_HEALTHY)  return TINGLE_COOL_RIPPLE;
        return TINGLE_WARM_GLOW;
    }

    /* Wake the node — transition from DORMANT to LISTENING */
    void wake() {
        if (state == STATE_DORMANT) {
            state = STATE_LISTENING;
            last_beat = millis();
        }
    }

    /* Graceful exit — Boundary Law 5: Clean Exit */
    void withdraw() {
        if (state == STATE_PARTICIPATING || state == STATE_SYNCED) {
            /* Send final tingle */
            if (send_handler) {
                ffsp_signal_t sig;
                _buildSignal(&sig, getTingle());
                send_handler(&sig);
            }
            state = STATE_DORMANT;
        }
    }

    /*
     * Execute one heartbeat cycle.
     * Call this from loop(). It self-paces at 1 Hz.
     *
     * Returns true if a heartbeat was executed this call.
     */
    bool heartbeat() {
        if (state == STATE_DORMANT) return false;

        unsigned long now = millis();
        if (now - last_beat < FFSP_CYCLE_MS) return false;

        last_beat = now;
        cycle_count++;

        /* Auto-advance state */
        if (state == STATE_LISTENING)  state = STATE_SYNCED;
        if (state == STATE_SYNCED)     state = STATE_PARTICIPATING;

        if (state != STATE_PARTICIPATING) return false;

        /* ── SYNC PHASE ── */
        /* (Phase alignment happens here — in hardware, this would
            be where nodes lock to the network rhythm) */

        /* ── FUZZ PHASE ── */
        /* Broadcast current tingle */
        if (send_handler) {
            ffsp_signal_t sig;
            _buildSignal(&sig, getTingle());
            send_handler(&sig);
        }

        return true;
    }

    /* Receive a signal from the network */
    void receive(ffsp_signal_t *signal) {
        if (state < STATE_SYNCED) return;
        if (strcmp(signal->source, name) == 0) return; /* Ignore own */
        if (signal_handler) {
            signal_handler(signal);
        }
    }

private:
    void _buildSignal(ffsp_signal_t *sig, uint8_t type) {
        strncpy(sig->source, name, 15);
        sig->source[15] = '\0';
        sig->signal_type = type;
        sig->target[0] = '\0'; /* Broadcast */
        sig->timestamp = millis();
    }
};

#endif /* FFSP_H */
