<p align="center">
  <img src="assets/merkal-icon-color-on-dark.svg" width="88" alt="MerKal">
</p>

<h1 align="center">MerKal</h1>
<p align="center"><strong>Navigating the Land · ⴰⴽⴰⵍ</strong></p>
<p align="center">Autonomous crop-row navigation for the farms robotics companies have priced out.</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-prototype%20%2F%20bench%20integration-C06A3E" alt="status">
  <img src="https://img.shields.io/badge/stack-ROS%202%20%C2%B7%20STM32%20%C2%B7%20Raspberry%20Pi-3F9457" alt="stack">
  <img src="https://img.shields.io/badge/platform-PRBonn%2Fagribot%20(BSD--2--Clause)-2A2724" alt="license">
</p>

<p align="center">
  <img src="assets/merkal-lockup-on-dark.svg" width="520" alt="MerKal lockup">
</p>

---

### The problem

GPS fails exactly where precision is non-negotiable. RTK-grade accuracy collapses in the field: trees, metal structures, and correction-link dropouts degrade a centimeter-precise signal into an error of tens of centimeters. Row spacing runs 30 to 75 cm depending on crop, so a degraded fix can exceed the entire gap between rows. A visited 1,200 ha estate has weak cellular coverage, ruling out any solution that depends on a permanent network link. Commercial ag-robots already automate harvesting, weeding, and spraying, but for large, capitalized operations, out of reach for the small and mid-size Moroccan farm.

| Metric | Value |
|---|---|
| Row spacing (cereals to maize) | 30 to 75 cm |
| GPS error growth, fix to degraded float | 10x to 50x |
| Cellular coverage at a real visited estate | Weak, across 1,200 ha |

A 50 cm positioning gap under degraded GPS is comparable to, or larger than, the full row spacing of many crops. That is the difference between a negligible error and a robot driving over the crop.

### The solution

Fuse low-cost GPS, IMU, and vision to stay in the row.

- **Sensors**: GPS, IMU, wheel odometry, and one RGB camera. No RTK hardware.
- **Extended Kalman Filter** fuses GPS, IMU, and odometry into a single global pose estimate, weighted by the confidence of each measurement.
- **U-Net row detector** injects a row-relative position correction whenever the crop is visible and well formed.
- **Pure Pursuit** tracking executes a planned lawnmower path, row by row.
- **Graceful degradation**: vision compensates as GPS worsens, and never interferes when GPS is already good.

| Metric | Value |
|---|---|
| Pose accuracy (EKF, good localization) | ~3 cm |
| Measured in-row lateral tracking | 4.35 cm |
| U-Net row-detector validation | 0.78 IoU |

### Validated in simulation before touching hardware

A simulation-first methodology in Gazebo and ROS 2: the robot, its sensors, and a crop field are modeled to test hundreds of runs before any field trial, under controlled, injected GPS degradation. The key result: vision fusion improves in-row accuracy under random GPS noise, with the gain increasing alongside the noise level, cutting technical risk before the move to the field.

<p align="center">
  <img src="docs/images/sim_demo.png" width="640" alt="Simulated crop-row run in Gazebo">
</p>
<p align="center">
  <img src="docs/images/unet_arch.png" width="640" alt="U-Net row-detector architecture">
</p>

### Market: confirmed in the field, not at a desk

Two field visits and direct interviews, March 2026, with operators at very different scales, set the priorities and the price a real buyer will actually pay.

| | Small farm | Large estate |
|---|---|---|
| Scale / crop | Mixed crops | ~1,200 ha, orange groves |
| Priority task | Seasonal manual weeding | Orchard clearing, pruning |
| Price anchor | Worker wage, ~4,500 DH/month | Stated budget, ~70 to 80k DH |
| Purchase condition | Live on-site demo | Live on-site demo |

Both operators judge the machine against the cost of the labor it replaces, not against its technical sophistication.

### Why now: the gap is accessibility, not capability

Agricultural robotics already exists at scale, built for heavily capitalized operations. What the field visits surfaced is the absence of an affordable, field-robust option for the small and mid-size farmer.

| Approach | Strength | Limit |
|---|---|---|
| High-end RTK alone | Centimeter precision, simple global reference | Costs thousands of dollars; still fails under obstruction and correction loss |
| Vision alone | No satellite dependency, low-cost sensor | Fragile in occluded or poorly lit rows; weak at row-end and row-switch |
| GPS + IMU + odometry + vision, MerKal's approach | Keeps a global reference, adds a local correction, degrades gracefully, low-cost sensors only | Needs calibration, measurement validation, failure handling |
| Commercial robots for large operations | Proven at scale | Not viable for small and mid-size holdings |

### Business model

Over four years, the labor a robot would replace is worth roughly 216,000 DH (4,500 DH/month x 12 x 4). That is the theoretical ceiling; a robot that only partially assists needs to land well below it.

| Band | Range | Read |
|---|---|---|
| Low-cost target | Under 35,000 DH | Strong fit for small farms |
| Operator anchor | ~54,000 DH | About one year of wages over a four-year life |
| Financing / service | 70,000 to 120,000 DH | Reachable through leasing or a paid service |
| Above target | Over 120,000 DH | Not aligned with a small farm's budget |

Avoiding survey-grade RTK hardware, worth thousands of dollars, is the central economic decision: it keeps the sensor budget inside these bands while vision fusion recovers most of the precision that decision gives up. Because a live field demo is a purchase condition, a service, paid pilot, or leasing model is likely a better fit than a direct sale, especially for the small operator, for whom upfront cost is the main barrier.

### Hardware

A hoverboard BLDC drivetrain, an STM32 safety and motor-control core, and a Raspberry Pi 5 perception stack.

<p align="center">
  <img src="docs/images/hw_block_diagram.png" width="640" alt="System block diagram">
</p>

| Subsystem | Detail |
|---|---|
| Drive | 2x hoverboard BLDC motors, 36 V, plus 2 rear casters, differential |
| Motor controllers | 2x ZS-X11H, 6 to 60 V, 400 W, Hall commutation |
| Motor power | 36 V hoverboard Li-ion (10S, 42 V max), dedicated motor bus |
| Logic power | 80 W solar panel and 24 V battery through a PWM charge controller into 2x LM2596 bucks (Pi 5, STM32) |
| Compute | STM32F767ZI Nucleo for safety and motor control; Raspberry Pi 5 for perception |
| Sensors | RGB night-vision camera (CSI), MPU6050 IMU |
| RC | FlySky i6 with FS-iA6B receiver, iBUS |

**Firmware status**: iBUS RC reception verified at approximately 135 frames per second with 0 errors. Motor control verified for full-vehicle teleoperation. Arm button implemented, testing pending.

<p align="center">
  <img src="docs/images/chassis_assembled.jpg" width="560" alt="Assembled chassis">
</p>

### Roadmap

- [x] **V1, RC teleoperation**: full-vehicle drive demonstrated
- [ ] **V2, autonomy handoff**: Pi `cmd_vel` over serial, in progress next
- [ ] **V3, state estimation on hardware**: odometry and EKF
- [ ] **V4, vision-guided navigation**: closed-loop crop-row following

**Next milestone**: a lawnmower-pattern field demo across two rows, at a farm already visited.

### Traction

1. **Field research**, complete: two real farm visits, need and price confirmed
2. **Simulation validated**, complete: full navigation stack tested under controlled GPS degradation
3. **Physical prototype**, in progress: chassis assembled, hardware integrated, bench testing underway
4. **Field demo**, next step

### Team

**Zakaria Jouhari**, founder. Software (navigation, sensor fusion, vision) and hardware integration.
Electrical Engineering, Embedded Systems, ENSA Kenitra. Research Engineer Intern, UM6P College of Computing. Part of the UM6P / OCP / OCP NutriCrops ecosystem.

Solo-founded at this stage, and building out the team across technical, business, and agronomy expertise is a current priority.

### Repository structure

```
docs/         Figures and images
firmware/     STM32 firmware (V1 teleoperation)
software/     Raspberry Pi software and tools
hardware/     Schematics and wiring
```

---

<p align="center">Mechanical platform adapted from <a href="https://github.com/PRBonn/agribot">PRBonn/agribot</a> (BSD-2-Clause). Sensor-fusion design details are not shared publicly in this repository.</p>
