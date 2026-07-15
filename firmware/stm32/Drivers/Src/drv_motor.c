#include "drv_motor.h"
#include "app_config.h"

/*
 * ZS-X11H Motor Driver Interface
 *
 * Per motor controller:
 *   PWM  -> speed control (duty cycle)
 *   DIR  -> direction (HIGH/LOW mapping TBD - verify on bench)
 *   STOP -> enable/disable (active level TBD - verify on bench)
 *   BRAKE -> regenerative brake (active level TBD)
 *
 * All functions return error_t (Elecia White, Ch 3 "Standardized Error Codes").
 *
 * TODO: Replace with actual HAL calls after CubeMX pin assignment.
 */

static bool initialized = false;

error_t motor_init(void)
{
    /* TODO: Start PWM timers for both channels
     *   HAL_TIM_PWM_Start(&htimX, TIM_CHANNEL_1);  // left
     *   HAL_TIM_PWM_Start(&htimX, TIM_CHANNEL_2);  // right
     *
     * Set initial duty to 0
     * Set STOP pins to ACTIVE (motors disabled)
     * Set BRAKE pins to INACTIVE
     * Set DIR pins to FORWARD
     */

    initialized = true;
    motor_emergency_stop();
    return ERR_NONE;
}

error_t motor_enable(motor_id_t id, bool enable)
{
    if (!initialized) return ERR_UNINITIALIZED;
    if (id >= MOTOR_COUNT) return ERR_BAD_INDEX;

    /* TODO:
     * if (enable)
     *     HAL_GPIO_WritePin(STOP_PORT[id], STOP_PIN[id], STOP_ENABLE_LEVEL);
     * else
     *     HAL_GPIO_WritePin(STOP_PORT[id], STOP_PIN[id], STOP_DISABLE_LEVEL);
     */
    (void)id;
    (void)enable;
    return ERR_NONE;
}

error_t motor_set_duty(motor_id_t id, float duty)
{
    if (!initialized) return ERR_UNINITIALIZED;
    if (id >= MOTOR_COUNT) return ERR_BAD_INDEX;

    if (duty < 0.0f) duty = 0.0f;
    if (duty > 1.0f) duty = 1.0f;

    /* TODO:
     * uint32_t period = __HAL_TIM_GET_AUTORELOAD(&htimX);
     * uint32_t compare = (uint32_t)(duty * (float)period);
     *
     * if (id == MOTOR_LEFT)
     *     __HAL_TIM_SET_COMPARE(&htimX, TIM_CHANNEL_1, compare);
     * else
     *     __HAL_TIM_SET_COMPARE(&htimX, TIM_CHANNEL_2, compare);
     */
    (void)id;
    (void)duty;
    return ERR_NONE;
}

error_t motor_set_direction(motor_id_t id, motor_dir_t dir)
{
    if (!initialized) return ERR_UNINITIALIZED;
    if (id >= MOTOR_COUNT) return ERR_BAD_INDEX;

    /* TODO:
     * GPIO_PinState level = (dir == MOTOR_DIR_FORWARD)
     *     ? FORWARD_LEVEL : REVERSE_LEVEL;
     * HAL_GPIO_WritePin(DIR_PORT[id], DIR_PIN[id], level);
     */
    (void)id;
    (void)dir;
    return ERR_NONE;
}

error_t motor_set_brake(motor_id_t id, bool brake_on)
{
    if (!initialized) return ERR_UNINITIALIZED;
    if (id >= MOTOR_COUNT) return ERR_BAD_INDEX;

    /* TODO:
     * GPIO_PinState level = brake_on ? BRAKE_ACTIVE : BRAKE_INACTIVE;
     * HAL_GPIO_WritePin(BRAKE_PORT[id], BRAKE_PIN[id], level);
     */
    (void)id;
    (void)brake_on;
    return ERR_NONE;
}

void motor_emergency_stop(void)
{
    motor_set_duty(MOTOR_LEFT, 0.0f);
    motor_set_duty(MOTOR_RIGHT, 0.0f);
    motor_enable(MOTOR_LEFT, false);
    motor_enable(MOTOR_RIGHT, false);
}
