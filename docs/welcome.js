document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('test-config-form');

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const book = formData.get('book');
        const test = formData.get('test');
        const mode = formData.get('mode');

        // Construct URL parameters
        const params = new URLSearchParams({
            book: book,
            test: test,
            mode: mode
        });

        // Redirect to test interface
        window.location.href = `test.html?${params.toString()}`;
    });
});
