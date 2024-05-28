
function main() {

    const baseUrl = "https://formspree.io/f/xqkworog";

    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 5000
    });

    const helpForm = document.getElementById('help-form');

    helpForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(helpForm);

        try {
            const response = await fetch('/ayuda', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                helpForm.reset();

                Toast.fire({
                    icon: 'success',
                    title: 'Ayuda enviada correctamente.'
                });

            }

            if (response.status === 400) {
                console.error('Error:', data);

                Toast.fire({
                    icon: 'error',
                    title: 'Error al enviar la ayuda, por favor intenta de nuevo.'
                });
            }

        } catch (error) {
            console.error('Error:', error);
            
            Toast.fire({
                icon: 'error',
                title: 'Error al enviar la ayuda, por favor intenta de nuevo.'
            });
        }
    });
}

document.addEventListener('DOMContentLoaded', main);