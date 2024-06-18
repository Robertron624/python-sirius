let userToDeleteId = null;
let userToEditId = null;

async function deleteUser() {
    const response = await fetch(`/delete-user/${userToDeleteId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    if (response.ok) {
        return {"status": "success"};
    } else {
        const data = await response.json();

        if (data.error) {
            console.error('Failed to delete user', data.error);
        }
        return {"status": "error"};
    }
}

async function editRole(newRole) {
    const response = await fetch(`/edit-user-role/${userToEditId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'new-role': newRole})
    });

    if (response.ok) return {"status": "success"};

    const data = await response.json();

    if (data.error) {
        console.error('Failed to edit user role', data.error);
    }

    return {"status": "error"};
}

function main() {
    console.log("adminDashboard.js loaded")

    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
    });

    const deleteModal = document.getElementById('delete-user-modal');
    const cancelDeleteUser = document.getElementById('cancel-delete-user');
    const confirmDeleteUser = document.getElementById('confirm-delete-user');

    const editRoleModal = document.getElementById('edit-role-modal');
    const cancelEditRole = document.getElementById('cancel-edit-role');
    const confirmEditRole = document.getElementById('confirm-edit-role');

    const userCurrentRole = document.getElementById('current-role');

    deleteModal.addEventListener('click', (event) => {
        if (event.target === deleteModal) {
            deleteModal.close();
        }
    });

    deleteModal.addEventListener('close', () => {
        userToDeleteId = null;
    });

    editRoleModal.addEventListener('click', (event) => {
        if (event.target === editRoleModal) {
            editRoleModal.close();
        }
    });

    editRoleModal.addEventListener('close', () => {
        userToEditId = null;
    });

    cancelDeleteUser.addEventListener('click', () => {
        deleteModal.close();
    });

    cancelEditRole.addEventListener('click', () => {
        editRoleModal.close();
    });

    const deleteUserButtons = document.querySelectorAll('.trigger-delete-user');

    deleteUserButtons.forEach(button => {
        button.addEventListener('click', () => {
            const closestTR = button.closest('tr');
            const dataUserId = closestTR.getAttribute('data-user-id');
            userToDeleteId = dataUserId;
            deleteModal.showModal();
        });
    });

    const editRoleButtons = document.querySelectorAll('.trigger-edit-role');

    editRoleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const closestTR = button.closest('tr');
            const dataUserId = closestTR.getAttribute('data-user-id');
            const thisUserRole = closestTR.querySelector('.user-role').textContent;
            userCurrentRole.textContent = thisUserRole;
            userToEditId = dataUserId;
            editRoleModal.showModal();
        });
    });


    // Confirm delete user

    confirmDeleteUser.addEventListener('click', async () => {
        try {
            const response = await deleteUser();
            if (response.status === "success") {
                Toast.fire({
                    icon: 'success',
                    title: 'Usuario eliminado correctamente, recargando la página...'
                });
                setTimeout(() => {
                    window.location.reload();
                }, 3000);
            } else {
                Toast.fire({
                    icon: 'error',
                    title: 'Error al eliminar usuario, intente nuevamente'
                });
            }
        } catch (error) {
            console.error('Failed to delete user', error);
            Toast.fire({
                icon: 'error',
                title: 'Error al eliminar usuario, intente nuevamente'
            });
        } finally {
            deleteModal.close();
        }
    });

    // Confirm edit role

    confirmEditRole.addEventListener('click', async () => {

        const userRow = document.querySelector(`tr[data-user-id="${userToEditId}"]`);
        const thisUserRole = userRow.querySelector('.user-role').textContent;

        const newRoleSelect = document.getElementById('new-role')
        const newRole = newRoleSelect.value;

        if(newRole === thisUserRole) {
            Toast.fire({
                icon: 'error',
                title: 'El nuevo rol debe ser diferente al actual'
            });
            return;
        }

        if (newRole === "") {
            Toast.fire({
                icon: 'error',
                title: 'El campo no puede estar vacío'
            });
            return;
        }

        try {
            const response = await editRole(newRole);
            if (response.status === "success") {
                Toast.fire({
                    icon: 'success',
                    title: 'Rol actualizado correctamente, recargando la página...'
                });
                setTimeout(() => {
                    window.location.reload();
                }, 3000);
            } else {
                Toast.fire({
                    icon: 'error',
                    title: 'Error al actualizar rol, intente nuevamente'
                });
            }
        } catch (error) {
            console.error('Failed to edit role', error);
            Toast.fire({
                icon: 'error',
                title: 'Error al actualizar rol, intente nuevamente'
            });
        } finally {
            editRoleModal.close();
        }
    });
}

document.addEventListener('DOMContentLoaded', main);