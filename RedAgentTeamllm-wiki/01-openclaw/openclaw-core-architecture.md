# OpenClaw 核心架構

**創建時間:** 2026-04-24  
**來源:** https://github.com/mudrii/openclaw-docs/blob/main/ARCHITECTURE.md  
**狀態:** 🟢 完成  
**可信度:** 1.0

---

## 4 層架構

| 層 | 功能 | 技術 |
|----|------|------|
| **HAL** | 硬件抽象 | GPIO、I2C、ROS 2 |
| **Control** | 運動規劃 | PID、阻抗控制 |
| **Task** | 高等級任務 | 狀態機、Action |
| **API** | 外部集成 | REST、gRPC |

---

## 依賴

- ROS 2 Humble
- Eigen 3.4
- libgpiod
- Protobuf

---

## 實測命令

**構建:**
```bash
mkdir -p colcon_ws/src && cd colcon_ws/src
git clone https://github.com/mudrii/openclaw.git
cd .. && colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release
```

**驗證:**
```bash
source install/setup.bash
ros2 run openclaw_hal test_hal_connection
```

---

## 資產

- `08-genes/openclaw-build-command.gene.md`
- `08-genes/openclaw-hal-verification.gene.md`
- `09-capsules/openclaw-deploy-capsule.md`

---

**維護者:** Red Agent Team
