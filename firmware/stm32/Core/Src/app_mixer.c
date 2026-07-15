#include "app_mixer.h"
#include "app_config.h"
#include <math.h>

void mixer_init(mixer_state_t *mx)
{
    mx->prev_left = 0.0f;
    mx->prev_right = 0.0f;
    mx->last_update_ms = 0;
    mx->left_dir_change_pending = 0;
    mx->right_dir_change_pending = 0;
    mx->left_dir_dwell_start = 0;
    mx->right_dir_dwell_start = 0;
}

static float clampf(float val, float lo, float hi)
{
    if (val < lo) return lo;
    if (val > hi) return hi;
    return val;
}

static float rate_limit(float target, float current, float max_delta)
{
    float diff = target - current;
    if (diff > max_delta) diff = max_delta;
    if (diff < -max_delta) diff = -max_delta;
    return current + diff;
}

static float apply_deadband(float val, float deadband)
{
    if (fabsf(val) < deadband) return 0.0f;
    return val;
}

void mixer_update(mixer_state_t *mx,
                  float throttle, float steering,
                  uint32_t now_ms,
                  motor_command_t *left_out,
                  motor_command_t *right_out)
{
    /* Compute dt */
    uint32_t dt_ms = now_ms - mx->last_update_ms;
    if (dt_ms == 0) dt_ms = 20; /* default 50Hz */
    if (dt_ms > 200) dt_ms = 200; /* clamp for safety */
    mx->last_update_ms = now_ms;
    float dt_s = (float)dt_ms / 1000.0f;

    /* Apply deadband */
    throttle = apply_deadband(throttle, 0.05f);
    steering = apply_deadband(steering, 0.05f);

    /* Differential mix: left = throttle - steering, right = throttle + steering */
    float left_raw  = throttle - steering;
    float right_raw = throttle + steering;

    /* Normalize if exceeding [-1, 1] */
    float max_mag = fmaxf(fabsf(left_raw), fabsf(right_raw));
    if (max_mag > 1.0f) {
        left_raw  /= max_mag;
        right_raw /= max_mag;
    }

    /* Apply V1 duty limit */
    float limit = (float)MOTOR_V1_DUTY_LIMIT_PCT / 100.0f;
    left_raw  = clampf(left_raw,  -limit, limit);
    right_raw = clampf(right_raw, -limit, limit);

    /* Rate limit (acceleration limiter) */
    float max_delta = MOTOR_ACCEL_LIMIT * dt_s;
    float left_limited  = rate_limit(left_raw,  mx->prev_left,  max_delta);
    float right_limited = rate_limit(right_raw, mx->prev_right, max_delta);

    mx->prev_left  = left_limited;
    mx->prev_right = right_limited;

    /* Convert signed command to duty + direction */
    /* Handle direction change dwell for left motor */
    uint8_t left_fwd  = (left_limited >= 0.0f) ? 1 : 0;
    uint8_t right_fwd = (right_limited >= 0.0f) ? 1 : 0;

    left_out->duty = fabsf(left_limited);
    left_out->forward = left_fwd;

    right_out->duty = fabsf(right_limited);
    right_out->forward = right_fwd;
}

void mixer_cmd_vel_to_inputs(float linear_vel, float angular_vel,
                             float max_linear, float max_angular,
                             float *throttle_out, float *steering_out)
{
    if (max_linear > 0.0f)
        *throttle_out = clampf(linear_vel / max_linear, -1.0f, 1.0f);
    else
        *throttle_out = 0.0f;

    if (max_angular > 0.0f)
        *steering_out = clampf(angular_vel / max_angular, -1.0f, 1.0f);
    else
        *steering_out = 0.0f;
}
