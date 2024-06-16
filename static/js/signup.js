function main() {
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
    });

    const signupForm = document.getElementById("signup-form");

    signupForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(signupForm);

        const firstName = formData.get("signup_first_name");
        const lastName = formData.get("signup_last_name");
        const email = formData.get("signup_email");
        const confirmEmail = formData.get("signup_confirm_email");
        const password = formData.get("signup_password");
        const confirmPassword = formData.get("signup_confirm_password");
        const birthday = formData.get("signup_birthdate");
        const sex = formData.get("signup_sex");

        const rawData = {
            firstName,
            lastName,
            email,
            confirmEmail,
            password,
            confirmPassword,
            birthday,
            sex,
        }

        const isDataValid = checkSignupData(rawData);

        if(isDataValid.hasError) {
            Toast.fire({
                icon: 'error',
                title: isDataValid.message,
            });
            return;
        }

        const data = {
            signup_first_name: firstName,
            signup_last_name: lastName,
            signup_email: email,
            signup_confirm_email: confirmEmail,
            signup_password: password,
            signup_confirm_password: confirmPassword,
            signup_birthdate: birthday,
            signup_sex: sex,
        }

        try {
            const response = await fetch("/registro", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });

            const responseData = await response.json();

            if(responseData.success) {
                Toast.fire({
                    icon: 'success',
                    title: "Registro exitoso. Serás redirigido al inicio de sesión",
                });
                setTimeout(() => {
                    window.location.href = "/login";
                }, 3000);
            } else {
                Toast.fire({
                    icon: 'error',
                    title: responseData.message,
                });
            }
        } catch (error) {
            console.error(error);
            Toast.fire({
                icon: 'error',
                title: "Ocurrió un error al procesar la solicitud, inténtalo de nuevo más tarde",
            });
        }

        
    });
}

document.addEventListener("DOMContentLoaded", main);