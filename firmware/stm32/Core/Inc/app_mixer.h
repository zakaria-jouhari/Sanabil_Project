#ifndef APP_MIXER_H
#define APP_MIXER_H

#include <stdint.h>

typedef struct {
    float duty;         /* 0.0 to 1.0 */
    uint8_t forward;    /* 1 = forward, 0 = reverse */
} motor_command_t;

typedef struct {
    float prev_left;
    float prev_right;
    uint32_t last_update_ms;
    uint8_t left_dir_change_pending;
    uint8_t right_dir_change_pending;
    uint32_t left_dir_dwell_start;
    uint32_t right_dir_dwell_start;
} mixer_state_t;

void mixer_init(mixer_state_t *mx);

/*
 * Convert RC-style throttle + steering into left/right motor commands.
 * throttle: -1.0 (full reverse) to +1.0 (full forward)
 * steering: -1.0 (full left) to +1.0 (full right)
 * dt_ms: time since last call in milliseconds
 */
void mixer_update(mixer_state_t *mx,
                  float throttle, float steering,
                  uint32_t now_ms,
                  motor_command_t *left_out,
                  motor_command_t *right_out);

/*
 * Convert cmd_vel (linear m/s, angular rad/s) to throttle/steering.
 * Normalized to [-1, 1] based on max speed.
 */
void mixer_cmd_vel_to_inputs(float linear_vel, float angular_vel,
                             float max_linear, float max_angular,
                             float *throttle_out, float *steering_out);

#endif /* APP_MIXER_H */
