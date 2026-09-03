<p align="center">
  <img src="assets/atelier-banner.svg"
       alt="Jonas Atelier embedded library workshop"
       width="100%">
</p>

<h1 align="center">Embedded Library Workshop</h1>

<p align="center">
  Portable C libraries and hardware projects, organized for quick discovery.
</p>

<p align="center">
  ✅ Available · 🧪 Hardware validation · 🚧 On-going · 🧭 Coming soon
</p>

<pre>
Jonas Atelier
├── ⚡ ESP32 / ESP-IDF
│   ├── Actuators
│   │   ├── esp-c620-control       — C620 motor control       🧪
│   │   ├── esp-tmc5240-stepper    — TMC5240 stepper driver   🧪
│   │   ├── esp-tmc2209-stepper    — TMC2209 stepper, UART    🚧
│   │   ├── esp-drv8323-gatedriver — DRV8323 BLDC gate driver 🚧
│   │   └── esp-pca9685-pwm        — PCA9685 16-ch PWM        🧪
│   │
│   ├── Sensors
│   │   ├── Motion &amp; Orientation
│   │   │   ├── esp-bmi088-imu   — BMI088 IMU interface    🧪
│   │   │   ├── esp-icm45686-imu — ICM-45686 IMU interface 🧪
│   │   │   ├── esp-mpu6050-imu  — MPU-6050 IMU interface  🧪
│   │   │   ├── esp-bno085-imu   — BNO085 IMU interface    🧭
│   │   │   └── esp-icm42688-imu — ICM-42688 IMU interface 🧭
│   │   │
│   │   ├── Magnetic Field
│   │   │   ├── esp-qmc5883l-mag — QMC5883L magnetometer  🧪
│   │   │   └── esp-mmc5983-mag  — MMC5983MA magnetometer 🧭
│   │   │
│   │   ├── Distance &amp; Ranging
│   │   │   ├── esp-ld06-lidar      — LD06 LiDAR interface    🧭
│   │   │   ├── esp-tfmini-lidar    — TFmini LiDAR interface  🧭
│   │   │   └── esp-vl53l1x-tof     — VL53L1X ToF sensor      🚧
│   │   │
│   │   ├── GNSS &amp; Navigation
│   │   │   └── esp-ublox-gnss   — u-blox M8/M10 GNSS  🧭
│   │   │
│   │   ├── Encoders
│   │   │   ├── esp-as5600-encoder  — AS5600 magnetic encoder   🚧
│   │   │   ├── esp-as5047p-encoder — AS5047P SPI encoder, FOC  🚧
│   │   │   ├── esp-amt102-encoder  — AMT102-V quadrature, PCNT 🚧
│   │   │   └── esp-as5048a-encoder — AS5048A magnetic encoder  🧭
│   │   │
│   │   ├── Pressure &amp; Altitude
│   │   │   └── esp-dps310-baro — DPS310 barometer 🧪
│   │   │
│   │   ├── Force &amp; Load
│   │   │   ├── esp-hx711-loadcell   — HX711 load cell amplifier 🧪
│   │   │   └── esp-nau7802-loadcell — NAU7802 bridge ADC, I2C   🧪
│   │   │
│   │   └── Power &amp; Battery
│   │       ├── esp-ina2xx-sensor      — INA2xx power monitor       🧪
│   │       ├── esp-max17048-fuelgauge — MAX17048 1S fuel gauge     🧪
│   │       └── esp-bq769x0-bms        — bq769x0 3-15S pack monitor 🧪
│   │
│   ├── Input &amp; Controllers
│   │   └── esp-ps-controller   — PS4/PS5 controller input  🧪
│   │
│   ├── I/O &amp; Bus Expansion
│   │   ├── esp-mcp23-expander — MCP23017 I/O expander    🚧
│   │   ├── esp-ads1115-adc    — ADS1115 4-ch 16-bit ADC  🧪
│   │   └── esp-tca9548a-mux   — TCA9548A I2C multiplexer 🧭
│   │
│   ├── Communications
│   │   ├── esp-sn65hvd230-can   — CAN transceiver driver  ✅  <a href="https://github.com/JonasAtelier/esp-sn65hvd230-can">🔗 GitHub</a>
│   │   └── esp-dw1000-uwb       — DW1000 UWB ranging      🧪
│   │
│   └── Camera
│       └── Coming soon 🧭
│
├── 🔷 STM32
│   └── Coming soon 🧭
│
├── ♾️ Arduino
│   └── Coming soon 🧭
│
├── 🐧 Linux
│   ├── Drivers
│   │   └── nv-ps-controller — PS4/PS5 controller input  🚧
│   │
│   ├── ROS2
│   │   └── rs-d455-camera — RealSense D455 camera  🧭
│   │
│   └── Communication
│       └── Robust — ROS2-style C framework  🚧
│
│   Prefix key: rs- = ROS2 · nv- = NVIDIA Jetson Linux · rasp- = Raspberry Pi
│
├── 🧰 General
│   ├── Control &amp; Algorithms
│   │   ├── upid — Portable PID control  ✅  <a href="https://github.com/JonasAtelier/upid">🔗 GitHub</a>
│   │   ├── fsm  — Finite state machines           🧪
│   │   ├── kin  — Forward/inverse kinematics      🧪
│   │   └── imp  — Impedance &amp; admittance control  🧪
│   │
│   └── Filters
│       ├── f_kalman        — Scalar Kalman filter  🧪
│       ├── f_complementary — Complementary filter  🧪
│       ├── f_particle      — Particle filter       🧪
│       └── f_hampel        — Hampel filtering      🧭
│
└── 🛠️ Misc
    ├── 🦅 Hawk    — Drone           🧭
    ├── 🐕 Dingo   — Robotic dog     🧭
    ├── 🕷️ Arachne — Spider robot    🧭
    ├── 🚚 Navis   — AGV             🧭
    ├── 🤖 Helios  — Humanoid robot  🧭
    └── 🦾 Jarvis  — Robotic arm     🧭
</pre>

<p align="center">
  Projects become clickable after hardware validation and public release.
  <br>
  Built in the
  <a href="https://github.com/JonasAtelier">Jonas Atelier</a> workshop.
</p>
