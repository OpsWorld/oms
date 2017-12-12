<template>
  <div class="dashboard-container">
    <component :is="currentRole"></component>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import adminDashboard from './admin'
import editorDashboard from './editor'
import { super_group } from '@/config'

export default {
  name: 'dashboard',
  components: { adminDashboard, editorDashboard },
  data() {
    return {
      currentRole: 'adminDashboard'
    }
  },
  computed: {
    ...mapGetters([
      'groups'
    ])
  },
  created() {
    if (!this.groups.includes(super_group)) {
      this.currentRole = 'editorDashboard'
    }
  }
}
</script>
