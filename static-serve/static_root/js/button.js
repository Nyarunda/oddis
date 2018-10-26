document.querySelectorAll('.btn-submit').forEach(function(e) {
  e.addEventListener('click', function() {
    this.style.backgroundColor = "red";
  })
});