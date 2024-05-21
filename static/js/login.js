function main() {

    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
    });
    
    const loginForm = document.getElementById("login-form");
    
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(loginForm);

        const username = formData.get("login_user");
        const password = formData.get("login_password");

        try {
            const response = await fetch("/login", {
                method: "POST",
                body: JSON.stringify({ 
                    "login_user": username,
                    "login_password": password,
                }),
                headers: {
                    "Content-Type": "application/json",
                },
            });

            if(response.status === 401){
                Toast.fire({
                    icon: 'error',
                    title: 'Usuario o contraseña incorrectos.'
                });
                return;
            }

            if(response.status === 200){
                window.location.href = "/feed";
            }

        }catch (error) {
            console.error("Error:", error);
            Toast.fire({
                icon: 'error',
                title: 'Hubo un error al iniciar sesión, por favor intenta de nuevo.'
            });
        }
    });
}

document.addEventListener("DOMContentLoaded", main);