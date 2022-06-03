from nonebot.permission import SUPERUSER
from nonebot import get_driver,on_command
from loguru import logger
from nonebot.adapters.onebot.v11 import Event,GROUP_OWNER,GROUP_ADMIN,GroupMessageEvent


global colour
global size
global group_image_covid
colour = get_driver().config.dict().get("covid_19_by_colour",None)
group_image_covid = get_driver().config.dict().get("covid_19_by_images",[])
size = get_driver().config.dict().get("covid_19_by_size",None)
global group_covid
group_covid = get_driver().config.dict().get("covid_19_by_group",[])
if colour ==None:
    logger.warning("covid_19:未配置文转图颜色 默认None")
if size==None:
    logger.warning("covid_19:未配置文转图字体 默认None")
if group_covid ==[]:
    logger.warning("covid_19:未配置开启群号 默认[]")
if group_image_covid==[]:
    logger.success("covid_19:未配置文转图群组 默认[]")

add_group = on_command("covid_19_by_group_turn_on",permission=SUPERUSER|GROUP_ADMIN|GROUP_OWNER)
@add_group.handle()
async def _(event:GroupMessageEvent):
    group_covid.append(str(event.group_id))
    logger.success(f"covid_19:开启{event.group_id}成功")
    await add_group.finish("covid_19:开启本群成功")
    

del_group = on_command("covid_19_by_group_turn_off",permission=SUPERUSER|GROUP_ADMIN|GROUP_OWNER)
@del_group.handle()
async def del_group_(event:GroupMessageEvent):
    try:
        group_covid.remove(str(event.group_id))
    except(ValueError):
        logger.error("covid_19:此群不存在列表中")
        pass
    else:
        logger.success(f"covid_19:关闭{event.group_id}成功")
        await del_group.finish("covid_19:关闭本群成功")

image_group = on_command("covid_19_by_image_turn_on",permission=SUPERUSER|GROUP_ADMIN|GROUP_OWNER)
@image_group.handle()
async def _(event:GroupMessageEvent):
    group_image_covid.append(str(event.group_id))
    logger.success(f"covid_19:开启{event.group_id}成功")
    await image_group.finish("covid_19:开启本群成功")
    

image_group_off = on_command("covid_19_by_image_turn_off",permission=SUPERUSER|GROUP_ADMIN|GROUP_OWNER)
@image_group_off.handle()
async def del_group_(event:GroupMessageEvent):
    try:
        group_image_covid.remove(str(event.group_id))
    except(ValueError):
        logger.error("covid_19:此群不存在列表中")
        pass
    else:
        logger.success(f"covid_19:关闭{event.group_id}成功")
        await image_group_off.finish("covid_19:关闭本群成功")








    


