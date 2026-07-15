#ifndef DRV_PI_SERIAL_H
#define DRV_PI_SERIAL_H

/*
 * Pi <-> STM32 Serial Protocol Driver
 *
 * Uses ring buffer (Elecia White, Ch 7) for ISR-safe UART RX,
 * and command pattern (Ch 3) for message dispatch.
 *
 * Frame format: [0xAA] [0x55] [msg_id] [len] [payload...] [crc16_lo] [crc16_hi]
 */

#include <stdint.h>
#include <stdbool.h>
#include "app_error.h"

#define PI_RX_BUF_SIZE  128     /* must be power of 2 */
#define PI_TX_BUF_SIZE  128
#define PI_MAX_PAYLOAD  32

/* Parsed packet */
typedef struct {
    uint8_t msg_id;
    uint8_t len;
    uint8_t payload[PI_MAX_PAYLOAD];
} pi_packet_t;

/* Message handler callback (command pattern: each msg_id has a handler) */
typedef void (*pi_msg_handler_t)(const pi_packet_t *pkt);

typedef struct {
    uint8_t msg_id;
    pi_msg_handler_t handler;
} pi_msg_dispatch_t;

error_t pi_serial_init(void);

/*
 * Call from UART RX ISR to feed received bytes into ring buffer.
 */
void pi_serial_rx_byte(uint8_t byte);

/*
 * Call from main loop to parse buffered data and dispatch messages.
 * Returns ERR_NONE if a complete packet was processed.
 */
error_t pi_serial_process(void);

/*
 * Send a packet to Pi.
 */
error_t pi_serial_send(uint8_t msg_id, const uint8_t *payload, uint8_t len);

/*
 * Register message handlers (command table).
 * table: array of {msg_id, handler} pairs, terminated by {0, NULL}.
 */
void pi_serial_register_handlers(const pi_msg_dispatch_t *table, uint8_t count);

#endif /* DRV_PI_SERIAL_H */
