const getters = {
  sidebar: state => state.app.sidebar,
  language: state => state.app.language,
  visitedViews: state => state.app.visitedViews,
  cachedViews: state => state.app.cachedViews,
  token: state => state.user.token,
  username: state => state.user.username,
  groups: state => state.user.groups,
  role: state => state.user.role,
  menus: state => state.user.menus,
  elements: state => state.user.elements,
  permission_routers: state => state.permission.routers,
  addRouters: state => state.permission.addRouters,
  permissionMenus: state => state.user.permissionMenus
}
export default getters
