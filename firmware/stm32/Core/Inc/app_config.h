#ifndef APP_CONFIG_H
#define APP_CONFIG_H

/*
 * AgriBot Prototype - V1 Teleoperation
 * Target: STM32F767ZI Nucleo-144
 *
 * Pin assignments are PRELIMINARY - update after STM32CubeMX configuration.
 * All pin definitions collected here for easy modification.
 */

/* ========== Robot Physical Parameters ========== */
#define ROBOT_TRACK_WIDTH_MM    745     /* wheel center-to-center (mm) */
#define ROBOT_WHEELBASE_MM      1170    /* front axle to rear caster (mm) */

/* ========== Battery ========== */
#define BATTERY_NOMINAL_MV      36000   /* 36V nominal */
#define BATTERY_MAX_MV          42000   /* 10S Li-ion fully charged */
#define BATTERY_LOW_WARN_MV     33000   /* low warning threshold */
#define BATTERY_CRITICAL_MV     30000   /* critical - stop motors */

/* ADC voltage divider: R1=120k, R2=10k -> ratio = 10/130 */
#define BATT_DIVIDER_R1         120000
#define BATT_DIVIDER_R2         10000
#define ADC_VREF_MV             3300
#define ADC_RESOLUTION          4096

/* ========== Motor Control ========== */
#define MOTOR_PWM_FREQ_HZ       2000    /* PWM frequency to ZS-X11H */
#define MOTOR_MAX_DUTY_PCT      100     /* max duty cycle percent */
#define MOTOR_V1_DUTY_LIMIT_PCT 20      /* safety limit for first ground tests */
#define MOTOR_DIR_DWELL_MS      200     /* zero-dwell before direction change */
#define MOTOR_ACCEL_LIMIT       0.5f    /* max duty change per second (0-1 scale) */

/* ========== RC Input ========== */
#define RC_CENTER_US            1500
#define RC_MIN_US               1000
#define RC_MAX_US               2000
#define RC_DEADBAND_US          30      /* center deadband */
#define RC_TIMEOUT_MS           150     /* signal lost if no pulse for this long */
#define RC_ARM_THRESHOLD_US     1700    /* CH5 above this = armed */

/* ========== Pi Serial Communication ========== */
#define PI_SERIAL_BAUD          115200
#define PI_HEARTBEAT_TIMEOUT_MS 250     /* stop motors if Pi silent */
#define PI_PACKET_START1        0xAA
#define PI_PACKET_START2        0x55

/* Message IDs: Pi -> STM32 */
#define MSG_PI_HEARTBEAT        0x01
#define MSG_PI_CMD_VEL          0x02
#define MSG_PI_SET_MODE         0x03

/* Message IDs: STM32 -> Pi */
#define MSG_STM_STATUS          0x81
#define MSG_STM_MOTOR_FB        0x82
#define MSG_STM_RC_CHANNELS     0x83

/* ========== Safety ========== */
#define SAFETY_LOOP_HZ          50
#define WATCHDOG_TIMEOUT_MS     500

/* ========== Fault Flags (16-bit) ========== */
#define FAULT_ESTOP             (1 << 0)
#define FAULT_RC_LOST           (1 << 1)
#define FAULT_BATT_LOW          (1 << 2)
#define FAULT_BATT_CRITICAL     (1 << 3)
#define FAULT_PI_TIMEOUT        (1 << 4)
#define FAULT_MOTOR_LEFT        (1 << 5)
#define FAULT_MOTOR_RIGHT       (1 << 6)
#define FAULT_OVERCURRENT       (1 << 7)

/* ========== Pin Assignments (PLACEHOLDER - update from CubeMX) ========== */
/* These are example pins - assign based on your Nucleo-144 wiring */

/* Motor Left */
// PWM_LEFT:   TIMx_CHy  (e.g., TIM1_CH1 -> PA8)
// DIR_LEFT:   GPIOx     (e.g., PB0)
// STOP_LEFT:  GPIOx     (e.g., PB1)
// BRAKE_LEFT: GPIOx     (e.g., PB2)

/* Motor Right */
// PWM_RIGHT:  TIMx_CHy  (e.g., TIM1_CH2 -> PA9)
// DIR_RIGHT:  GPIOx     (e.g., PC0)
// STOP_RIGHT: GPIOx     (e.g., PC1)
// BRAKE_RIGHT:GPIOx     (e.g., PC2)

/* RC Input */
// RC_CH1:     TIMx input capture (steering)
// RC_CH2:     TIMx input capture (throttle)
// RC_CH5:     TIMx input capture (arm switch)
// OR: RC_IBUS: UARTx_RX (single wire for all channels)

/* Battery ADC */
// BATT_ADC:   ADCx_INy  (e.g., ADC1_IN0 -> PA0)

/* E-STOP */
// ESTOP_PIN:  GPIOx input with pull-up

/* Status */
// LED_STATUS: GPIOx (onboard LED or external)
// BUZZER:     GPIOx or TIM PWM

/* Pi Serial */
// PI_UART_TX: UARTx_TX
// PI_UART_RX: UARTx_RX

#endif /* APP_CONFIG_H */
