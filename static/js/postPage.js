
let currentCommentToDeleteId = null;
let currentCommentToEditId = null;

// sanitize text to prevent XSS attacks 
function sanitizeText(text) {
  return text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function getCurrentPostId() {
  const postId = window.location.pathname.split("/")[2];
  return postId;
}

async function addCommentQuery(data) {
  const { commentText, postId } = data;

  const addCommentUrl = `${window.location.origin}/new-comment/${postId}/`;

  const formData = new URLSearchParams();

  const sanitizedText = sanitizeText(commentText);

  formData.append("new_comment_text", sanitizedText);

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
  const { commentId } = data;

  const postId = getCurrentPostId();

  const deleteCommentUrl = `/eliminar-comentario/${postId}/${commentId}`;

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

async function editCommentQuery(data) {
  const { commentId, commentText } = data;

  const postId = getCurrentPostId();

  const editCommentUrl = `/editar-comentario/${postId}/${commentId}`;

  const sanitizedText = sanitizeText(commentText);

  try {
    const response = await fetch(editCommentUrl, {
      method: "PUT",
      body: JSON.stringify({ commentText: sanitizedText }),
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      const parsedResponse = await response.json();

      return parsedResponse.commentData;
    }

    throw new Error("Failed to edit comment");
  } catch (error) {
    throw new Error(error.message);
  }
}

async function deletePostQuery(data) {
  const { postId } = data;

  const deletePostUrl = `/eliminar-post/${postId}`;

  try {
    const response = await fetch(deletePostUrl, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      return;
    }

    throw new Error("Failed to delete post");
  } catch (error) {
    throw new Error(error.message);
  }
}

async function generateNewCommentElement(comment) {
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

  const commentDeleteButtonTrigger = document.createElement("button");
  commentDeleteButtonTrigger.classList.add("delete-comment-trigger");
  commentDeleteButtonTrigger.textContent = "Borrar";

  commentDeleteButtonTrigger.addEventListener("click", () => {
    const deleteCommentModal = document.getElementById("delete-comment-modal");
    deleteCommentModal.showModal();
    currentCommentToDeleteId = id;
  });

  const commentEditButtonTrigger = document.createElement("button");
  commentEditButtonTrigger.classList.add("edit-comment-trigger");
  commentEditButtonTrigger.textContent = "Editar";

  commentEditButtonTrigger.addEventListener("click", () => {
    const editCommentModal = document.getElementById("edit-comment-modal");


    const editCommentForm = document.getElementById("edit-comment-form");
    const editCommentTextArea = editCommentForm.querySelector("#edit-comment-text");

    editCommentTextArea.value = commentText;

    editCommentModal.showModal();
    currentCommentToEditId = id;
  });

  commentToolbar.appendChild(commentDeleteButtonTrigger);
  commentToolbar.appendChild(commentEditButtonTrigger);

  mainNewComment.appendChild(commentInfoContainer);
  mainNewComment.appendChild(commentToolbar);

  newCommentElement.appendChild(mainNewComment);

  return newCommentElement;
}

async function loadEditCommentEvents(Toast) {

  const editCommentModal = document.getElementById("edit-comment-modal");
  const editCommentForm = document.getElementById("edit-comment-form");
  const editCommentTextArea = editCommentForm.querySelector("#edit-comment-text");

  const editCommentTriggers = document.querySelectorAll(".edit-comment-trigger");

  const confirmEditButton = editCommentModal.querySelector(".confirm-edit-comment");
  const cancelEditButton = editCommentModal.querySelector(".cancel-edit-comment");


  cancelEditButton.addEventListener("click", () => {
    editCommentModal.close();
  });

  // close modal when clicking outside
  editCommentModal.addEventListener("click", (e) => {
    if (e.target === editCommentModal) {
      editCommentModal.close();
    }
  });

  confirmEditButton.addEventListener("click", async () => {
    const commentId = currentCommentToEditId;
    const commentText = editCommentTextArea.value;

    if (!commentText) {
      Toast.fire({
        icon: "error",
        title: "El comentario no puede estar vacío",
      });

      return;
    }

    const data = {
      commentId,
      commentText,
    };

    try {
      const editedCommentData = await editCommentQuery(data);

      Toast.fire({
        icon: "success",
        title: "Comentario editado",
      });

      const { commentText } = editedCommentData;

      // find the comment container and update the text
      const commentContainer = document.querySelector(
        `.comment-container[data-comment-id="${commentId}"]`
      );

      if(!commentContainer) {
        console.error("Comment container not found");
        return;
      }

      const commentTextElement = commentContainer.querySelector(".comment_body p");

      commentTextElement.textContent = commentText;

    } catch (error) {
      console.error("Error:", error);

      Toast.fire({
        icon: "error",
        title: "Error al editar comentario, por favor intente de nuevo.",
      });
    } finally {
      editCommentModal.close();
    }
  });

  editCommentTriggers.forEach(async (trigger) => {
    trigger.addEventListener("click", () => {
      // open modal
      editCommentModal.showModal();

      const commentContainer = trigger.closest(".comment-container");

      // Set the current comment text in the edit textarea
      const commentTextElement = commentContainer.querySelector(".comment_body p");
      editCommentTextArea.value = commentTextElement.textContent;

      // Get comment id and image id from closest ".comment-container" element
      const commentId = commentContainer.getAttribute("data-comment-id");

      currentCommentToEditId = commentId;
    });
  });

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
      const newCommentElement = await generateNewCommentElement(newCommentData);

      commentsContainer.appendChild(newCommentElement);
      commentForm.reset();

      Toast.fire({
        icon: "success",
        title: "Comentario agregado",
      });
    } catch (error) {
      console.error("Error:", error);

      Toast.fire({
        icon: "error",
        title: "Error al agregar comentario, por favor intente de nuevo.",
      });
    }
  });
}

function loadDeleteCommentEvents(Toast) {
  const deleteCommentModal = document.getElementById("delete-comment-modal");

  const deleteCommentTriggers = document.querySelectorAll(
    ".delete-comment-trigger"
  );

  const confirmDeleteButton = deleteCommentModal.querySelector(
    ".confirm-delete-comment"
  );

  confirmDeleteButton.addEventListener("click", async () => {
    if (!currentCommentToDeleteId) {
      console.error("Comment id not found");
      return;
    }

    const data = {
      commentId: currentCommentToDeleteId,
    };

    try {
      await deleteCommentQuery(data);

      Toast.fire({
        icon: "success",
        title: "Comentario eliminado",
      });

      const commentContainer = document.querySelector(
        `.comment-container[data-comment-id="${currentCommentToDeleteId}"]`
      );

      commentContainer.remove();

      // Reset current comment id and image id
      currentCommentToDeleteId = null;
    } catch (error) {
      console.error("Error:", error);

      Toast.fire({
        icon: "error",
        title: "Error al eliminar comentario, por favor intente de nuevo.",
      });
    } finally {
      deleteCommentModal.close();
    }
  });

  const cancelDeleteButton = deleteCommentModal.querySelector(
    ".cancel-delete-comment"
  );

  cancelDeleteButton.addEventListener("click", () => {
    deleteCommentModal.close();
  });

  // close modal when clicking outside
  deleteCommentModal.addEventListener("click", (e) => {
    if (e.target === deleteCommentModal) {
      deleteCommentModal.close();
    }
  });

  deleteCommentTriggers.forEach(async (trigger) => {
    trigger.addEventListener("click", () => {
      // open modal
      deleteCommentModal.showModal();

      // Get comment id and image id from closest ".comment-container" element

      const commentContainer = trigger.closest(".comment-container");
      const commentId = commentContainer.getAttribute("data-comment-id");

      currentCommentToDeleteId = commentId;
    });
  });
}

function loadDeletePostEvents(Toast) {
  // Delete post
  const deletePostBaseUrl = "/eliminar-post/";
  const deletePostModal = document.getElementById("delete-post-modal");
  const postId = getCurrentPostId();

  const deletePostTrigger = document.getElementById("delete-post-trigger");

  if (!deletePostTrigger) return;

  const confirmDeletePostButton = deletePostModal.querySelector(
    ".confirm-delete-post"
  );
  const cancelDeletePostButton = deletePostModal.querySelector(
    ".cancel-delete-post"
  );

  async function confirmDeleteHandler() {
    const data = {
      postId,
    };

    try {
      await deletePostQuery(data);

      Toast.fire({
        icon: "success",
        title: "Post eliminado correctamente, redirigiendo...",
      });

      setTimeout(() => {
        window.location.href = "/perfil";
      }, 3000);

    } catch (error) {
      console.error("Error:", error);

      Toast.fire({
        icon: "error",
        title: "Error al eliminar post, por favor intente de nuevo.",
      });
    } finally {
      deletePostModal.close();
    }
  }

  deletePostTrigger.addEventListener("click", () => {
    deletePostModal.showModal();

    confirmDeletePostButton.removeEventListener("click", confirmDeleteHandler);

    confirmDeletePostButton.addEventListener("click", confirmDeleteHandler, {
      once: true,
    });
  });

  cancelDeletePostButton.addEventListener("click", () => {
    deletePostModal.close();
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

  loadDeleteCommentEvents(Toast);
  loadAddCommentEvents(Toast);
  loadEditCommentEvents(Toast);
  loadDeletePostEvents(Toast);
};

document.addEventListener("DOMContentLoaded", main);
