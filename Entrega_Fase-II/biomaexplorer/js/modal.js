document.addEventListener('DOMContentLoaded', function () {
  var infoModal = document.getElementById('infoModal');
  infoModal.addEventListener('show.bs.modal', function (event) {
      var button = event.relatedTarget; // Botón que activó la modal
      var title = button.getAttribute('data-title'); // Extrae título del atributo data-title del botón
      var text = button.getAttribute('data-text'); // Extrae texto del atributo data-text del botón

      var modalTitle = infoModal.querySelector('.modal-title');
      var modalBody = infoModal.querySelector('.modal-body');

      modalTitle.textContent = title; // Establece título de la modal
      modalBody.textContent = text; // Establece texto de la modal
  });
});
