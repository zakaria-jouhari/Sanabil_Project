#ifndef APP_SCHEDULER_H
#define APP_SCHEDULER_H

/*
 * Very Small Scheduler (Elecia White, Ch 5 p.146)
 *
 * Non-preemptive cooperative scheduler for periodic tasks.
 * Each task has a callback, a period, and a next-run time.
 * The scheduler runs in the main loop and fires tasks when due.
 *
 * Tasks must be short (non-blocking) since they cannot be preempted.
 */

#include <stdint.h>
#include <stdbool.h>

#define SCHED_MAX_TASKS 8

typedef void (*task_callback_t)(uint32_t now_ms);

typedef struct {
    task_callback_t callback;
    uint32_t period_ms;
    uint32_t next_run_at;
    bool enabled;
    const char *name;       /* for debug/logging */
} sched_task_t;

typedef struct {
    sched_task_t tasks[SCHED_MAX_TASKS];
    uint8_t count;
} scheduler_t;

void sched_init(scheduler_t *s);

/*
 * Register a periodic task. Returns task index, or -1 on failure.
 */
int8_t sched_add(scheduler_t *s, const char *name,
                 task_callback_t cb, uint32_t period_ms, uint32_t now_ms);

void sched_enable(scheduler_t *s, uint8_t task_id, bool enable);

/*
 * Call from main loop. Runs all tasks whose time has come.
 */
void sched_run(scheduler_t *s, uint32_t now_ms);

#endif /* APP_SCHEDULER_H */
