import '../css/styles.scss';

import './csrf';

const messageTemplate = ({ id, author, time, text }) => `
    <div class="message" data-id="${id}">
        <div class="message__author">
            <div class="message__avatar"></div>
            <div class="message__name">${author}</div>
            <div class="message__time">${time}</div>
        </div>
        <div class="message__text">${text}</div>
    </div>
`;

$(document).ready(function() {
    var form = $('#message-form');
    var input = $('input[name=text]');
    var chat = $($('.chat')[0]);

    form.on('submit', function(e) {
        e.preventDefault();

        var formData = new FormData(e.target);

        $.post({
            // method: 'POST',
            url: '/chat/message_create/',
            data: formData,
            processData: false,
            contentType: false,

            success: response => {
                chat.prepend(response.renderedTemplate);
                input.val('');
            }
        })
    });

    setInterval(function() {
        const lastId = $('.message').first().data('id');

        $.get({
            url: '/chat/messages',
            data: {
                last_id: lastId
            },

            success: response => {
                if (response !== '') {
                    chat.prepend(response);
                }
            }
        })
    }, 5 * 1000);
});