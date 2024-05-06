


function generateNewCommentElement(comment, Toast) {
  const {
    commentText,
    dateComment,
    userName,
    userLastName,
    userEmail,
    urlAvatar,
    id,
  } = comment;

  const newCommentElement = document.createElement("div");
  newCommentElement.classList.add("comment-container");
  newCommentElement.setAttribute("data-comment-id", id);

  const mainNewComment = document.createElement("div");
  mainNewComment.classList.add("user_comment");

  const commentInfoContainer = document.createElement("div");
  commentInfoContainer.classList.add("main-comment");

  const userAvatarContainer = document.createElement("div");
  userAvatarContainer.classList.add("comment_user_avatar");

  const userAvatar = document.createElement("img");
  userAvatar.src = `${window.location.origin}/static/${urlAvatar}`;

  const commentNameDate = document.createElement("div");
  commentNameDate.classList.add("name_date");

  const userNameP = document.createElement("p");
  userNameP.textContent = `${userName} ${userLastName}`;

  const commentDate = document.createElement("p");
  commentDate.textContent = dateComment;

  commentNameDate.appendChild(userNameP);
  commentNameDate.appendChild(commentDate);

  userAvatarContainer.appendChild(userAvatar);
  userAvatarContainer.appendChild(commentNameDate);

  const commentTextContainer = document.createElement("div");
  commentTextContainer.classList.add("comment_body");
  const commentTextP = document.createElement("p");
  commentTextP.textContent = commentText;

  commentTextContainer.appendChild(commentTextP);

  commentInfoContainer.appendChild(userAvatarContainer);
  commentInfoContainer.appendChild(commentTextContainer);

  const commentToolbar = document.createElement("div");
  commentToolbar.classList.add("comment_toolbar");

  const commentDeleteButton = document.createElement("button");
  commentDeleteButton.classList.add("delete-comment-trigger");
  commentDeleteButton.textContent = "Borrar";

  commentDeleteButton.addEventListener("click", () => {

    const deleteCommentModal = document.getElementById("delete-comment-modal");


    deleteCommentModal.showModal();


    const confirmDeleteButton = deleteCommentModal.querySelector(
      ".confirm-delete-comment"
    );
    const cancelDeleteButton = deleteCommentModal.querySelector(
      ".cancel-delete-comment"
    );

    cancelDeleteButton.addEventListener("click", () => {
      deleteCommentModal.close();
    });

    confirmDeleteButton.addEventListener("click", () => {

        const deleteUrl = "/eliminarcomment/";
        const imageId = window.location.pathname.split("/")[2];
        const deleteCommentUrl = `${deleteUrl}${imageId}/${id}`;

      fetch(deleteCommentUrl, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (response.ok) {
            Toast.fire({
              icon: "success",
              title: "Comentario eliminado",
            });

            newCommentElement.remove();
          } else {
            Toast.fire({
              icon: "error",
              title: "Error al eliminar comentario",
            });
          }
        })
        .catch((error) => {
          console.error("Error:", error);

          Toast.fire({
            icon: "error",
            title: "Error al eliminar comentario",
          });
        })
        .finally(() => {
          deleteCommentModal.close();
        });
    });
  });

  commentToolbar.appendChild(commentDeleteButton);

  mainNewComment.appendChild(commentInfoContainer);
  mainNewComment.appendChild(commentToolbar);

  newCommentElement.appendChild(mainNewComment);

  return newCommentElement;
}

function loadAddCommentEvents(Toast) {
  // Assuming you have a form with the ID 'commentForm'
  const commentForm = document.getElementById("new-comment-form");
  const postId = window.location.pathname.split("/")[2];

  const addCommentUrl = `${window.location.origin}/new-comment/${postId}/`;
  const newCommentTextArea = commentForm.querySelector("#new_comment_text");

  commentForm.addEventListener("submit", (event) => {
    event.preventDefault(); // Prevent default form submission

    const newCommentText = newCommentTextArea.value;

    if (!newCommentText) {
      Toast.fire({
        icon: "error",
        title: "El comentario no puede estar vacío",
      });

      return;
    }

    const formData = new URLSearchParams();
    formData.append("new_comment_text", newCommentText);

    fetch(addCommentUrl, {
      method: "POST",
      body: formData,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    })
      .then((response) => {
        if (response.ok) {
          return response.json(); // Parse response JSON
        } else {
          throw new Error("Failed to add comment");
        }
      })
      .then((data) => {
        const newCommentData = data.commentData;

        console.log(
          "new comment data returned from backend -> ",
          newCommentData
        );

        const commentsSection = document.querySelector(".comment_block");

        const newCommentElement = generateNewCommentElement(newCommentData, Toast);

        commentsSection.appendChild(newCommentElement); // Append the new comment element to the comments section

        // Clear the comment form after successful submission
        commentForm.reset();

        Toast.fire({
          icon: "success",
          title: "Comentario agregado",
        });
      })
      .catch((error) => {
        console.error("Error:", error);

        Toast.fire({
          icon: "error",
          title: "Error al agregar comentario, por favor intente nuevamente",
        });
      });
  });
}

function loadDeleteCommentEvents(Toast) {
  // Delete comment
  const deleteUrl = "/eliminarcomment/";

  const deleteCommentModal = document.getElementById("delete-comment-modal");

  const deleteCommentTriggers = document.querySelectorAll(
    ".delete-comment-trigger"
  );

  deleteCommentTriggers.forEach((trigger) => {
    trigger.addEventListener("click", () => {
      const commentId = trigger.getAttribute("data-comment-id");
      const imageId = trigger.getAttribute("data-image-id");
      const confirmDeleteButton = deleteCommentModal.querySelector(
        ".confirm-delete-comment"
      );
      const cancelDeleteButton = deleteCommentModal.querySelector(
        ".cancel-delete-comment"
      );

      cancelDeleteButton.addEventListener("click", () => {
        deleteCommentModal.close();
      });

      // display toast when deleting comment
      confirmDeleteButton.addEventListener("click", () => {

        const deleteCommentUrl = `${deleteUrl}${imageId}/${commentId}`;

        fetch(deleteCommentUrl, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((response) => {
            if (response.ok) {
              Toast.fire({
                icon: "success",
                title: "Comentario eliminado",
              });

              const commentElement = trigger.closest(".comment-container"); // Adjust selector as needed
              if (commentElement) {
                commentElement.remove();
              }
            } else {
              Toast.fire({
                icon: "error",
                title: "Error al eliminar comentario",
              });
            }
          })
          .catch((error) => {
            console.error("Error:", error);

            Toast.fire({
              icon: "error",
              title: "Error al eliminar comentario",
            });
          })
          .finally(() => {
            deleteCommentModal.close();
          });
      });

      // open modal
      deleteCommentModal.showModal();

      // close modal when clicking outside
      deleteCommentModal.addEventListener("click", (e) => {
        if (e.target === deleteCommentModal) {
          deleteCommentModal.close();
        }
      });
    });
  });
}

function loadDeletePostEvents(Toast) {
  // Delete post
  const deletePostUrl = "/eliminarpost/";
  const deletePostModal = document.getElementById("delete-post-modal");

  const deletePostTrigger = document.getElementById("delete-post-trigger");

  if (!deletePostTrigger) return;

  const confirmDeletePostButton = deletePostModal.querySelector(
    "a.confirm-delete-post"
  );
  const cancelDeletePostButton = deletePostModal.querySelector(
    ".cancel-delete-post"
  );

  deletePostTrigger.addEventListener("click", () => {
    const postId = deletePostTrigger.getAttribute("data-post-id");
    confirmDeletePostButton.href = `${deletePostUrl}${postId}`;
    deletePostModal.showModal();
  });

  cancelDeletePostButton.addEventListener("click", () => {
    deletePostModal.close();
  });

  confirmDeletePostButton.addEventListener("click", () => {
    Toast.fire({
      icon: "success",
      title: "Publicación eliminada",
    });
  });

  // close modal when clicking outside
  deletePostModal.addEventListener("click", (e) => {
    if (e.target === deletePostModal) {
      deletePostModal.close();
    }
  });
}

const main = () => {

    const Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        });

  loadAddCommentEvents(Toast);
  loadDeleteCommentEvents(Toast);
  loadDeletePostEvents(Toast);
};

document.addEventListener("DOMContentLoaded", main);
