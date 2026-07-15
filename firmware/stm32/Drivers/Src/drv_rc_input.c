#include "drv_rc_input.h"
#include "app_config.h"

/*
 * FlySky i6 Receiver Input Driver
 *
 * Two options:
 *   A) iBUS protocol over single UART (recommended)
 *   B) PWM per channel via timer input capture
 *
 * iBUS frame format (if used):
 *   32 bytes total
 *   Byte 0: 0x20 (length)
 *   Byte 1: 0x40 (command)
 *   Bytes 2-27: 14 channels, 2 bytes each, little-endian
 *   Bytes 28-29: checksum (0xFFFF - sum of bytes 0-27)
 *   Value range: 1000-2000
 *
 * TODO: Implement based on chosen input method after wiring.
 */

void rc_init(void)
{
    /* TODO:
     * For iBUS:
     *   HAL_UART_Receive_IT(&huartX, ibus_rx_buf, 32);
     *
     * For PWM input capture:
     *   HAL_TIM_IC_Start_IT(&htimX, TIM_CHANNEL_y); // per channel
     */
}

void rc_update(rc_input_t *rc, uint32_t now_tick)
{
    /* Check timeout */
    if ((now_tick - rc->last_update_tick) > RC_TIMEOUT_MS) {
        rc->valid = false;
    }

    /* TODO:
     * For iBUS: parse received buffer, validate checksum, extract channels
     * For PWM:  channels are updated in ISR, just check validity here
     */
}

float rc_get_normalized(const rc_input_t *rc, uint8_t channel)
{
    if (channel >= RC_NUM_CHANNELS) return 0.0f;

    int16_t raw = (int16_t)rc->channels[channel] - RC_CENTER_US;

    /* Apply deadband */
    if (raw > -RC_DEADBAND_US && raw < RC_DEADBAND_US)
        return 0.0f;

    /* Normalize to -1.0 .. +1.0 */
    float half_range = (float)(RC_MAX_US - RC_CENTER_US);
    float normalized = (float)raw / half_range;

    if (normalized > 1.0f) normalized = 1.0f;
    if (normalized < -1.0f) normalized = -1.0f;

    return normalized;
}

bool rc_is_armed(const rc_input_t *rc)
{
    /* CH5 (index 4) above threshold = armed */
    return rc->valid && (rc->channels[4] > RC_ARM_THRESHOLD_US);
}

bool rc_is_auto_mode(const rc_input_t *rc)
{
    /* CH6 (index 5) above threshold = auto mode */
    return rc->valid && (rc->channels[5] > RC_ARM_THRESHOLD_US);
}

bool rc_is_valid(const rc_input_t *rc, uint32_t now_tick)
{
    return rc->valid && ((now_tick - rc->last_update_tick) < RC_TIMEOUT_MS);
}
