#include <iostream>
#include <vector>
#include <string>
#include <chrono>

void processPacketWithHexStr(uint8_t *data, size_t len) {
  std::string hex_str;
  hex_str.reserve(len * 3);
  for (size_t i = 0; i < len; i++) {
    char buf[4];
    snprintf(buf, sizeof(buf), "%02X ", data[i]);
    hex_str += buf;
  }
  // Simulate doing something with data to prevent optimization
  volatile uint8_t dummy = data[0];
}

void processPacketWithoutHexStr(uint8_t *data, size_t len) {
  // Simulate doing something with data to prevent optimization
  volatile uint8_t dummy = data[0];
}

int main() {
  std::vector<uint8_t> data(40, 0xAA);
  int iterations = 100000;

  auto start = std::chrono::high_resolution_clock::now();
  for (int i = 0; i < iterations; ++i) {
    processPacketWithHexStr(data.data(), data.size());
  }
  auto end = std::chrono::high_resolution_clock::now();
  auto duration_with = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();

  start = std::chrono::high_resolution_clock::now();
  for (int i = 0; i < iterations; ++i) {
    processPacketWithoutHexStr(data.data(), data.size());
  }
  end = std::chrono::high_resolution_clock::now();
  auto duration_without = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();

  std::cout << "With hex_str: " << duration_with << " us\n";
  std::cout << "Without hex_str: " << duration_without << " us\n";
  return 0;
}
