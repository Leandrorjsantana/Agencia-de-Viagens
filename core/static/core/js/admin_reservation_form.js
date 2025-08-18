// core/static/core/js/admin_reservation_form.js
document.addEventListener('DOMContentLoaded', function() {
    const $ = django.jQuery;

    function fetchAndDisplayClientName(clientId) {
        const nameDisplayInput = $('#id_client_name_confirmation');
        if (clientId) {
            const url = `/api/v1/accounts/get-full-name/${clientId}/`;
            fetch(url).then(response => response.json()).then(data => {
                nameDisplayInput.val(data.full_name);
            }).catch(error => {
                console.error('Erro ao buscar nome do cliente:', error);
                nameDisplayInput.val('Não foi possível carregar o nome.');
            });
        } else {
            nameDisplayInput.val('');
        }
    }

    $('#id_offer').on('change', function() {
        const offerId = $(this).val();
        const priceInput = $('#id_total_price');
        const startDateInput = $('#id_start_date');
        const endDateInput = $('#id_end_date');
        const reservationCodeInput = $('#id_reservation_code');
        const offerCodeInput = $('#id_offer_code_placeholder'); // Seletor para o código da oferta

        if (offerId) {
            const url = `/api/v1/offers/admin-details/${offerId}/`;
            fetch(url).then(response => response.json()).then(data => {
                priceInput.val(data.price || '').trigger('change');
                startDateInput.val(data.start_date || '').trigger('change');
                endDateInput.val(data.end_date || '').trigger('change');
                
                if (data.offer_code) {
                    const randomPart = Math.random().toString(36).substring(2, 8).toUpperCase();
                    const newCode = `RES-${data.offer_code}-${randomPart}`;
                    reservationCodeInput.val(newCode).trigger('change');
                    offerCodeInput.val(data.offer_code); // Preenche o código da oferta
                }
            }).catch(error => console.error('Erro ao buscar detalhes da oferta:', error));
        } else {
            priceInput.val('').trigger('change');
            startDateInput.val('').trigger('change');
            endDateInput.val('').trigger('change');
            reservationCodeInput.val('').trigger('change');
            offerCodeInput.val(''); // Limpa o código da oferta
        }
    });

    const clientSelect = $('#id_client');
    clientSelect.on('select2:select', function(e) {
        const clientId = e.params.data.id;
        fetchAndDisplayClientName(clientId);
    });
    clientSelect.on('select2:unselect', function() {
        fetchAndDisplayClientName(null);
    });
    const initialClientId = clientSelect.val();
    if (initialClientId) {
        fetchAndDisplayClientName(initialClientId);
    }
});