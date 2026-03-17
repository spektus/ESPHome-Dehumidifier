#pragma once

#include <vector>
#include <string>
#include <cstdint>
#include <cstddef>

namespace esphome {
namespace midea_dehum {

// Extracts capabilities from the raw packet into human-readable strings.
// This function is purely deterministic and thus easy to unit test.
std::vector<std::string> parse_capabilities(const uint8_t *data, size_t length, bool device_info_known, uint8_t appliance_type);

}  // namespace midea_dehum
}  // namespace esphome
