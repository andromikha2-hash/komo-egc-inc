(function () {
  document.querySelectorAll('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = b.getAttribute('data-copy');
      try {
        navigator.clipboard.writeText(t).then(
          function () { b.textContent = 'Copied ' + t; },
          function () { b.textContent = t; }
        );
      } catch (e) { b.textContent = t; }
    });
  });
})();
