import {getMenuPerm} from 'api/perm';
import {getInfo} from 'api/auth';

const perm = {
    state: {
        routers: localStorage.getItem('routers')
    },

    mutations: {
        SET_ROUTERS: (state, routers) => {
        state.routers = routers;
       }
    },

    actions: {
        GetRouters({commit}){
            return new Promise((resolve, reject) => {
                const user_id = localStorage.getItem('user_id');
                getMenuPerm(user_id).then(response => {
                const router_data = response.data.results;
                localStorage.setItem('routers', router_data);
                commit('SET_ROUTERS', router_data);
                resolve()
            })
        })
    }
    }
};


export default perm;
