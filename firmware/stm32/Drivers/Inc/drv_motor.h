#ifndef DRV_MOTOR_H
#define DRV_MOTOR_H

#include <stdint.h>
#include <stdbool.h>
#include "app_error.h"

typedef enum {
    MOTOR_LEFT = 0,
    MOTOR_RIGHT = 1,
    MOTOR_COUNT = 2
} motor_id_t;

typedef enum {
    MOTOR_DIR_FORWARD = 0,
    MOTOR_DIR_REVERSE = 1
} motor_dir_t;

/*
 * Initialize motor driver GPIO and PWM timers.
 * Motors start in DISABLED state (STOP pin active).
 */
error_t motor_init(void);

/*
 * Enable/disable motor controller via STOP pin.
 */
error_t motor_enable(motor_id_t id, bool enable);

/*
 * Set motor duty cycle (0.0 to 1.0).
 */
error_t motor_set_duty(motor_id_t id, float duty);

/*
 * Set motor direction.
 * Caller must ensure duty is 0 before changing direction.
 */
error_t motor_set_direction(motor_id_t id, motor_dir_t dir);

/*
 * Activate regenerative/dynamic brake.
 */
error_t motor_set_brake(motor_id_t id, bool brake_on);

/*
 * Emergency stop: disable both motors immediately, set duty to 0.
 */
void motor_emergency_stop(void);

#endif /* DRV_MOTOR_H */
