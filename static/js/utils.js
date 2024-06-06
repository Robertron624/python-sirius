function checkEmail(email) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    return emailReg.test(email);
}

function isUserAdult(birthday) {

    // Check if if the user is at least 18
    const today = new Date();
    const birthdate = new Date(birthday);
    let age = today.getFullYear() - birthdate.getFullYear();
    const month = today.getMonth() - birthdate.getMonth();
    const day = today.getDate() - birthdate.getDate();

    if (month < 0 || (month === 0 && day < 0)) {
        age--;
    }

    return age >= 18;
}

function checkSignupData(signupData) {

    const {
        firstName,
        lastName,
        email,
        confirmEmail,
        password,
        confirmPassword,
        birthday,
        sex
    } = signupData;

    const emptyValidations = [
        { field: firstName, message: "El campo de nombre no puede estar vacío" },
        { field: lastName, message: "El campo de apellido no puede estar vacío" },
        { field: email, message: "El campo de correo electrónico no puede estar vacío" },
        { field: confirmEmail, message: "El campo de confirmación de correo electrónico no puede estar vacío" },
        { field: password, message: "El campo de contraseña no puede estar vacío" },
        { field: confirmPassword, message: "El campo de confirmación de contraseña no puede estar vacío" },
        { field: birthday, message: "El campo de fecha de nacimiento no puede estar vacío" },
        { field: sex, message: "El campo de sexo no puede estar vacío" }
    ];

    for (let { field, message } of emptyValidations) {
        if (field === "") {
            return { hasError: true, message };
        }
    }

    const identicalValidations = [
        { field: email, confirmField: confirmEmail, message: "Los correos electrónicos no coinciden" },
        { field: password, confirmField: confirmPassword, message: "Las contraseñas no coinciden" }
    ];

    for (let { field, confirmField, message } of identicalValidations) {
        if (field !== confirmField) {
            return { hasError: true, message };
        }
    }

    if (!checkEmail(email)) {
        return { hasError: true, message: "El correo electrónico no es válido" };
    }

    if (!isUserAdult(birthday)) {
        return { hasError: true, message: "Debes ser mayor de 18 años para registrarte" };
    }

    return { hasError: false, message: "" };
}

