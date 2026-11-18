# Embedded Library Workshop

![Jonas Atelier embedded library workshop](assets/atelier-banner.svg)

Find C libraries and firmware for robots built with ESP32 and STM32. Each public project has its own setup instructions and examples.

## Pick a first project

| What would you like to try? | Start here |
| --- | --- |
| See a controller bring a simulated heater to a target temperature. All you need is a C compiler. | [UPID heater example](https://github.com/JonasAtelier/upid/blob/HEAD/examples/basic_pid.c) · [Build instructions](https://github.com/JonasAtelier/upid) |
| Exchange messages between an ESP32 and another device on a CAN bus. You’ll need a CAN transceiver and a second node. | [ESP32 CAN driver and wiring](https://github.com/JonasAtelier/esp-sn65hvd230-can) |

## What’s on the bench

These projects are in development or awaiting hardware validation. Drivers are grouped by job so an application can use the same interface with different chips.

<details>
<summary>Find a driver by part or task</summary>

| Task | Libraries and examples |
| --- | --- |
| Measure motion or direction | `mcu-imu` (MPU-6050, BMI088), `mcu-compass` (LIS3MDL, IST8310), `mcu-encoder` (AS5600, AS5047P) |
| Measure pressure, force or distance | `mcu-baro` (BMP280, MS5611), `mcu-loadcell` (HX711), `mcu-tof` (VL53L1X), `mcu-lidar` (LD19), `mcu-uwb` (DW1000) |
| Measure power or battery state | `mcu-powermon` (INA219, INA226), `mcu-battery` (MAX17048, BQ769x0) |
| Drive a motor | `mcu-stepper` (TMC2209), `mcu-esc` (C620), `mcu-servo` (PWM, PCA9685) |
| Connect controls and peripherals | `mcu-rc`, `mcu-gamecontroller`, `mcu-can`, `mcu-expander` |
| Add ESP32 peripherals | ADS1115 analog input, SSD1306 display, WS2812 LEDs, ESP-NOW radio, SD logging and Wi-Fi updates |

</details>

<details>
<summary>Explore algorithms and robot projects</summary>

| Area | Projects |
| --- | --- |
| Portable C algorithms | `algo-filter` for sensor estimates, `algo-control` for feedback loops, `algo-kinematics` for arm and wheel motion, `algo-motion` for path following, `algo-behavior` for robot decisions |
| Build tools | `esp-forge` builds ESP32 images with ESP-IDF. `stm-forge` builds STM32 images with the Arm GNU toolchain. |
| Robots and boards | Dingo quadruped, Nova swerve module, Flux motor drive, Hawk flight controller and Nexus power monitor |
| Linux | `nv-ps-controller` reads PlayStation gamepads. `Robust` is a robotics framework in C. |

</details>

Planned additions include a Hampel outlier filter, motion profiles, more sensor drivers and camera support.
