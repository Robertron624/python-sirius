function getReceiverId() {
    // get the second to last element of the URL path
    const path = window.location.pathname;
    const pathParts = path.split('/');
    return pathParts[pathParts.length - 2];
}

async function sendMessage(formData) {
    const receiverId = getReceiverId();

    const url = `/enviar-mensaje/${receiverId}/`;
    const response = await fetch(url, {
        method: 'POST',
        body: formData,
    });

    if (response.ok) {
        return response.json();
    } else {
        const errorMessage = await response.text();
        throw new Error(errorMessage);
    }
}

function main() {

    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true
    });

    const sendMessageForm = document.getElementById('send-message-form');
    const fileInputEl = document.getElementById('attached_image');
    const imagePreviewContainer = document.getElementById('image-preview-container');
    const imagePreview = document.getElementById('image-preview');
    const deleteImageButton = document.getElementById('delete-image-button');

    fileInputEl.addEventListener('change', () => {
        const file = fileInputEl.files[0];

        if (!file) {
            imagePreview.src = '';
            return;
        }

        const reader = new FileReader();

        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreviewContainer.hidden = false;
        }

        reader.readAsDataURL(file);
    });

    deleteImageButton.addEventListener('click', () => {
        fileInputEl.value = '';
        imagePreview.src = '';
        imagePreviewContainer.hidden = true;
    });

    sendMessageForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(sendMessageForm);

        const messageText = formData.get('message_text');

        if (!messageText) {
            Toast.fire({
                icon: 'error',
                title: 'El mensaje no puede estar vacío.'
            });
            return;
        }

        try {
            await sendMessage(formData);
            
            Toast.fire({
                icon: 'success',
                title: 'Mensaje enviado correctamente.'
            });

            sendMessageForm.reset();
            imagePreview.src = '';
            imagePreviewContainer.hidden = true;
        } catch (error) {
            console.error("error while sending message: ", error);
            Toast.fire({
                icon: 'error',
                title: "Ocurrió un error al enviar el mensaje. Por favor, inténtalo de nuevo."
            });
        }
    });
}

document.addEventListener('DOMContentLoaded', main);