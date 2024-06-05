function main() {
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
    });

    const fileInputEl = document.getElementById('post_file');
    const imagePlaceholder = document.getElementById('image-placeholder');
    const originalImagePlaceholder = imagePlaceholder.src;
    const allowedExtensions = ['image/jpeg', 'image/png', 'image/gif'];

    imagePlaceholder.addEventListener('click', () => {
        fileInputEl.click();
    });

    fileInputEl.addEventListener('change', (event) => {
        const file = event.target.files[0];

        if (!file) {
            imagePlaceholder.src = originalImagePlaceholder;    
            return;
        }

        if (!allowedExtensions.includes(file.type)) {
            Toast.fire({
                icon: 'error',
                title: 'Solo se permiten imágenes en formato JPG, PNG o GIF.',
            });

            fileInputEl.value = ''; // Clear the file input
            imagePlaceholder.src = originalImagePlaceholder;
            return;
        }

        const reader = new FileReader();

        reader.onload = (e) => {
            imagePlaceholder.src = e.target.result;
        }

        reader.readAsDataURL(file);
        
    });

    const newPostForm = document.getElementById('new-post-form');

    newPostForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(newPostForm);

        // Include CSRF token
        const csrfToken = document.querySelector('input[name="csrf_token"]').value;
        formData.append('csrf_token', csrfToken);

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
                imagePlaceholder.src = originalImagePlaceholder;

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