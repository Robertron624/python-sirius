

const main = () => {
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true
    })

    // Delete comment
    const deleteUrl = "/eliminarcomment/"

    const deleteCommentModal = document.getElementById('delete-comment-modal')

    const deleteCommentTriggers = document.querySelectorAll('.delete-comment-trigger')

    deleteCommentTriggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            const commentId = trigger.getAttribute('data-comment-id')
            const imageId = trigger.getAttribute('data-image-id')
            const confirmDeleteButton = deleteCommentModal.querySelector('.confirm-delete-comment')
            const cancelDeleteButton = deleteCommentModal.querySelector('.cancel-delete-comment')

            cancelDeleteButton.addEventListener('click', () => {
                deleteCommentModal.close()
            })

            // display toast when deleting comment
            confirmDeleteButton.addEventListener('click', () => {
                
                const deleteCommentUrl = `${deleteUrl}${imageId}/${commentId}`

                fetch(deleteCommentUrl, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                }).then(response => {
                    if (response.ok) {
                        Toast.fire({
                            icon: 'success',
                            title: 'Comentario eliminado'
                        })

                        const commentElement = trigger.closest('.comment-container'); // Adjust selector as needed
                        console.log("commentElement", commentElement)
                        if (commentElement) {
                            commentElement.remove();
                        }
                    } else {
                        Toast.fire({
                            icon: 'error',
                            title: 'Error al eliminar comentario'
                        })
                    }
                }).catch(error => {
                    console.error('Error:', error)

                    Toast.fire({
                        icon: 'error',
                        title: 'Error al eliminar comentario'
                    })
                }).finally(() => {
                    deleteCommentModal.close()
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

    // Delete post
    const deletePostUrl = "/eliminarpost/"
    const deletePostModal = document.getElementById('delete-post-modal')

    const deletePostTrigger = document.getElementById('delete-post-trigger')

    if(!deletePostTrigger) return

    const confirmDeletePostButton = deletePostModal.querySelector('a.confirm-delete-post')
    const cancelDeletePostButton = deletePostModal.querySelector('.cancel-delete-post')

    deletePostTrigger.addEventListener('click', () => {
        const postId = deletePostTrigger.getAttribute('data-post-id')
        confirmDeletePostButton.href = `${deletePostUrl}${postId}`
        deletePostModal.showModal()
    })

    cancelDeletePostButton.addEventListener('click', () => {
        deletePostModal.close()
    })

    confirmDeletePostButton.addEventListener('click', () => {
        Toast.fire({
            icon: 'success',
            title: 'Publicación eliminada'
        })
    })

    // close modal when clicking outside
    deletePostModal.addEventListener('click', (e) => {
        if (e.target === deletePostModal) {
            deletePostModal.close()
        }
    })

}

document.addEventListener('DOMContentLoaded', main)