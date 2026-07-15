#ifndef APP_VERSION_H
#define APP_VERSION_H

/*
 * Firmware version (Elecia White, Ch 3 "Command and Response")
 *
 * Embed version in binary so it can be queried over serial
 * and verified during bring-up. Update on every release.
 */

#define FW_VERSION_MAJOR    0
#define FW_VERSION_MINOR    1
#define FW_VERSION_PATCH    0
#define FW_VERSION_STRING   "0.1.0-v1-teleop"
#define FW_BUILD_TARGET     "STM32F767ZI"

#endif /* APP_VERSION_H */
