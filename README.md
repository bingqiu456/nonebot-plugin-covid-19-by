<center><h1>nonebot-plugin-covid-19-by<h1><center>

<center><p>👉疫情小助手 支持查地区 风险地区 境外输入等👈<p><center>

## 安装使用

你可以直接

```python
pip install nonebot-plugin-covid-19-by
```

或者用nonebot里的

```python
nb plugin install nonebot-plugin-covid-19-by
```

---

## 配置说明

请把以下加进你的evn

`covid_19_by_group=["xxxx"] #开启插件的群号
covid_19_by_colour=None #设置文字转图片的颜色 如:#ffffff
covid_19_by_size=None #设置文字转图片的大小 如:30
covid_19_by_images=["xxxx"]#开启文字转图片的群`

`COMMAND_START=["/"] #配置命令起始字符`

---

## 指令说明

执行了`nb run`之后 

请在群里说一句

`/by_covid_19`

获取菜单 详细内容如下

`/by_covid_19_search[地区] ##查询疫情地区
/by_covid_19_news ##查询疫情新闻
/by_covid_19_list_jwsr ##境外输入排行榜
/by_covid_19_details ##本国疫情
/by_covid_19_cha[地区] 如 /by_covid_19_cha广东省,广州市,全部
/covid_19_by_group_turn_on ##开启本群
/covid_19_by_group_turn_off ##关闭本群
/covid_19_by_image_turn_on ##开启文字转图片
/covid_19_by_image_turn_off ##关闭文字转图片`

这里为了不和其他插件冲突 所以指令有点长 抱歉

---

## 有bug？

请发issues给我