import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import climate
from esphome.const import CONF_ID

from . import MideaDehum, CONF_MIDEA_DEHUM_ID, midea_dehum_ns

DEPENDENCIES = ["midea_dehum"]

CONF_SWING = "swing"

CONFIG_SCHEMA = climate.CLIMATE_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(midea_dehum_ns.class_("MideaDehumClimate", climate.Climate)),
    cv.GenerateID(CONF_MIDEA_DEHUM_ID): cv.use_id(MideaDehum),
    cv.Optional(CONF_SWING, default=False): cv.boolean,
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    parent = await cg.get_variable(config[CONF_MIDEA_DEHUM_ID])
    await climate.register_climate(parent, config)
    if config[CONF_SWING]:
        cg.add_define("USE_MIDEA_DEHUM_SWING")
