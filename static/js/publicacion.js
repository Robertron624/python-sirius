const main = () => {

    // delete example url "/eliminarcomment/{{id_img}}/{{comentario['id']}}"
    const deleteUrl = "/eliminarcomment/"

    const deleteCommentModal = document.getElementById('delete-comment-modal')

    const deleteCommentTriggers = document.querySelectorAll('.delete-comment-trigger')

    console.log("deleteCommentTriggers", deleteCommentTriggers)

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