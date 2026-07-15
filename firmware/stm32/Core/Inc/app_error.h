#ifndef APP_ERROR_H
#define APP_ERROR_H

/*
 * Standardized error codes (Elecia White, Ch 3 "Dealing with Errors")
 *
 * Every module returns these codes. Error 0 is always success.
 * Callers can chain calls and check at the end:
 *   err = func_a(); if (err == ERR_NONE) err = func_b(); ...
 */

typedef enum {
    ERR_NONE = 0,
    ERR_UNKNOWN,
    ERR_BAD_PARAM,
    ERR_BAD_INDEX,
    ERR_UNINITIALIZED,
    ERR_TIMEOUT,
    ERR_BUSY,
    ERR_OVERFLOW,
    ERR_CHECKSUM,
    ERR_HAL,
    ERR_COUNT
} error_t;

#endif /* APP_ERROR_H */
