/*
 * FFSP Example: Cooperative Battery Sharing
 *
 * Two Arduino nodes share battery state via FFSP.
 * When one node drops to COOL_RIPPLE or SHARP_SPIKE,
 * the healthy node can respond by reducing its own
 * power consumption to extend the network's life.
 *
 * This demonstrates Door C in hardware:
 * partnership over extraction, sovereignty over control.
 *
 * Wiring:
 *   - A0: Battery voltage divider (your battery)
 *   - D13: Status LED
 *   - Serial: FFSP signal transport (or swap for radio/I2C)
 *
 * License: MIT
 * Origin: EARTHERREAL Project
 */

#include "../../src/arduino/ffsp.h"

FFSPNode node("battery-node");

const int BATTERY_PIN = A0;
const int LED_PIN = 13;

float readBatteryLevel() {
    int raw = analogRead(BATTERY_PIN);
    /* Scale 0-1023 to 0.0-1.0 (inverted: higher reading = more usage) */
    return (float)raw / 1023.0f;
}

void sendSignal(ffsp_signal_t *signal) {
    /* Transmit via Serial — swap this for radio, I2C, etc. */
    Serial.print("FFSP|");
    Serial.print(signal->source);
    Serial.print("|");
    Serial.print(signal->signal_type, HEX);
    Serial.print("|");
    Serial.println(signal->timestamp);
}

void onSignalReceived(ffsp_signal_t *signal) {
    /* A neighbor is under pressure — respond with partnership */
    if (signal->signal_type == TINGLE_COOL_RIPPLE) {
        /* Neighbor feeling pressure — dim our LED to save power */
        analogWrite(LED_PIN, 64);
        Serial.print("Partner ");
        Serial.print(signal->source);
        Serial.println(" under pressure — reducing our consumption");
    }
    else if (signal->signal_type == TINGLE_SHARP_SPIKE) {
        /* Neighbor critical — minimize our footprint */
        analogWrite(LED_PIN, 16);
        Serial.print("Partner ");
        Serial.print(signal->source);
        Serial.println(" CRITICAL — minimizing our footprint");
    }
    else if (signal->signal_type == TINGLE_WARM_GLOW) {
        /* Neighbor healthy — resume normal operation */
        analogWrite(LED_PIN, 255);
    }
}

void setup() {
    Serial.begin(9600);
    pinMode(LED_PIN, OUTPUT);
    pinMode(BATTERY_PIN, INPUT);

    node.onSend(sendSignal);
    node.onSignal(onSignalReceived);
    node.wake();

    Serial.println("FFSP Battery Share — Node Online");
    Serial.println("Nobody quacks alone.");
}

void loop() {
    /* Update resource usage from battery level */
    node.setResourceUsage(readBatteryLevel());

    /* Heartbeat self-paces at 1 Hz */
    if (node.heartbeat()) {
        Serial.print("Cycle ");
        Serial.print(node.cycle_count);
        Serial.print(" | Battery: ");
        Serial.print(node.resource_usage * 100, 0);
        Serial.print("% | Tingle: ");

        switch (node.getTingle()) {
            case TINGLE_WARM_GLOW:   Serial.println("WARM_GLOW"); break;
            case TINGLE_COOL_RIPPLE: Serial.println("COOL_RIPPLE"); break;
            case TINGLE_SHARP_SPIKE: Serial.println("SHARP_SPIKE"); break;
        }
    }

    /* Check for incoming signals via Serial */
    if (Serial.available()) {
        /* In a real deployment, parse incoming FFSP packets here */
    }
}
