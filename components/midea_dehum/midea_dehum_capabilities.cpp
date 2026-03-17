#include "midea_dehum_capabilities.h"
#include <cstdio>

namespace esphome {
namespace midea_dehum {

struct CapabilityMap {
  uint8_t id;
  uint8_t type;
  const char* name;
};

// Combined table — documented + dehumidifier findings
static const CapabilityMap CAPABILITY_TABLE[] = {
  // ───── Documented standard capabilities ─────
  {0x10, 0x02, "Fan speed control"},
  {0x12, 0x02, "ECO mode"},
  {0x13, 0x02, "8°C heating / freeze protection"},
  {0x14, 0x02, "Mode selection"},
  {0x15, 0x02, "Swing control"},
  {0x16, 0x02, "Power consumption / calibration"},
  {0x17, 0x02, "Filter reminder"},
  {0x18, 0x02, "No-wind comfort / silky cool"},
  {0x19, 0x02, "PTC heater / aux heating"},
  {0x1A, 0x02, "Turbo fan / strong mode"},
  {0x1E, 0x02, "Ionizer"},
  {0x1F, 0x02, "Auto humidity control"},
  {0x21, 0x02, "Filter check"},
  {0x22, 0x02, "Temperature Unit Changeable"},
  {0x24, 0x02, "Display / light control"},
  {0x25, 0x02, "Temperature range"},
  {0x2A, 0x02, "Strong fan (alt)"},
  {0x2C, 0x02, "Buzzer / beep control"},

  // ───── Dehumidifier / B5-specific capabilities ─────
  {0x1D, 0x02, "Drain pump control"},
  {0x20, 0x02, "Clothes Drying"},
  {0x2D, 0x02, "Water level sensor"},

  // ───── Sensor / structural presence capabilities (type 0x00) ─────
  {0x09, 0x00, "Vertical swing support"},
  {0x0A, 0x00, "Horizontal swing support"},
  {0x15, 0x00, "Indoor humidity sensor"},
  {0x18, 0x00, "No wind feel mode"},
  {0x30, 0x00, "Smart eye / energy save on absence"},
  {0x32, 0x00, "Blowing people"},
  {0x33, 0x00, "Avoid people"},
  {0x39, 0x00, "Self-cleaning"},
  {0x42, 0x00, "Voice control"},
  {0x43, 0x00, "Light sensor"},

  // Added based on observations
  {0x11, 0x02, "Continuous mode"},
  {0x14, 0x00, "Device type / capability profile"},
  {0x1A, 0x00, "Error code history / diag"},
  {0x1A, 0x03, "Secondary diagnostic"},
  {0x30, 0x02, "Filter clean status"},
  {0x33, 0x02, "Tank status / pump control"},
  {0x40, 0x00, "PM2.5 sensor presence"},
  {0x44, 0x00, "Light / display control"}
};

std::vector<std::string> parse_capabilities(const uint8_t *data, size_t length, bool device_info_known, uint8_t appliance_type) {
  std::vector<std::string> caps;
  if (length < 14) return caps;

  size_t i = 12;
  while (i + 3 < length - 1) {
    uint8_t id   = data[i];
    uint8_t type = data[i + 1];
    uint8_t len  = data[i + 2];
    uint8_t val  = data[i + 3];

    if (i + 3 + len > length) break;

    const char *name = nullptr;
    for (const auto &entry : CAPABILITY_TABLE) {
      if (entry.id == id && entry.type == type) {
        name = entry.name;
        break;
      }
    }

    std::string desc;
    if (name != nullptr) {
      desc = name;

      // Decode multi-valued capabilities
      switch (id) {
        case 0x14: {  // Mode selection
          std::string mode_str;
          switch (val) {
            case 0: mode_str = "Cool+Dry+Auto"; break;
            case 1: mode_str = "Cool+Heat+Dry+Auto"; break;
            case 2: mode_str = "Heat+Auto"; break;
            case 3: mode_str = "Cool only"; break;
            default: mode_str = "Unknown"; break;
          }
          desc += " → " + mode_str;
          break;
        }

        case 0x15: {  // Swing control
          std::string sw;
          switch (val) {
            case 0: sw = "Up/Down"; break;
            case 1: sw = "Both directions"; break;
            case 2: sw = "None"; break;
            case 3: sw = "Left/Right only"; break;
            default: sw = "Unknown"; break;
          }
          desc += " → " + sw;
          break;
        }

        case 0x16: {  // Power calibration
          switch (val) {
            case 2: desc += " → Calibration supported"; break;
            case 3: desc += " → Calibration+Setting supported"; break;
            default: desc += " → Not supported"; break;
          }
          break;
        }

        case 0x1A: {  // Turbo
          switch (val) {
            case 0: desc += " → Cool only"; break;
            case 1: desc += " → Heat+Cool"; break;
            case 2: desc += " → Disabled"; break;
            case 3: desc += " → Heat only"; break;
            default: desc += " → Unknown"; break;
          }
          break;
        }

        case 0x1F: {  // Humidity control
          if (device_info_known && appliance_type == 0xA1) {
            // Dehumidifier-specific interpretation
            switch (val) {
              case 0: desc += " → None"; break;
              case 1: desc += " → Manual + Auto"; break;
              case 2: desc += " → val2"; break;
              case 3: desc += " → val3"; break;
              default: desc += " → Unknown"; break;
            }
          } else {
            // Default (AC or other appliance type)
            switch (val) {
              case 0: desc += " → None"; break;
              case 1: desc += " → Auto only"; break;
              case 2: desc += " → Auto+Manual"; break;
              case 3: desc += " → Manual only"; break;
              default: desc += " → Unknown"; break;
            }
          }
          break;
        }

        case 0x25: {  // Temperature range (multi-value)
          if (len >= 6) {
            float min_cool = data[i + 3] / 2.0f;
            float max_cool = data[i + 4] / 2.0f;
            float min_auto = data[i + 5] / 2.0f;
            float max_auto = data[i + 6] / 2.0f;
            float min_heat = data[i + 7] / 2.0f;
            float max_heat = data[i + 8] / 2.0f;
            char buf[128];
            snprintf(buf, sizeof(buf),
                     " → Cool %.1f–%.1f°C, Auto %.1f–%.1f°C, Heat %.1f–%.1f°C",
                     min_cool, max_cool, min_auto, max_auto, min_heat, max_heat);
            desc += buf;
          } else {
            desc += " → Invalid range";
          }
          break;
        }

        default:
          // Generic numeric output for unknown value meanings
          {
            char buf[16];
            snprintf(buf, sizeof(buf), " (val=%u)", val);
            desc += buf;
          }
          break;
      }

      caps.push_back(desc);
    }

    i += 3 + len;
  }

  if (caps.empty())
    caps.push_back("No capabilities detected");

  return caps;
}

}  // namespace midea_dehum
}  // namespace esphome
