#define CATCH_CONFIG_MAIN
#include "catch.hpp"
#include "midea_dehum_capabilities.h"

using namespace esphome::midea_dehum;

TEST_CASE("parse_capabilities edge cases", "[midea_dehum_capabilities]") {
    SECTION("Short packet returns empty capabilities") {
        uint8_t data[] = {1, 2, 3};
        auto caps = parse_capabilities(data, sizeof(data), false, 0);
        REQUIRE(caps.empty());
    }

    SECTION("Packet with no valid capabilities returns 'No capabilities detected'") {
        uint8_t data[14] = {0};
        auto caps = parse_capabilities(data, sizeof(data), false, 0);
        REQUIRE(caps.size() == 1);
        REQUIRE(caps[0] == "No capabilities detected");
    }

    SECTION("Out of bounds capability length is handled safely") {
        uint8_t data[] = {
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // padding to index 12
            0x14, 0x02, 100, 0, // id=0x14, type=0x02, len=100 (way too large)
            0 // end
        };
        auto caps = parse_capabilities(data, sizeof(data), false, 0);
        REQUIRE(caps.size() == 1);
        REQUIRE(caps[0] == "No capabilities detected");
    }
}

TEST_CASE("parse_capabilities decodes standard capabilities", "[midea_dehum_capabilities]") {
    SECTION("Mode selection (id=0x14, type=0x02)") {
        uint8_t data[] = {
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0x14, 0x02, 1, 0, // Cool+Dry+Auto
            0
        };
        auto caps = parse_capabilities(data, sizeof(data), false, 0);
        REQUIRE(caps.size() == 1);
        REQUIRE(caps[0] == "Mode selection → Cool+Dry+Auto");

        data[15] = 1;
        caps = parse_capabilities(data, sizeof(data), false, 0);
        REQUIRE(caps[0] == "Mode selection → Cool+Heat+Dry+Auto");
    }

    SECTION("Swing control (id=0x15, type=0x02)") {
        uint8_t data[] = {
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0x15, 0x02, 1, 2, // None
            0
        };
        auto caps = parse_capabilities(data, sizeof(data), false, 0);
        REQUIRE(caps.size() == 1);
        REQUIRE(caps[0] == "Swing control → None");
    }

    SECTION("Auto humidity control (id=0x1F, type=0x02)") {
        uint8_t data[] = {
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0x1F, 0x02, 1, 1,
            0
        };

        // As AC (default)
        auto caps_ac = parse_capabilities(data, sizeof(data), false, 0);
        REQUIRE(caps_ac.size() == 1);
        REQUIRE(caps_ac[0] == "Auto humidity control → Auto only");

        // As Dehumidifier
        auto caps_dehum = parse_capabilities(data, sizeof(data), true, 0xA1);
        REQUIRE(caps_dehum.size() == 1);
        REQUIRE(caps_dehum[0] == "Auto humidity control → Manual + Auto");
    }

    SECTION("Temperature range (id=0x25, type=0x02)") {
        uint8_t data[] = {
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0x25, 0x02, 6, 32, 60, 32, 60, 34, 60, // 16C-30C
            0
        };
        auto caps = parse_capabilities(data, sizeof(data), false, 0);
        REQUIRE(caps.size() == 1);
        REQUIRE(caps[0] == "Temperature range → Cool 16.0–30.0°C, Auto 16.0–30.0°C, Heat 17.0–30.0°C");
    }

    SECTION("Multiple capabilities combined") {
        uint8_t data[] = {
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0x14, 0x02, 1, 0, // Mode
            0x15, 0x02, 1, 3, // Swing (Left/Right)
            0x40, 0x00, 1, 1, // PM2.5 sensor presence
            0
        };
        auto caps = parse_capabilities(data, sizeof(data), false, 0);
        REQUIRE(caps.size() == 3);
        REQUIRE(caps[0] == "Mode selection → Cool+Dry+Auto");
        REQUIRE(caps[1] == "Swing control → Left/Right only");
        REQUIRE(caps[2] == "PM2.5 sensor presence (val=1)");
    }
}
