#ifndef APP_RINGBUF_H
#define APP_RINGBUF_H

/*
 * Circular (ring) buffer (Elecia White, Ch 7)
 *
 * ISR-safe single-producer / single-consumer ring buffer.
 * Producer writes via ringbuf_put(), consumer reads via ringbuf_get().
 * No locking needed when one side is ISR and the other is main loop,
 * as long as head is only written by producer and tail by consumer.
 *
 * Size MUST be a power of 2 for fast masking.
 */

#include <stdint.h>
#include <stdbool.h>

typedef struct {
    uint8_t *buf;
    uint16_t size;      /* must be power of 2 */
    volatile uint16_t head;  /* written by producer (ISR) */
    volatile uint16_t tail;  /* written by consumer (main) */
} ringbuf_t;

static inline void ringbuf_init(ringbuf_t *rb, uint8_t *buffer, uint16_t size)
{
    rb->buf = buffer;
    rb->size = size;
    rb->head = 0;
    rb->tail = 0;
}

static inline uint16_t ringbuf_count(const ringbuf_t *rb)
{
    return (uint16_t)(rb->head - rb->tail) & (rb->size - 1);
}

static inline uint16_t ringbuf_free(const ringbuf_t *rb)
{
    return (rb->size - 1) - ringbuf_count(rb);
}

static inline bool ringbuf_is_empty(const ringbuf_t *rb)
{
    return rb->head == rb->tail;
}

static inline bool ringbuf_is_full(const ringbuf_t *rb)
{
    return ringbuf_count(rb) == (rb->size - 1);
}

static inline bool ringbuf_put(ringbuf_t *rb, uint8_t byte)
{
    if (ringbuf_is_full(rb)) return false;
    rb->buf[rb->head & (rb->size - 1)] = byte;
    rb->head++;
    return true;
}

static inline bool ringbuf_get(ringbuf_t *rb, uint8_t *byte)
{
    if (ringbuf_is_empty(rb)) return false;
    *byte = rb->buf[rb->tail & (rb->size - 1)];
    rb->tail++;
    return true;
}

static inline uint8_t ringbuf_peek(const ringbuf_t *rb, uint16_t offset)
{
    return rb->buf[(rb->tail + offset) & (rb->size - 1)];
}

#endif /* APP_RINGBUF_H */
