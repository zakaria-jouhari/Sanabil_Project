#include "drv_pi_serial.h"
#include "app_config.h"
#include "app_ringbuf.h"

/*
 * Pi Serial Protocol Driver
 *
 * Ring buffer (Ch 7): ISR pushes bytes, main loop pulls and parses.
 * Command pattern (Ch 3): message handlers registered in a dispatch table.
 * CRC16 for integrity (Ch 10).
 */

/* ---- Ring buffer ---- */

static uint8_t rx_buf_storage[PI_RX_BUF_SIZE];
static ringbuf_t rx_ring;

/* ---- Command dispatch table ---- */

static const pi_msg_dispatch_t *msg_table = (void *)0;
static uint8_t msg_table_count = 0;

/* ---- Packet parser state machine ---- */

typedef enum {
    PARSE_SYNC1,
    PARSE_SYNC2,
    PARSE_ID,
    PARSE_LEN,
    PARSE_PAYLOAD,
    PARSE_CRC_LO,
    PARSE_CRC_HI,
} parse_state_t;

static parse_state_t parse_state = PARSE_SYNC1;
static pi_packet_t parse_pkt;
static uint8_t parse_idx;
static uint16_t parse_crc;

/* ---- CRC-16/CCITT ---- */

static uint16_t crc16_update(uint16_t crc, uint8_t byte)
{
    crc ^= (uint16_t)byte << 8;
    for (uint8_t i = 0; i < 8; i++) {
        if (crc & 0x8000)
            crc = (crc << 1) ^ 0x1021;
        else
            crc <<= 1;
    }
    return crc;
}

static uint16_t crc16_block(const uint8_t *data, uint8_t len)
{
    uint16_t crc = 0xFFFF;
    for (uint8_t i = 0; i < len; i++)
        crc = crc16_update(crc, data[i]);
    return crc;
}

/* ---- Public API ---- */

error_t pi_serial_init(void)
{
    ringbuf_init(&rx_ring, rx_buf_storage, PI_RX_BUF_SIZE);
    parse_state = PARSE_SYNC1;

    /* TODO: HAL_UART_Receive_IT(&huartX, &rx_byte, 1); */
    return ERR_NONE;
}

void pi_serial_rx_byte(uint8_t byte)
{
    ringbuf_put(&rx_ring, byte);
}

void pi_serial_register_handlers(const pi_msg_dispatch_t *table, uint8_t count)
{
    msg_table = table;
    msg_table_count = count;
}

static void dispatch_packet(const pi_packet_t *pkt)
{
    if (!msg_table) return;

    for (uint8_t i = 0; i < msg_table_count; i++) {
        if (msg_table[i].msg_id == pkt->msg_id && msg_table[i].handler) {
            msg_table[i].handler(pkt);
            return;
        }
    }
    /* Unknown message ID - silently ignore (graceful degradation) */
}

error_t pi_serial_process(void)
{
    uint8_t byte;

    while (ringbuf_get(&rx_ring, &byte)) {
        switch (parse_state) {
        case PARSE_SYNC1:
            if (byte == PI_PACKET_START1) parse_state = PARSE_SYNC2;
            break;

        case PARSE_SYNC2:
            if (byte == PI_PACKET_START2) {
                parse_state = PARSE_ID;
            } else {
                parse_state = PARSE_SYNC1;
            }
            break;

        case PARSE_ID:
            parse_pkt.msg_id = byte;
            parse_state = PARSE_LEN;
            break;

        case PARSE_LEN:
            if (byte > PI_MAX_PAYLOAD) {
                parse_state = PARSE_SYNC1;
                break;
            }
            parse_pkt.len = byte;
            parse_idx = 0;
            if (byte == 0)
                parse_state = PARSE_CRC_LO;
            else
                parse_state = PARSE_PAYLOAD;
            break;

        case PARSE_PAYLOAD:
            parse_pkt.payload[parse_idx++] = byte;
            if (parse_idx >= parse_pkt.len)
                parse_state = PARSE_CRC_LO;
            break;

        case PARSE_CRC_LO:
            parse_crc = byte;
            parse_state = PARSE_CRC_HI;
            break;

        case PARSE_CRC_HI: {
            parse_crc |= (uint16_t)byte << 8;
            parse_state = PARSE_SYNC1;

            /* Verify CRC over [msg_id, len, payload] */
            uint8_t crc_buf[2 + PI_MAX_PAYLOAD];
            crc_buf[0] = parse_pkt.msg_id;
            crc_buf[1] = parse_pkt.len;
            for (uint8_t i = 0; i < parse_pkt.len; i++)
                crc_buf[2 + i] = parse_pkt.payload[i];

            uint16_t expected = crc16_block(crc_buf, 2 + parse_pkt.len);
            if (parse_crc == expected) {
                dispatch_packet(&parse_pkt);
                return ERR_NONE;
            }
            return ERR_CHECKSUM;
        }
        }
    }
    return ERR_BUSY; /* no complete packet yet */
}

error_t pi_serial_send(uint8_t msg_id, const uint8_t *payload, uint8_t len)
{
    if (len > PI_MAX_PAYLOAD) return ERR_BAD_PARAM;

    /* Build CRC over [msg_id, len, payload] */
    uint8_t crc_buf[2 + PI_MAX_PAYLOAD];
    crc_buf[0] = msg_id;
    crc_buf[1] = len;
    for (uint8_t i = 0; i < len; i++)
        crc_buf[2 + i] = payload[i];
    uint16_t crc = crc16_block(crc_buf, 2 + len);

    /* TODO: Replace with actual HAL UART transmit
     * uint8_t header[4] = { PI_PACKET_START1, PI_PACKET_START2, msg_id, len };
     * uint8_t footer[2] = { crc & 0xFF, crc >> 8 };
     * HAL_UART_Transmit(&huartX, header, 4, 10);
     * if (len > 0) HAL_UART_Transmit(&huartX, payload, len, 10);
     * HAL_UART_Transmit(&huartX, footer, 2, 10);
     */

    (void)crc;
    return ERR_NONE;
}
