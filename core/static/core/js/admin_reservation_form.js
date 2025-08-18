// core/static/core/js/admin_reservation_form.js
document.addEventListener('DOMContentLoaded', function() {
    // Usamos o jQuery que já vem com o Django Admin para segurança
    const $ = django.jQuery;

    // Quando o campo da oferta (#id_offer) mudar...
    $('#id_offer').on('change', function() {
        const offerId = $(this).val();
        const priceInput = $('#id_total_price');
        const startDateInput = $('#id_start_date');
        const endDateInput = $('#id_end_date');
        const reservationCodeInput = $('#id_reservation_code');

        // Se uma oferta foi selecionada...
        if (offerId) {
            // Monta a URL da nossa API interna
            const url = `/api/v1/offers/admin-details/${offerId}/`;
            
            // Faz a chamada para a API
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    // Preenche cada campo com os dados recebidos
                    if (data.price) {
                        // --- CORREÇÃO AQUI: Usando o valor com PONTO ---
                        priceInput.val(data.price).trigger('change');
                    }
                    if (data.start_date) {
                        startDateInput.val(data.start_date).trigger('change');
                    }
                    if (data.end_date) {
                        endDateInput.val(data.end_date).trigger('change');
                    }
                    if (data.offer_code) {
                        // Gera um código de reserva único, mas baseado no da oferta
                        const randomPart = Math.random().toString(36).substring(2, 8).toUpperCase();
                        const newCode = `RES-${data.offer_code}-${randomPart}`;
                        reservationCodeInput.val(newCode).trigger('change');
                    }
                })
                .catch(error => console.error('Erro ao buscar detalhes da oferta:', error));
        } else {
            // Se o usuário desmarcar a oferta, limpa os campos
            priceInput.val('').trigger('change');
            startDateInput.val('').trigger('change');
            endDateInput.val('').trigger('change');
            reservationCodeInput.val('').trigger('change');
        }
    });
});