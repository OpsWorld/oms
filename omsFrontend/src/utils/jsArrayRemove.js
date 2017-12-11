Array.prototype.indexItem = function(val) {
  for (var i = 0; i < this.length; i++) {
    if (this[i] === val) return i
  }
  return -1
}

Array.prototype.remove = function(val) {
  const index = this.indexItem(val)
  if (index > -1) {
    this.splice(index, 1)
  }
}
