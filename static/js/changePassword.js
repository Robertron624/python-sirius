function main () {

    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 5000,
        timerProgressBar: true
    })

    const changePasswordForm = document.getElementById('change-password-form')

    changePasswordForm.addEventListener('submit', async (event) => {
        event.preventDefault()

        const formData = new FormData(changePasswordForm)
        const previous_password = formData.get('previous_password')
        const new_password = formData.get('new_password')
        const new_password_confirm = formData.get('new_password_confirm')

        if(new_password !== new_password_confirm) {
            Toast.fire({
                icon: 'error',
                title: 'Las contraseñas no coinciden',
            })
            return
        }

        const data = {
            previous_password,
            new_password,
            new_password_confirm
        }

        try {
            const response = await fetch('/cambiar-contraseña', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })

            const result = await response.json()

            if (response.status === 200) {
                changePasswordForm.reset()
                Toast.fire({
                    icon: 'success',
                    title: `${result.message}, serás redirigido a la página de inicio de sesión`,
                })

                setTimeout(() => {
                    window.location.href = '/login'
                }, 5000)

            } else {
                Toast.fire({
                    icon: 'error',
                    title: result.message,
                })
            }
        }catch (error) {
            console.error(error)
            
            Toast.fire({
                icon: 'error',
                title: 'Error al cambiar la contraseña, intente de nuevo',
            })
        }
    })
}

document.addEventListener('DOMContentLoaded', main)