/**
 * Created by Administrator on 2017/12/16.
 */
module.exports = function(datetime) {
  let date
  if (datetime) {
    date = new Date(datetime)
  } else {
    date = new Date()
  }
  const Y = date.getFullYear().toString()
  const M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1)
  const D = date.getDate()
  const h = date.getHours()
  const m = date.getMinutes()
  const s = date.getSeconds()
  const ctime = Y + M + D + h + m + s
  return ctime
}
