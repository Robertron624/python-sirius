async function addCommentQuery(data) {

    const { commentText, postId } = data;

    const addCommentUrl = `${window.location.origin}/new-comment/${postId}/`;

    const formData = new URLSearchParams();
    formData.append("new_comment_text", commentText);

    try {

        const response = await fetch(addCommentUrl, {
            method: "POST",
            body: formData,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        });

        if (response.ok) {
            const parsedResponse = await response.json();
            return parsedResponse.commentData;
        }

        throw new Error("Failed to add comment");

    } catch (error) {
        throw new Error(error.message);
    }

}

async function deleteCommentQuery(data) {

    const { commentId, postId } = data;

    const deleteCommentUrl = `/eliminarcomment/${postId}/${commentId}`;

    try {

        const response = await fetch(deleteCommentUrl, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (response.ok) {
            return;
        }

        throw new Error("Failed to delete comment");

    } catch (error) {
        throw new Error(error.message);
    }

}

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

async function loadAddCommentEvents(Toast) {

  const commentsContainer = document.querySelector(".comment_block");
  const commentForm = document.getElementById("new-comment-form");
  const postId = window.location.pathname.split("/")[2];
  const newCommentTextArea = commentForm.querySelector("#new_comment_text");

  commentForm.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent default form submission

    const newCommentText = newCommentTextArea.value;

    if (!newCommentText) {
      Toast.fire({
        icon: "error",
        title: "El comentario no puede estar vacío",
      });

      return;
    }

    const data = {
        commentText: newCommentText,
        postId,
    };

    try {
        const newCommentData = await addCommentQuery(data);
        const newCommentElement = generateNewCommentElement(newCommentData, Toast);

        commentsContainer.appendChild(newCommentElement);
        commentForm.reset();

        Toast.fire({
            icon: "success",
            title: "Comentario agregado",
        });
    }
    catch (error) {
      console.error("Error:", error);

      Toast.fire({
        icon: "error",
        title: "Error al agregar comentario",
      });
    }

    
  });
}

function loadDeleteCommentEvents(Toast) {
  // Delete comment
  const deleteUrl = "/eliminarcomment/";

  const deleteCommentModal = document.getElementById("delete-comment-modal");

  const deleteCommentTriggers = document.querySelectorAll(
    ".delete-comment-trigger"
  );

  deleteCommentTriggers.forEach(async (trigger) => {
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
      confirmDeleteButton.addEventListener("click", async () => {

        try {

            const data = {
                commentId,
                postId: imageId,
            };
    
            await deleteCommentQuery(data);
    
            Toast.fire({
                icon: "success",
                title: "Comentario eliminado",
            });

            const commentElement = trigger.closest(".comment-container");

            commentElement.remove();
        }
        catch (error) {
            console.error("Error:", error);
    
            Toast.fire({
                icon: "error",
                title: "Error al eliminar comentario",
            });
        } finally {
            deleteCommentModal.close();
        }
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
