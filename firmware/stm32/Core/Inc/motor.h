/*
 * motor.h  -  Differential-drive motor control for the UGV
 *
 * Two ZS-X11H BLDC controllers, one per driven wheel. Each board takes:
 *   - PWM  -> speed   (TIM1: CH1=PE9 left, CH2=PE11 right; board "P" pin, jumper set)
 *   - DIR  -> direction (ACTIVE LOW)
 *   - STOP -> run/stop  (ACTIVE LOW: HIGH = run, LOW = stop)
 * Speed channel = CH2 (right-stick vertical), steering = CH1 (right-stick horizontal),
 * both spring-centered so releasing the stick stops the vehicle.
 */
#ifndef MOTOR_H
#define MOTOR_H

#include <stdint.h>
#include "stm32f7xx_hal.h"

typedef enum {
    MOTOR_LEFT  = 0,
    MOTOR_RIGHT = 1
} motor_side_t;

/* Configure TIM1 PWM + DIR/STOP GPIOs and leave both motors stopped. */
void motor_init(void);

/* Drive one side. cmd in -1000..+1000 (sign = direction, magnitude = speed). */
void motor_set(motor_side_t side, int16_t cmd);

/* Immediately stop both motors (assert STOP, 0% PWM). */
void motor_stop_all(void);

/* Read iBUS, mix to left/right, drive motors. Stops if disarmed or RC link lost. */
void motor_rc_update(void);

/* Poll the arm button (debounced). Each press toggles armed/disarmed. Call ~100 Hz. */
void motor_button_update(void);

/* 1 = armed (drive enabled), 0 = disarmed (motors forced stop). */
int motor_is_armed(void);

/* Last commanded direction for a side: +1 forward, -1 reverse, 0 stopped.
 * Used to sign the encoder speed (the S pin gives magnitude only). */
int motor_dir_sign(motor_side_t side);

#endif /* MOTOR_H */
