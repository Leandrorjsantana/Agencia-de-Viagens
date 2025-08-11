// core/static/core/js/admin_custom.js

// Espera que o documento HTML esteja completamente carregado
document.addEventListener("DOMContentLoaded", function() {
    // Procura pelo link que abre o personalizador da UI
    // O seletor '[data-bs-target="#jazzmin-ui-builder"]' é o identificador único deste botão
    const customizeButton = document.querySelector('a[data-bs-target="#jazzmin-ui-builder"]');

    // Se o botão for encontrado, muda o seu texto
    if (customizeButton) {
        // Encontra o elemento <span> dentro do botão que contém o texto
        const buttonTextSpan = customizeButton.querySelector('span');
        if (buttonTextSpan) {
            buttonTextSpan.textContent = "Personalizar";
        }
    }
});