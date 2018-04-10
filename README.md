# 运维自动化管理系统 #

[![python3.x](https://img.shields.io/badge/python-3.X-blue.svg)](https://www.python.org/)
[![django](https://img.shields.io/badge/django-1.11-blue.svg)](https://www.djangoproject.com/)
[![django-rest-framework](https://img.shields.io/badge/djangorestframework-3.6.3-blue.svg)](http://www.django-rest-framework.org/)
[![celery](https://img.shields.io/badge/celery-4.1.0-green.svg)](http://www.celeryproject.org/)
[![vue](https://img.shields.io/badge/vue-2.5.9-brightgreen.svg)](https://github.com/vuejs/vue)
[![element-ui](https://img.shields.io/badge/element--ui-2.0.7-brightgreen.svg)](https://github.com/ElemeFE/element)

注意：该项目是采用的前后端分离开发，是在python3.6下面开发的，因为是使用的django-rest-framework，理论也支持python2.7x；由于前端使用的是vuejs,所有不支持低版本ie游览器。

## 基础模块
> 几乎所有系统都必须要一下基础模块，其他模块都是基于基础模块扩展的，不用过多说明，顾名思义。

- 用户模块
- 菜单模块
- 权限模块

## 办公模块
- 工单系统
> 工单系统用于客服发现业务出现异常后通过本系统提交工单，工单可以直接粘贴截图和上传附件，处理人接到工单后，可以工单下面回复处理过程。


- 任务系统
> 本系统主要是给开发童鞋用的，作用类似禅道等项目管理，当然功能上弱多了，其实市面上有很多开源的bug任务管理系统，这里由于开发童鞋不喜，所以凑合的写一个给他们用。

- 考勤机集成
> 通过调用考勤机的api,把员工每天的打卡记录集成到oms系统，方便查询。

## 运维模块
- 主机模块
> 主机模块也可以叫做资产模块，在本系统中主要是用来管理公司的服务器、机房等资产，可以手动录入主机信息，也可以通过 `saltapi` 自动收集或更新主机信息，这个模块是运维自动化的基础，发布、监控等系统的自动化都需依赖完善的CMDB(资产管理系统)。

- 审计模块
> 审计模块是一个大类，主要职责是日志记录，比如记录每个人的操作，记录主机录入或修改时的前后变化等，防止出现误操作后无记录可查。

- salt模块
> salt模块核心的利用saltapi完成自动化工作，比如发布、分发文件、批量更新机器配置等，

- 发布系统
> 发布系统实现只用点击按钮就能实现发布动作，配合脚本可以实现发布故障立即回滚，并且记录发布人以及发布结果，减少人为发布失误以及上线故障。

- dns域名管理集成
> 因公司在几家不同的dns服务商上面分别都有很多域名，管理起来不甚方便，于是通过调用它们的api,在oms系统上实现集中化管理。

- 通知
> 这个不能算是一个模块， 只能算一个小功能，作用是给用户发送通知，比如发送发布结果、新工单通知和任务通知；目前集成了邮件、skype和telegram。

## 说明

### 项目后续功能

- [ ] 监控模块
> 利用zabbix Api获取zabbix数据，对zabbix进行批量操作，api的使用可以参考 [利用zabbix API进行批量操作](https://www.jianshu.com/p/e087cace8ddf)。

- [ ] 周报系统
> 每周结束之前在oms系统上发布周报，方便领导统计、查看。

- [ ] 继续想新功能