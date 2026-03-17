#include "components/midea_dehum/midea_dehum_utils.h"
#include <iostream>

using esphome::midea_dehum::crc8;
using esphome::midea_dehum::checksum;

void assert_eq(uint8_t expected, uint8_t actual, const char* name) {
    if (expected != actual) {
        std::cerr << "Test failed: " << name << " -> Expected: " << (int)expected << ", Actual: " << (int)actual << std::endl;
        exit(1);
    }
}

int main() {
    std::cout << "Running crc8 tests..." << std::endl;

    // Edge case 1: Empty input
    uint8_t dummy = 0;
    assert_eq(0x00, crc8(&dummy, 0), "Empty input");

    // Edge case 2: Single zero byte
    uint8_t zero = 0x00;
    assert_eq(0x00, crc8(&zero, 1), "Single zero byte");

    // Edge case 3: Single non-zero bytes
    uint8_t one = 0x01;
    assert_eq(0x5E, crc8(&one, 1), "Single byte 0x01");

    uint8_t aa = 0xAA;
    assert_eq(0xD1, crc8(&aa, 1), "Single byte 0xAA");

    uint8_t ff = 0xFF;
    assert_eq(0x35, crc8(&ff, 1), "Single byte 0xFF");

    // Edge case 4: Multiple bytes
    uint8_t all_ones[] = {0xFF, 0xFF, 0xFF};
    assert_eq(0x66, crc8(all_ones, 3), "Multiple bytes 0xFF");

    uint8_t mixed[] = {0x00, 0x5E, 0x00};
    assert_eq(0xAB, crc8(mixed, 3), "Mixed bytes");

    // Realistic payload extracted from device traffic
    uint8_t cmd[] = {
        0x41, 0x81, 0x00, 0xff, 0x03, 0xff,
        0x00, 0x02, 0x00, 0x00, 0x00
    };
    assert_eq(0x3D, crc8(cmd, sizeof(cmd)), "Realistic payload");

    std::cout << "All tests passed!" << std::endl;
    return 0;
}
