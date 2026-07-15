#include "app_scheduler.h"

void sched_init(scheduler_t *s)
{
    s->count = 0;
    for (uint8_t i = 0; i < SCHED_MAX_TASKS; i++) {
        s->tasks[i].callback = (task_callback_t)0;
        s->tasks[i].enabled = false;
    }
}

int8_t sched_add(scheduler_t *s, const char *name,
                 task_callback_t cb, uint32_t period_ms, uint32_t now_ms)
{
    if (s->count >= SCHED_MAX_TASKS) return -1;
    if (!cb) return -1;

    uint8_t id = s->count;
    s->tasks[id].name = name;
    s->tasks[id].callback = cb;
    s->tasks[id].period_ms = period_ms;
    s->tasks[id].next_run_at = now_ms + period_ms;
    s->tasks[id].enabled = true;
    s->count++;
    return (int8_t)id;
}

void sched_enable(scheduler_t *s, uint8_t task_id, bool enable)
{
    if (task_id < s->count)
        s->tasks[task_id].enabled = enable;
}

void sched_run(scheduler_t *s, uint32_t now_ms)
{
    for (uint8_t i = 0; i < s->count; i++) {
        sched_task_t *t = &s->tasks[i];
        if (!t->enabled) continue;

        /* Handles uint32 rollover correctly via unsigned subtraction */
        if ((int32_t)(now_ms - t->next_run_at) >= 0) {
            t->callback(now_ms);
            t->next_run_at += t->period_ms;

            /* If we fell behind, snap forward instead of running catch-up */
            if ((int32_t)(now_ms - t->next_run_at) >= 0) {
                t->next_run_at = now_ms + t->period_ms;
            }
        }
    }
}
