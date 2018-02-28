/**
 * Created by Itimor on 2017/12/12.
 */

let CONFIG
const rest_url = 'oms.tb-gaming.local'
const ws_scheme = window.location.protocol === 'https:' ? 'wss' : 'ws'

// if (process.env.NODE_ENV === 'development') {
if (process.env.NODE_ENV === 'production') {
  CONFIG = {
    apiUrl: '',
    super_group: 'OMS_Super_Admin',
    wsurl: ws_scheme + '://' + rest_url + '/ws'
  }
} else if (process.env.NODE_ENV === 'test') {
  CONFIG = {
    apiUrl: 'http://oms.tb-gaming.local:8000',
    super_group: 'admin',
    wsurl: ws_scheme + '://' + rest_url + '/ws'
  }
} else {
  CONFIG = {
    apiUrl: 'http://127.0.0.1:8000',
    super_group: 'admin',
    wsurl: ws_scheme + '://127.0.0.1:8000'
  }
}

/*
 接口API根地址
 */
const url = CONFIG.apiUrl

module.exports = {
  apiUrl: CONFIG.apiUrl,
  ws_url: CONFIG.wsurl,

  // 超级管理组
  super_group: CONFIG.super_group,

  // 表格数据
  LIMIT: 20,
  pagesize: [20, 50, 100],
  pageformat: 'total, prev, pager, next, sizes',

  // 本地上传到服务器
  uploads: `${url}/api/upload/`,
  uploadurl: 'https://httpbin.org/post',

  // 登录
  login: `${url}/api/api-token-auth/`,
  // login: `${url}/api/api-auth/login/`,
  logout: `${url}/api/api-auth/logout/`,
  changePassword: `${url}/api/changepasswd/`,

  // 主机
  hosts: `${url}/api/hosts/`,
  idcs: `${url}/api/idcs/`,

  // 用户
  users: `${url}/api/users/`,
  groups: `${url}/api/groups/`,
  roles: `${url}/api/roles/`,

  // 工单
  worktickers: `${url}/api/worktickers/`,
  ticketcomments: `${url}/api/ticketcomments/`,
  ticketenclosures: `${url}/api/ticketenclosures/`,
  tickettypes: `${url}/api/tickettypes/`,
  records: `${url}/api/records/`,

  // 第三支付工单
  platforms: `${url}/api/platforms/`,
  merchants: `${url}/api/merchants/`,
  threepayenclosures: `${url}/api/threepayenclosures/`,
  paychannels: `${url}/api/paychannels/`,
  paychannelnames: `${url}/api/paychannelnames/`,
  threepaycomments: `${url}/api/threepaycomments/`,
  platformpaychannels: `${url}/api/platformpaychannels/`,

  // 权限
  usermenuperms: `${url}/api/usermenuperms/`,
  userhostperms: `${url}/api/userhostperms/`,
  userwikiperms: `${url}/api/userwikiperms/`,
  routerinfo: `${url}/api/routers/`,

  // 菜单
  firstmenus: `${url}/api/firstmenus/`,
  secondmenus: `${url}/api/secondmenus/`,
  menumetas: `${url}/api/menumetas/`,

  // tools
  sendmail: `${url}/api/sendmail/`,
  sendmessage: `${url}/api/sendmessage/`,
  calenders: `${url}/api/calenders/`,

  // 文档平台
  wikis: `${url}/api/wikis/`,
  opswikis: `${url}/api/opswikis/`,

  // 发布
  jobs: `${url}/api/jobs/`,
  deployenvs: `${url}/api/deployenvs/`,
  deployjobs: `${url}/api/deployjobs/`,
  updaejobsstatus: `${url}/api/update_jobs_status/`,
  deploycmds: `${url}/api/deploycmds/`,
  deployversions: `${url}/api/deployversions/`,
  deploytickets: `${url}/api/deploytickets/`,
  deployticketenclosures: `${url}/api/deployticketenclosures/`,

  // salt
  get_all_key: `${url}/api/salts/get_all_key/`,
  minions_status: `${url}/api/salts/minions_status/`,
  get_minion_info: `${url}/api/salts/get_minion_info/`,
  cmdrun: `${url}/api/salts/cmdrun/`,
  get_result: `${url}/api/salts/get_result/`,
  sync_remote_server: `${url}/api/salts/sync_remote_server/`,

  // 项目
  projects: `${url}/api/projects/`,
  projectcomments: `${url}/api/projectcomments/`,
  projectenclosures: `${url}/api/projectenclosures/`,
  projecttypes: `${url}/api/projecttypes/`,
  bugmanagers: `${url}/api/bugmanagers/`,
  testmanagers: `${url}/api/testmanagers/`,
  demandmanagers: `${url}/api/demandmanagers/`,
  demandenclosures: `${url}/api/demandenclosures/`,

  // 运维项目
  opsprojects: `${url}/api/opsprojects/`,
  opsprojectenclosures: `${url}/api/opsprojectenclosures/`,
  opsprojecttypes: `${url}/api/opsprojecttypes/`,
  opsdemandmanagers: `${url}/api/opsdemandmanagers/`,
  opsdemandenclosures: `${url}/api/opsdemandenclosures/`
}
