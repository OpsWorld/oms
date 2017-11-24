const getters = {
    sidebar: state => state.app.sidebar,
    visitedViews: state => state.app.visitedViews,
    token: state => state.user.token,
    token_time: state => state.user.token_time,
    username: state => state.user.username,
    roles: state => state.user.roles,
    islogin: state => state.user.islogin,
};
export default getters
