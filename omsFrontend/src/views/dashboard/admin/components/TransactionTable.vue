<template>
  <el-table :data="list" style="width: 100%;padding-top: 15px;">
    <el-table-column label="Order_No" show-overflow-tooltip>
      <template slot-scope="scope">
        {{scope.row.order_no}}
      </template>
    </el-table-column>
    <el-table-column label="Price" width="195" align="center">
      <template slot-scope="scope">
        ¥{{scope.row.price | toThousandslsFilter}}
      </template>
    </el-table-column>
    <el-table-column label="Status" width="100" align="center">
      <template slot-scope="scope">
        <el-tag :type="scope.row.status | statusFilter"> {{scope.row.status}}</el-tag>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
export default {
  data() {
    return {
      list: [
        { order_no: '3ace8815-add7-4F3F-4635-6e1314dbB1f4', price: 14000.83, status: 'success', timestamp: 1085532909106, username: 'Lisa Moore' },
        { order_no: '4ace8815-add7-4F3F-4635-6e1314dbB1f4', price: 24000.83, status: 'success', timestamp: 1085532909106, username: 'Disa Moore' },
        { order_no: '5ace8815-add7-4F3F-4635-6e1314dbB1f4', price: 34000.83, status: 'danger', timestamp: 1085532909106, username: 'Gisa Moore' },
        { order_no: '6ace8815-add7-4F3F-4635-6e1314dbB1f4', price: 44000.83, status: 'success', timestamp: 1085532909106, username: 'Hisa Moore' },
        { order_no: '7ace8815-add7-4F3F-4635-6e1314dbB1f4', price: 54000.83, status: 'danger', timestamp: 1085532909106, username: 'Visa Moore' },
        { order_no: '8ace8815-add7-4F3F-4635-6e1314dbB1f4', price: 64000.83, status: 'success', timestamp: 1085532909106, username: 'Sisa Moore' }
      ]
    }
  },
  filters: {
    statusFilter(status) {
      const statusMap = {
        success: 'success',
        pending: 'danger'
      }
      return statusMap[status]
    }
  },
  created() {
  },
  methods: {}
}
</script>
