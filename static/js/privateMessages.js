let messageToDeleteId = null

function deleteCommentFromDOM(messageId) {
    const message = document.getElementById(`message-${messageId}`)
    message.remove()
    const messageCountElement = document.getElementById('message-count')
    const messageCount = messageCountElement.querySelector('span')
    const currentCount = parseInt(messageCount.textContent)

    if (currentCount === 1) {
        const noMessagesContainer = document.createElement('div')
        noMessagesContainer.classList.add('no-messages')
        const noMessages = document.createElement('p')
        noMessages.textContent = 'No tienes mensajes privados'
        noMessagesContainer.appendChild(noMessages)
        messageCountElement.replaceWith(noMessagesContainer)
        return
    }

    if(currentCount === 2) {
        const newMessage = `Tienes <span>1</span> mensaje`
        messageCountElement.innerHTML = `${newMessage}`
        return
    }

    messageCount.textContent = currentCount - 1
}

async function deleteMessageQuery() {
    
    let url = `/delete-message/${messageToDeleteId}`
    
    try {
        let response = await fetch(url, {
            method: 'DELETE'
        })
        if (response.status === 200) {
            return {success: true}
        } else {
            console.log("Error Deleting Message, Status Code: ", response.status)
            return {success: false}
        }
    
    } catch (error) {
        console.log("Error Deleting Message")
        throw error
    }
}

function main(){

    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
    });

    const deleteMessageModal = document.getElementById('delete-message-modal')
    const deleteButtons = document.getElementsByClassName('delete-message-trigger')

    for (let button of deleteButtons) {

        const closestMessage = button.closest('.message')

        // get id from data-message-id attribute
        const messageId = closestMessage.getAttribute('id').split('-')[1]

        button.onclick = function() {
            messageToDeleteId = messageId
            deleteMessageModal.showModal()
        }
    }

    async function handleConfirmDelete() {
        console.log("Deleting Message: ", messageToDeleteId)
        try {
            const queryResponse = await deleteMessageQuery()

            if (!queryResponse.success) {
                throw new Error("Error Deleting Message")
            }

            deleteCommentFromDOM(messageToDeleteId)

            Toast.fire({
                icon: 'success',
                title: 'Mensaje eliminado correctamente.'
            })

            console.log("Message Deleted Successfully")

        } catch (error) {
            console.error("Error Deleting Message: ", error)
            Toast.fire({
                icon: 'error',
                title: 'Error al eliminar el mensaje. Intente nuevamente.'
            })

            console.log("Error Deleting Message")
        } finally {
            messageToDeleteId = null
            deleteMessageModal.close()

            console.log("Message Deletion Process Finished")
        }
    }

    const cancelButton = document.getElementById('cancel-delete-message')
    const confirmButton = document.getElementById('confirm-delete-message')

    cancelButton.addEventListener('click', () => {
        deleteMessageModal.close()
        messageToDeleteId = null
    })

    confirmButton.addEventListener('click', handleConfirmDelete)

    // Close modal if user clicks outside of it
    deleteMessageModal.addEventListener('click', (event) => {
        if (event.target === deleteMessageModal) {
            deleteMessageModal.close()
            messageToDeleteId = null
        }
    })
}

document.addEventListener('DOMContentLoaded', main)