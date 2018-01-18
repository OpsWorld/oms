import { getAllminions, getAllminionStatus } from 'api/salt'

const salt = {
  state: {
    allkeys: '',
    allminions: ''
  },
  mutations: {
    SET_ALLKEYS: (state, allkeys) => {
      state.allkeys = allkeys
    },
    SET_ALLMINIONS: (state, allminions) => {
      state.allminions = allminions
    }
  },
  actions: {
    getAllKeys({ commit }) {
      return new Promise((resolve, reject) => {
        getAllminions().then(response => {
          const data = response.data.results
          const allminions = {}
          allminions.accepted = data.accepted.length
          allminions.rejected = data.rejected.length
          allminions.unaccept = data.unaccept.length
          commit('SET_ALLKEYS', allminions)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },
    getAllminions({ commit }) {
      return new Promise((resolve, reject) => {
        getAllminionStatus().then(response => {
          const data = response.data.results
          console.log(data)
          commit('SET_ALLMINIONS', data)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    }
  }
}

export default salt
