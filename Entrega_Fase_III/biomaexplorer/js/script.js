document.querySelectorAll('.thumbnail').forEach(item => {
    item.addEventListener('click', function() {
        const fullSizeImage = document.getElementById('full-size-image');
        const descriptionElement = document.getElementById('image-description'); // Obtiene el elemento del texto descriptivo

        fullSizeImage.src = this.src; // Actualiza la imagen en tamaño completo con la fuente de la miniatura clickeada
        fullSizeImage.alt = this.alt; // Actualiza el texto alternativo también, si es necesario
        descriptionElement.textContent = this.getAttribute('data-description'); // Actualiza la descripción del texto con el data-description de la miniatura
    });
});

