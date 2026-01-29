document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('.like-btn').forEach(btn => {

        btn.addEventListener('click', () => {
            const noteId = btn.dataset.noteId;
            const url = btn.dataset.likeUrl;

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': window.CSRF_TOKEN,
                },
            })
            .then(response => response.json())
            .then(data => {
                btn.querySelector('.like-count').textContent = data.likes;
                btn.classList.toggle('liked', data.liked);
            })
            .catch(err => console.error('Like error:', err));
        });

    });

});
