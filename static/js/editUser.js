async function editUserQuery(data) {
  const editUserUrl = "/editar-usuario";

  console.log("data -> ", data);
  const res = await fetch(editUserUrl, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const responseData = await res.json();

  if (!res.ok) {
    return responseData;
  }

  return responseData;
}

function main() {
  console.log("editUser.js loaded");

  const Toast = Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
  });

  const editUserForm = document.getElementById("edit-user");

  editUserForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(editUserForm);

    const data = {
      edit_first_name: formData.get("edit_first_name"),
      edit_last_name: formData.get("edit_last_name"),
      edit_password: formData.get("edit_password"),
      edit_birthdate: formData.get("edit_birthdate"),
      edit_sex: formData.get("edit_sex"),
    };

    try {
      const apiResponse = await editUserQuery(data);

      if (apiResponse.message == undefined) {
        let error_message = "Error al editar usuario, intenta de nuevo";

        if (apiResponse.error_type == "incorrect_password") {
          error_message = "Contraseña incorrecta, intenta de nuevo";
        }

        Toast.fire({
          icon: "error",
          title: error_message,
        });

        return;
      }

      Toast.fire({
        icon: "success",
        title: "Usuario editado correctamente",
      });
    } catch (err) {
      console.error("error: ", err);

      let message = "Error al editar usuario, intenta de nuevo";

      Toast.fire({
        icon: "error",
        title: message,
      });
    }
  });
}

document.addEventListener("DOMContentLoaded", main);
