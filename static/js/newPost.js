function main() {
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
    });

    const newPostForm = document.getElementById('new-post-form');

    newPostForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(newPostForm);

        try {

            const response = await fetch('/nueva-publicacion', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if(response.ok) {
                Toast.fire({
                    icon: 'success',
                    title: `${data.success}. Serás redirigido al feed en 3 segundos.`,
                });

                // Clear the form
                newPostForm.reset();

                setTimeout(() => {
                    window.location.href = '/feed';
                }, 3000);
            } else {
                Toast.fire({
                    icon: 'error',
                    title: `${data.message}`,
                });
            }

        } catch (error) {
            console.error(error);
            Toast.fire({
                icon: 'error',
                title: 'Hubo un error al procesar la solicitud. Inténtalo de nuevo.',
            });
        }
    });
}

document.addEventListener('DOMContentLoaded', main);