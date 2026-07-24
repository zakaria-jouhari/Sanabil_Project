# MerKal

**Autonomous crop-row navigation for the 90% of farms robotics companies ignore.**

MerKal is a low-cost autonomous ground robot that stays in the row when GPS can't. It fuses commodity GPS, IMU, and a single RGB camera — no RTK, no cellular dependency — to deliver centimeter-class in-row tracking on hardware a small or mid-size Moroccan farm can actually afford.

[![Status](https://img.shields.io/badge/status-prototype%20%7C%20bench%20integration-C06A3E)](#roadmap)
[![Stack](https://img.shields.io/badge/stack-ROS%202%20%7C%20STM32%20%7C%20Raspberry%20Pi-3F9457)](#hardware)
[![License](https://img.shields.io/badge/platform-PRBonn%2Fagribot%20(BSD--2--Clause)-2A2724)](https://github.com/PRBonn/agribot)

<p align="center"><img src="assets/merkal-lockup-on-dark.svg" width="480" alt="MerKal — Navigating the Land"></p>

---

## The problem

GPS fails exactly where precision matters most.

| | |
|---|---|
| **30–75 cm** | typical row spacing (cereals → maize) |
| **×10 to ×50** | GPS error growth, fix → degraded float |
| **1,200 ha** | scale of a real visited estate with weak cellular coverage |

RTK-float error (~50 cm) can exceed the entire row spacing — the difference between a clean pass and a robot driving over the crop. Existing commercial ag-robots automate harvesting, weeding, and spraying, but are priced for large capitalized operations, not the small Moroccan exploitant.

## The solution

Fuse everything cheap; let vision cover for GPS when it degrades.

- **Sensors:** GPS + IMU + wheel odometry + one RGB camera. No RTK hardware.
- **EKF** fuses all three into a single pose estimate, weighted by measurement confidence.
- **U-Net row detector** injects a vision-based lateral correction when GPS drifts.
- **Pure Pursuit** executes a planned lawnmower path, row by row.
- Graceful degradation: vision compensates when GPS is bad, never interferes when GPS is good.

| | |
|---|---|
| **~3 cm** | EKF pose accuracy (good localization) |
| **4.35 cm** | measured in-row lateral tracking |
| **0.78 IoU** | U-Net row-detector validation |

## Validated in simulation first

Full Gazebo/ROS 2 simulation-first pipeline — robot, sensors, and crop field modeled to run hundreds of paths under controlled GPS degradation (injected noise + bias) before any hardware risk. **Result:** vision fusion improves in-row accuracy under GPS noise, with the gain growing as noise increases — directly reducing technical risk ahead of field trials.

![Simulation run](docs/images/sim_demo.png)
![U-Net architecture](docs/images/unet_arch.png)

## Market — confirmed on the ground, not on paper

Two field visits and direct interviews (March 2026) with operators of very different scale:

| | Small farm | Large estate |
|---|---|---|
| Profile | Mixed crops | ~1,200 ha, orange groves |
| Priority task | Seasonal manual weeding | Orchard clearing, pruning |
| Price anchor | Worker wage ~4,500 DH/mo | Announced budget ~70–80k DH |
| Purchase condition | Live on-site demo | Live on-site demo |

Both operators evaluate the machine against the labor cost it replaces — not its technical sophistication.

## Why now — the gap is accessibility, not technology

| Approach | Strength | Limit |
|---|---|---|
| High-end RTK only | Centimeter precision, simple global reference | Thousands of dollars; still fails under obstruction / correction loss |
| Vision only | No satellite dependency, cheap sensor | Fragile in occluded/low-light rows, weak at row-end and row-switch |
| **GPS + IMU + odometry + vision (MerKal)** | Keeps a global reference, adds local correction, degrades gracefully, commodity sensors only | Needs calibration, measurement validation, failure handling |
| Commercial ag-robots | Proven, capable | Built for large capitalized operations only |

## Business model

Over 4 years, the labor a robot could replace is worth ~216,000 DH (4,500 DH/mo × 12 × 4) — the theoretical ceiling. A partially-assistive robot must price well under it.

| Band | Range | Read |
|---|---|---|
| Low-cost target | < 35,000 DH | Strong small-farm fit |
| Operator anchor | ~54,000 DH | ~1 year of wages over a 4-year life |
| Financing / service | 70,000–120,000 DH | Reachable via leasing or paid service |
| Above target | > 120,000 DH | Misaligned with small-farm budgets |

Avoiding survey-grade RTK hardware is the core economic decision — it keeps the sensor budget inside these bands while vision fusion recovers most of the lost precision. Given demo-before-buy behavior, a service, paid pilot, or leasing model likely beats direct sale.

## Hardware

Hoverboard BLDC drive + STM32 low-level control + Raspberry Pi 5 perception.

![System block diagram](docs/images/hw_block_diagram.png)

| Subsystem | Detail |
|---|---|
| Drive | 2× hoverboard BLDC motors (36 V) + 2 rear casters (differential) |
| Motor controllers | 2× ZS-X11H (6–60 V, 400 W, Hall commutation) |
| Motor power | 36 V hoverboard Li-ion (10S, 42 V max) — dedicated motor bus |
| Logic power | 80 W solar panel + 24 V battery → PWM charge controller → 2× LM2596 buck (Pi 5, STM32) |
| Compute | STM32F767ZI Nucleo (safety + motor control) · Raspberry Pi 5 (perception) |
| Sensors | RGB night-vision camera (CSI) · MPU6050 IMU |
| RC | FlySky i6 + FS-iA6B receiver (iBUS) |

**Firmware status:** iBUS RC reception ✅ verified (~135 frame/s, 0 errors) · Motor control ✅ full-vehicle teleoperation verified · Arm button ✅ implemented, testing pending.

<p align="center"><img src="docs/images/chassis_assembled.jpg" width="520" alt="Assembled chassis"></p>

## Roadmap

- [x] **V1 — RC teleoperation** — full-vehicle drive demonstrated
- [ ] **V2 — Autonomy handoff** — Pi `cmd_vel` over serial *(next)*
- [ ] **V3 — State estimation on hardware** — odometry + EKF
- [ ] **V4 — Vision-guided navigation** — closed-loop crop-row following

**Next milestone:** a lawnmower-pattern field demo, 2 rows, at a farm already visited.

## Traction

1. ✅ **Field research** — two real farm visits, need and price confirmed
2. ✅ **Simulation validated** — full navigation stack tested under controlled GPS degradation
3. 🔄 **Physical prototype** — chassis assembled, hardware integrated, bench integration in progress
4. ⏭ **Field demo** — next step

## Team

**Zakaria Jouhari** — Founder. Software (navigation, sensor fusion, vision) and hardware integration.
Electrical Engineering, Embedded Systems (ENSA Kénitra) · Research Engineer Intern, UM6P College of Computing · UM6P / OCP / OCP NutriCrops ecosystem.

Solo-founded at this stage — actively looking to build out the team across technical, business, and agronomy expertise.

## Repo structure

```
docs/         Figures and images
firmware/     STM32 firmware (V1 teleoperation)
software/     Raspberry Pi software + tools
hardware/     Schematics and wiring
```

---

*Mechanical platform adapted from [PRBonn/agribot](https://github.com/PRBonn/agribot) (BSD-2-Clause). Sensor-fusion design details are not shared publicly in this repository.*
