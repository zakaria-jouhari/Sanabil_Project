#ifndef APP_STATE_MACHINE_H
#define APP_STATE_MACHINE_H

/*
 * Table-Driven State Machine (Elecia White, Ch 6 p.161)
 *
 * Instead of a switch/case with embedded transition logic,
 * we use a transition table: an array of {state, guard, next_state}
 * rows. The table is scanned top-to-bottom; the first matching
 * guard wins. This makes transitions explicit, auditable, and
 * easy to extend for V2+.
 *
 * Each state also has optional entry/exit actions via function
 * pointers in a state-descriptor table.
 */

#include <stdint.h>
#include <stdbool.h>

typedef enum {
    STATE_BOOT = 0,
    STATE_DISARMED,
    STATE_ARMED_MANUAL,
    STATE_ARMED_AUTO,
    STATE_FAULT,
    STATE_COUNT
} robot_state_t;

/* Snapshot of all inputs evaluated each cycle */
typedef struct {
    bool rc_valid;
    bool rc_armed;
    bool rc_mode_auto;
    bool pi_alive;
    bool estop_active;
    uint16_t battery_mv;
} sm_inputs_t;

typedef struct {
    robot_state_t state;
    uint16_t fault_flags;
    uint32_t state_enter_tick;
    bool motors_enabled;
} state_machine_t;

void sm_init(state_machine_t *sm);

/*
 * Evaluate inputs, update faults, and run the transition table.
 * tick: current HAL_GetTick() value.
 */
void sm_update(state_machine_t *sm, const sm_inputs_t *inputs, uint32_t tick);

robot_state_t sm_get_state(const state_machine_t *sm);
uint16_t sm_get_faults(const state_machine_t *sm);
bool sm_motors_allowed(const state_machine_t *sm);
const char *sm_state_name(robot_state_t s);

#endif /* APP_STATE_MACHINE_H */
