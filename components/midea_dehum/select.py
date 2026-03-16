import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import select
from . import midea_dehum_ns, CONF_MIDEA_DEHUM_ID

cg.add_define("USE_MIDEA_DEHUM_SELECT")

MideaDehum = midea_dehum_ns.class_("MideaDehumComponent", cg.Component)

MideaModeSelect = midea_dehum_ns.class_("MideaModeSelect", select.Select, cg.Component)
MideaFanSpeedSelect = midea_dehum_ns.class_("MideaFanSpeedSelect", select.Select, cg.Component)

CONF_MODE = "mode"
CONF_FAN_SPEED = "fan_speed"

CONFIG_SCHEMA = cv.Schema({
    cv.Required(CONF_MIDEA_DEHUM_ID): cv.use_id(MideaDehum),
    cv.Optional(CONF_MODE): select.select_schema(
        MideaModeSelect,
        icon="mdi:water-percent",
    ),
    cv.Optional(CONF_FAN_SPEED): select.select_schema(
        MideaFanSpeedSelect,
        icon="mdi:fan",
    ),
})

async def to_code(config):
    parent = await cg.get_variable(config[CONF_MIDEA_DEHUM_ID])

    if CONF_MODE in config:
        cg.add_define("USE_MIDEA_DEHUM_MODE_SELECT")
        mode_select = await select.new_select(
            config[CONF_MODE],
            options=["Setpoint", "Continuous", "Smart", "Clothes Drying"],
        )
        cg.add(parent.set_mode_select(mode_select))

    if CONF_FAN_SPEED in config:
        cg.add_define("USE_MIDEA_DEHUM_FAN_SPEED_SELECT")
        fan_speed_select = await select.new_select(
            config[CONF_FAN_SPEED],
            options=["Low", "Medium", "High"],
        )
        cg.add(parent.set_fan_speed_select(fan_speed_select))
