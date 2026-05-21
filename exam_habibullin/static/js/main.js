setTimeout(function () {
    var alerts = document.querySelectorAll('.site-alert');
    alerts.forEach(function (alert) {
        var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        bsAlert.close();
    });
}, 4000);

var cards = document.querySelectorAll('.course-card');
cards.forEach(function (card) {
    card.addEventListener('click', function () {
        card.classList.toggle('border-primary');
    });
});
