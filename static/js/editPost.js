function main() {

    function getCurrentPostId() {
        const url = window.location.href;
        const urlParts = url.split('/');
        return urlParts[urlParts.length - 1];
    }

    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
    });
    
    const editPostForm = document.getElementById('edit-post-form');

    editPostForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(editPostForm);
        const postId = getCurrentPostId();
        const edited_text = formData.get('edited_text');

        const body = {
            edited_text,
        };

        try {
            const res = await fetch(`/editar/${postId}`, {
                method: 'PUT',
                body: JSON.stringify(body),
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await res.json();

            if (data.error) {
                Toast.fire({
                    icon: 'error',
                    title: data.error,
                });
            } else {
                Toast.fire({
                    icon: 'success',
                    title: 'Publicación editada exitosamente, redirigiendo...',
                });
                setTimeout(() => {
                    window.location.href = '/perfil';
                }, 3000);
            }
            
        } catch (err) {
            console.error(err);
            Toast.fire({
                icon: 'error',
                title: 'Ha ocurrido un error. Intente nuevamente.',
            });
        }
    });
}

document.addEventListener('DOMContentLoaded', main);