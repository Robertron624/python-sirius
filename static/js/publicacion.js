const main = () => {


    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true
    })

    // delete example url "/eliminarcomment/{{id_img}}/{{comentario['id']}}"
    const deleteUrl = "/eliminarcomment/"

    const deleteCommentModal = document.getElementById('delete-comment-modal')

    const deleteCommentTriggers = document.querySelectorAll('.delete-comment-trigger')

    deleteCommentTriggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            const commentId = trigger.getAttribute('data-comment-id')
            const imageId = trigger.getAttribute('data-image-id')
            const confirmDeleteButton = deleteCommentModal.querySelector('a.confirm-delete-comment')
            const cancelDeleteButton = deleteCommentModal.querySelector('.cancel-delete-comment')

            confirmDeleteButton.href = `${deleteUrl}${imageId}/${commentId}`
            deleteCommentModal.classList.add('is-active')

            cancelDeleteButton.addEventListener('click', () => {
                deleteCommentModal.close()
            })

            // display toast when deleting comment

            confirmDeleteButton.addEventListener('click', () => {
                Toast.fire({
                    icon: 'success',
                    title: 'Comentario eliminado'
                })
            })

            // open modal
            deleteCommentModal.showModal()

            // close modal when clicking outside
            deleteCommentModal.addEventListener('click', (e) => {
                if (e.target === deleteCommentModal) {
                    deleteCommentModal.close()
                }
            })
        })
    })

}

document.addEventListener('DOMContentLoaded', main)