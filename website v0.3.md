website v0.3

数据库设计

| User            |              |               |          |
| --------------- | ------------ | ------------- | -------- |
| 字段              | 类型           | 说明            | 外键       |
| uid             | int          | 用户id          |          |
| name            | varchar(255) | 用户名           |          |
| password        | varchar(255) | 用户密码          |          |
| token           | varchar(255) | token         |          |
| status          | int          | 状态, 1.正常 0.停用 |          |
| role_id         | int          | 角色id          | Role表的id |
| create_time     | datetime     | 创建时间          |          |
| last_login_time | datetime     | 最后登录时间        |          |
| last_IP         | varchar(16)  | 最后登录IP        |          |



| Role        |              |               |      |
| ----------- | ------------ | ------------- | ---- |
| 字段          | 类型           | 说明            | 外键   |
| id          | int          | 角色id          |      |
| name        | varchar(255) | 角色名           |      |
| status      | int          | 状态, 1.正常 0.停用 |      |
| create_time | datetime     | 创建时间          |      |



| Module      |              |               |      |
| ----------- | ------------ | ------------- | ---- |
| 字段          | 类型           | 说明            | 外键   |
| id          | int          | 模块id          |      |
| name        | varchar(255) | 模块名           |      |
| url         | varchar(255) | 模块url         |      |
| create_time | datetime     | 创建时间          |      |
| status      | int          | 状态, 1.正常 0.停用 |      |
| icon        | varchar(255) | 图标            |      |



| Role_Module |              |                              |            |
| ----------- | ------------ | ---------------------------- | ---------- |
| 字段          | 类型           | 说明                           | 外键         |
| id          | int          | 角色模块关联id                     |            |
| role_id     | int          | 角色id                         | Role表的id   |
| module_id   | int          | 模块id                         | Module表的id |
| control     | varchar(255) | 控制权限, add,edit,delete,select |            |
| status      | int          | 状态, 1.正常 0.停用                |            |



接口说明:

1. login页面API:

   基本信息:

   请求类型:	HTTP

   请求方式:	POST

   响应类型:	JSON

   请求地址:	/login

   请求参数:	

   | 参数名称     | 是否必须 | 类型     | 描述   | 默认值  |
   | -------- | ---- | ------ | ---- | ---- |
   | username | 是    | string | 用户名  |      |
   | password | 是    | string | 密码   |      |
   响应数据
   | 响应参数   | 是否必须 | 类型   | 描述                 |
   | ------ | ---- | ---- | ------------------ |
   | result | 是    | int  | 0.表示验证失败, 1.表示验证成功 |


2. admin页面API:

   基本信息:

   请求类型:	HTTP

   请求方式:	GET

   响应类型:	JSON

   请求地址:	/admin/api/user[/\<int:uid>]

   请求参数:

   | 参数名称    | 是否必须 | 类型     | 描述        | 默认值  |
   | ------- | ---- | ------ | --------- | ---- |
   | page    | 否    | int    | 页码        | 1    |
   | name    | 否    | string | 用户名,搜索时用  |      |
   | role_id | 否    | int    | 角色id,搜索时用 |      |
   | status  | 否    | int    | 用户状态,搜索时用 |      |

   响应数据

   | 响应参数         | 是否必须 | 类型         | 描述              |
   | ------------ | ---- | ---------- | --------------- |
   | data         | 是    | list(dict) | 用户信息列表          |
   | id           | 是    | int        | 用户id            |
   | name         | 是    | string     | 用户名             |
   | password     | 是    | string     | 用户密码            |
   | token        | 是    | string     | token           |
   | role_name    | 是    | string     | 角色名             |
   | role_id      | 是    | int        | 角色id            |
   | status       | 是    | int        | 用户状态, 1.正常 0.停用 |
   | current_page | 是    | int        | 当前页码            |
   | total_page   | 是    | int        | 总页数             |
   | has_next     | 是    | bool       | 是否有下一页          |
   | has_prev     | 是    | bool       | 是否有上一页          |

   基本信息:

   请求类型:	HTTP

   请求方式:	POST

   响应类型:	JSON

   请求地址:	/admin/api/user

   请求参数:

   | 参数名称     | 是否必须 | 类型     | 描述   | 默认值  |
   | -------- | ---- | ------ | ---- | ---- |
   | username | 是    | string | 用户名  |      |
   | password | 是    | string | 用户密码 |      |
   | role_id  | 是    | int    | 角色id |      |

   响应数据:

   | 响应参数 | 是否必须 | 类型     | 描述   |
   | ---- | ---- | ------ | ---- |
   | code | 是    | int    | 状态字  |
   | info | 是    | string | 状态说明 |
   | name | 否    | string | 报错字段 |