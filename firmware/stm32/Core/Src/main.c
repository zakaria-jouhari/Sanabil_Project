/*
 * AgriBot Prototype - V1 Teleoperation Firmware
 * Target: STM32F767ZI Nucleo-144
 *
 * Architecture inspired by "Making Embedded Systems" (Elecia White, 2nd ed):
 *   - Very Small Scheduler (Ch 5 p.146): cooperative task scheduling
 *   - Table-Driven State Machine (Ch 6): auditable transition table
 *   - Ring Buffer (Ch 7): ISR-safe serial RX
 *   - Command Pattern (Ch 3): message dispatch table
 *   - Standardized Error Codes (Ch 3): consistent returns
 *   - Version String (Ch 3): firmware identification
 *
 * Build steps:
 *   1. Create CubeMX project for STM32F767ZI
 *   2. Configure peripherals (timers, UART, ADC, GPIO)
 *   3. Generate code
 *   4. Copy app_*.c/h and drv_*.c/h into generated project
 *   5. Call agribot_init() from main() after HAL init
 *   6. Call agribot_loop() from main while loop
 */

#include "app_config.h"
#include "app_version.h"
#include "app_error.h"
#include "app_state_machine.h"
#include "app_mixer.h"
#include "app_scheduler.h"
#include "drv_rc_input.h"
#include "drv_motor.h"
#include "drv_pi_serial.h"

/* ---- Application state ---- */

static state_machine_t g_sm;
static mixer_state_t   g_mixer;
static rc_input_t      g_rc;
static scheduler_t     g_sched;

static uint32_t g_last_pi_heartbeat = 0;

/* ---- Pi message handlers (command pattern, Ch 3) ---- */

static void handle_pi_heartbeat(const pi_packet_t *pkt)
{
    (void)pkt;
    g_last_pi_heartbeat = 0; /* TODO: = HAL_GetTick(); */
}

static void handle_pi_cmd_vel(const pi_packet_t *pkt)
{
    /* TODO: parse linear_vel + angular_vel from payload (V2) */
    (void)pkt;
}

static const pi_msg_dispatch_t pi_commands[] = {
    { MSG_PI_HEARTBEAT, handle_pi_heartbeat },
    { MSG_PI_CMD_VEL,   handle_pi_cmd_vel },
};

#define PI_CMD_COUNT (sizeof(pi_commands) / sizeof(pi_commands[0]))

/* ---- Scheduler task callbacks ---- */

/*
 * Safety-critical control loop - 50 Hz.
 * Reads inputs, runs state machine, computes and applies motor commands.
 */
static void task_control_loop(uint32_t now)
{
    /* 1. Read inputs */
    rc_update(&g_rc, now);

    uint16_t battery_mv = BATTERY_NOMINAL_MV; /* TODO: battery_read_mv() */
    bool estop = false;                        /* TODO: estop_is_active() */
    bool pi_alive = (now - g_last_pi_heartbeat) < PI_HEARTBEAT_TIMEOUT_MS;

    /* 2. Pack inputs and update state machine */
    sm_inputs_t inputs = {
        .rc_valid     = rc_is_valid(&g_rc, now),
        .rc_armed     = rc_is_armed(&g_rc),
        .rc_mode_auto = rc_is_auto_mode(&g_rc),
        .pi_alive     = pi_alive,
        .estop_active = estop,
        .battery_mv   = battery_mv,
    };

    sm_update(&g_sm, &inputs, now);

    /* 3. Compute motor commands */
    motor_command_t cmd_left  = { .duty = 0.0f, .forward = 1 };
    motor_command_t cmd_right = { .duty = 0.0f, .forward = 1 };

    if (sm_motors_allowed(&g_sm)) {
        float throttle = 0.0f;
        float steering = 0.0f;

        if (sm_get_state(&g_sm) == STATE_ARMED_MANUAL) {
            throttle = rc_get_normalized(&g_rc, 1); /* CH2 */
            steering = rc_get_normalized(&g_rc, 0); /* CH1 */
        } else if (sm_get_state(&g_sm) == STATE_ARMED_AUTO) {
            /* V2: Pi cmd_vel -> mixer_cmd_vel_to_inputs() */
        }

        mixer_update(&g_mixer, throttle, steering, now,
                     &cmd_left, &cmd_right);
    } else {
        mixer_init(&g_mixer); /* reset rate limiter */
    }

    /* 4. Apply motor commands */
    if (sm_motors_allowed(&g_sm)) {
        motor_set_direction(MOTOR_LEFT,
            cmd_left.forward ? MOTOR_DIR_FORWARD : MOTOR_DIR_REVERSE);
        motor_set_direction(MOTOR_RIGHT,
            cmd_right.forward ? MOTOR_DIR_FORWARD : MOTOR_DIR_REVERSE);
        motor_set_duty(MOTOR_LEFT, cmd_left.duty);
        motor_set_duty(MOTOR_RIGHT, cmd_right.duty);
        motor_enable(MOTOR_LEFT, true);
        motor_enable(MOTOR_RIGHT, true);
    } else {
        motor_emergency_stop();
    }
}

/*
 * Telemetry task - 10 Hz.
 * Sends status and motor feedback to Pi.
 */
static void task_telemetry(uint32_t now)
{
    /* Build status payload: [state, fault_hi, fault_lo, battery_hi, battery_lo] */
    uint16_t faults = sm_get_faults(&g_sm);
    uint8_t payload[5] = {
        (uint8_t)sm_get_state(&g_sm),
        (uint8_t)(faults >> 8),
        (uint8_t)(faults & 0xFF),
        (uint8_t)(BATTERY_NOMINAL_MV >> 8),  /* TODO: actual reading */
        (uint8_t)(BATTERY_NOMINAL_MV & 0xFF),
    };
    pi_serial_send(MSG_STM_STATUS, payload, sizeof(payload));

    (void)now;
}

/*
 * Serial RX processing task - 100 Hz.
 * Parses any buffered bytes from Pi UART.
 */
static void task_serial_rx(uint32_t now)
{
    (void)now;
    pi_serial_process();
}

/*
 * Status LED task - 2 Hz.
 * Blink pattern reflects current state.
 */
static void task_status_led(uint32_t now)
{
    /* TODO: implement LED patterns
     *   DISARMED:     toggle every 500ms (slow blink)
     *   ARMED_MANUAL: solid ON
     *   ARMED_AUTO:   toggle every 125ms (fast blink)
     *   FAULT:        toggle every 62ms (rapid flash)
     */
    (void)now;
}

/* ---- Init and main loop ---- */

void agribot_init(void)
{
    uint32_t now = 0; /* TODO: = HAL_GetTick(); */

    /* Initialize subsystems */
    sm_init(&g_sm);
    mixer_init(&g_mixer);
    rc_init();
    motor_init();
    pi_serial_init();
    pi_serial_register_handlers(pi_commands, PI_CMD_COUNT);

    /* Set up scheduler (Elecia White, Ch 5 "A Very Small Scheduler") */
    sched_init(&g_sched);
    sched_add(&g_sched, "control",   task_control_loop, 20,  now);  /* 50 Hz */
    sched_add(&g_sched, "serial_rx", task_serial_rx,    10,  now);  /* 100 Hz */
    sched_add(&g_sched, "telemetry", task_telemetry,    100, now);  /* 10 Hz */
    sched_add(&g_sched, "led",       task_status_led,   500, now);  /* 2 Hz */

    /* TODO: IWDG init with WATCHDOG_TIMEOUT_MS */
}

void agribot_loop(void)
{
    uint32_t now = 0; /* TODO: = HAL_GetTick(); */

    sched_run(&g_sched, now);

    /* TODO: HAL_IWDG_Refresh(&hiwdg); */
}

/*
 * STM32CubeMX generated main() should look like:
 *
 * int main(void)
 * {
 *     HAL_Init();
 *     SystemClock_Config();
 *     MX_GPIO_Init();
 *     MX_TIM1_Init();    // motor PWM
 *     MX_TIM2_Init();    // RC input capture
 *     MX_USART2_Init();  // Pi serial
 *     MX_USART3_Init();  // iBUS (if used)
 *     MX_ADC1_Init();    // battery voltage
 *     MX_IWDG_Init();    // watchdog
 *
 *     agribot_init();
 *
 *     while (1)
 *     {
 *         agribot_loop();
 *     }
 * }
 */
