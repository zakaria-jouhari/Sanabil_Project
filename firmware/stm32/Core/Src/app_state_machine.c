#include "app_state_machine.h"
#include "app_config.h"

/*
 * Table-Driven State Machine (Elecia White, Ch 6)
 *
 * Transition table: scanned top-to-bottom per current state.
 * First matching guard function wins. This design makes the
 * state machine auditable -- you can read the table to know
 * exactly what transitions exist and under what conditions.
 */

/* ---- State name strings (for debug/telemetry) ---- */

static const char *state_names[STATE_COUNT] = {
    [STATE_BOOT]         = "BOOT",
    [STATE_DISARMED]     = "DISARMED",
    [STATE_ARMED_MANUAL] = "ARMED_MANUAL",
    [STATE_ARMED_AUTO]   = "ARMED_AUTO",
    [STATE_FAULT]        = "FAULT",
};

/* ---- Guard functions ---- */
/* Each returns true if the transition should fire. */

typedef struct {
    const sm_inputs_t *in;
    uint16_t faults;
    uint16_t critical;
} guard_ctx_t;

static bool guard_always(const guard_ctx_t *ctx)
{
    (void)ctx;
    return true;
}

static bool guard_critical_fault(const guard_ctx_t *ctx)
{
    return (ctx->faults & ctx->critical) != 0;
}

static bool guard_arm_ok(const guard_ctx_t *ctx)
{
    return ctx->in->rc_valid
        && ctx->in->rc_armed
        && !(ctx->faults & ctx->critical);
}

static bool guard_disarm(const guard_ctx_t *ctx)
{
    return !ctx->in->rc_valid || !ctx->in->rc_armed;
}

static bool guard_enter_auto(const guard_ctx_t *ctx)
{
    return ctx->in->rc_mode_auto && ctx->in->pi_alive;
}

static bool guard_exit_auto(const guard_ctx_t *ctx)
{
    return !ctx->in->rc_mode_auto || !ctx->in->pi_alive;
}

static bool guard_fault_clear(const guard_ctx_t *ctx)
{
    return !(ctx->faults & ctx->critical) && !ctx->in->rc_armed;
}

/* ---- Transition table ---- */

typedef bool (*guard_fn_t)(const guard_ctx_t *ctx);

typedef struct {
    robot_state_t from;
    guard_fn_t guard;
    robot_state_t to;
} sm_transition_t;

/*
 * Table ordering matters: earlier rows have higher priority.
 * Critical faults are checked first in every armed state.
 */
static const sm_transition_t transition_table[] = {
    /* BOOT -> DISARMED (unconditional after init) */
    { STATE_BOOT,         guard_always,         STATE_DISARMED },

    /* DISARMED: critical fault -> FAULT */
    { STATE_DISARMED,     guard_critical_fault,  STATE_FAULT },
    /* DISARMED: arm OK -> ARMED_MANUAL */
    { STATE_DISARMED,     guard_arm_ok,          STATE_ARMED_MANUAL },

    /* ARMED_MANUAL: critical fault -> FAULT (highest priority) */
    { STATE_ARMED_MANUAL, guard_critical_fault,  STATE_FAULT },
    /* ARMED_MANUAL: lost RC or disarmed -> DISARMED */
    { STATE_ARMED_MANUAL, guard_disarm,          STATE_DISARMED },
    /* ARMED_MANUAL: mode switch + Pi alive -> ARMED_AUTO */
    { STATE_ARMED_MANUAL, guard_enter_auto,      STATE_ARMED_AUTO },

    /* ARMED_AUTO: critical fault -> FAULT */
    { STATE_ARMED_AUTO,   guard_critical_fault,  STATE_FAULT },
    /* ARMED_AUTO: lost RC or disarmed -> DISARMED */
    { STATE_ARMED_AUTO,   guard_disarm,          STATE_DISARMED },
    /* ARMED_AUTO: mode manual or Pi dead -> fallback to manual */
    { STATE_ARMED_AUTO,   guard_exit_auto,       STATE_ARMED_MANUAL },

    /* FAULT: faults cleared + disarmed -> DISARMED */
    { STATE_FAULT,        guard_fault_clear,     STATE_DISARMED },
};

#define TRANSITION_COUNT (sizeof(transition_table) / sizeof(transition_table[0]))

/* ---- Entry actions ---- */

static void enter_state(state_machine_t *sm, robot_state_t new_state, uint32_t tick)
{
    sm->state = new_state;
    sm->state_enter_tick = tick;

    switch (new_state) {
    case STATE_DISARMED:
    case STATE_FAULT:
    case STATE_BOOT:
        sm->motors_enabled = false;
        break;
    case STATE_ARMED_MANUAL:
    case STATE_ARMED_AUTO:
        sm->motors_enabled = true;
        break;
    default:
        sm->motors_enabled = false;
        break;
    }
}

/* ---- Public API ---- */

void sm_init(state_machine_t *sm)
{
    sm->state = STATE_BOOT;
    sm->fault_flags = 0;
    sm->state_enter_tick = 0;
    sm->motors_enabled = false;
}

void sm_update(state_machine_t *sm, const sm_inputs_t *inputs, uint32_t tick)
{
    /* Compute fault flags from inputs */
    uint16_t faults = 0;

    if (inputs->estop_active)
        faults |= FAULT_ESTOP;
    if (!inputs->rc_valid)
        faults |= FAULT_RC_LOST;
    if (inputs->battery_mv > 0 && inputs->battery_mv < BATTERY_LOW_WARN_MV)
        faults |= FAULT_BATT_LOW;
    if (inputs->battery_mv > 0 && inputs->battery_mv < BATTERY_CRITICAL_MV)
        faults |= FAULT_BATT_CRITICAL;
    if (!inputs->pi_alive)
        faults |= FAULT_PI_TIMEOUT;

    sm->fault_flags = faults;

    /* Build guard context */
    uint16_t critical = FAULT_ESTOP | FAULT_BATT_CRITICAL;
    guard_ctx_t ctx = {
        .in = inputs,
        .faults = faults,
        .critical = critical,
    };

    /* Scan transition table: first matching guard wins */
    for (uint16_t i = 0; i < TRANSITION_COUNT; i++) {
        const sm_transition_t *tr = &transition_table[i];
        if (tr->from != sm->state) continue;
        if (tr->guard(&ctx)) {
            if (tr->to != sm->state) {
                enter_state(sm, tr->to, tick);
            }
            break;
        }
    }
}

robot_state_t sm_get_state(const state_machine_t *sm)
{
    return sm->state;
}

uint16_t sm_get_faults(const state_machine_t *sm)
{
    return sm->fault_flags;
}

bool sm_motors_allowed(const state_machine_t *sm)
{
    return sm->motors_enabled;
}

const char *sm_state_name(robot_state_t s)
{
    if (s < STATE_COUNT) return state_names[s];
    return "UNKNOWN";
}
