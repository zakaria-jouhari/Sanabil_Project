#ifndef DRV_RC_INPUT_H
#define DRV_RC_INPUT_H

#include <stdint.h>
#include <stdbool.h>

#define RC_NUM_CHANNELS 6

typedef struct {
    uint16_t channels[RC_NUM_CHANNELS]; /* pulse width in microseconds */
    uint32_t last_update_tick;          /* HAL tick of last valid frame */
    bool valid;                         /* true if receiving data */
} rc_input_t;

/*
 * Initialize RC input.
 * For iBUS: configure UART RX with interrupt.
 * For PWM:  configure timer input capture channels.
 */
void rc_init(void);

/*
 * Call periodically (or from ISR) to process incoming RC data.
 * For iBUS: call from UART RX complete callback.
 * For PWM:  data is updated in timer ISR, this just checks timeout.
 */
void rc_update(rc_input_t *rc, uint32_t now_tick);

/*
 * Get normalized channel value.
 * Returns -1.0 to +1.0 for stick channels.
 * channel: 0-based index
 */
float rc_get_normalized(const rc_input_t *rc, uint8_t channel);

/*
 * Check if arm switch (CH5) is in armed position.
 */
bool rc_is_armed(const rc_input_t *rc);

/*
 * Check if mode switch indicates autonomous mode.
 * Returns true if CH6 > threshold (or whichever channel you assign).
 */
bool rc_is_auto_mode(const rc_input_t *rc);

/*
 * Check if RC signal is valid (receiving within timeout).
 */
bool rc_is_valid(const rc_input_t *rc, uint32_t now_tick);

#endif /* DRV_RC_INPUT_H */
