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

  var form = document.getElementById('rfq');
  if (!form) return;
  var status = document.getElementById('f-status');
  var phone = form.getAttribute('data-phone');

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (form.elements.website && form.elements.website.value) return; // honeypot
    var name = form.elements.name.value.trim();
    var tel = form.elements.phone.value.trim();
    if (!name || !tel) {
      status.textContent = 'Add your name and phone number so we can call you back.';
      return;
    }
    var endpoint = form.getAttribute('data-endpoint');
    if (!endpoint) {
      status.textContent = 'Online requests are not connected yet. Call ' + phone + '.';
      return;
    }
    // The intake sheet reads name, phone, email, service and message.
    // Fold the extra fields into message so nothing is dropped.
    var data = new FormData();
    data.append('name', name);
    data.append('phone', tel);
    data.append('email', form.elements.email.value.trim());
    data.append('service', form.elements.service.value);
    var extra = [
      'Company: ' + form.elements.company.value.trim(),
      'Role: ' + form.elements.role.value,
      'Site location: ' + form.elements.city.value,
      'Target start: ' + (form.elements.start.value || 'not given')
    ].join('\n');
    data.append('message', extra + '\n\n' + form.elements.message.value.trim());

    var btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    status.textContent = 'Sending…';
    fetch(endpoint, { method: 'POST', body: data, mode: 'no-cors' })
      .then(function () {
        status.textContent = 'Request sent. We will call you back. Need it sooner? Call ' + phone + '.';
        form.reset();
      })
      .catch(function () {
        status.textContent = 'That did not send. Call ' + phone + ' instead.';
      })
      .then(function () { btn.disabled = false; });
  });
})();
