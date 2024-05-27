let currentCommentToDeleteId = null;

function getCurrentPostId() {
    const postId = window.location.pathname.split("/")[2];
    return postId;
}

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

    const { commentId } = data;

    const postId = getCurrentPostId();

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

  commentToolbar.appendChild(commentDeleteButtonTrigger);

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
        const newCommentElement = await generateNewCommentElement(newCommentData);

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

  const deleteCommentModal = document.getElementById("delete-comment-modal");

  const deleteCommentTriggers = document.querySelectorAll(
    ".delete-comment-trigger"
  );

  const confirmDeleteButton = deleteCommentModal.querySelector(
    ".confirm-delete-comment"
  );

  confirmDeleteButton.addEventListener("click", async () => {

      if(!currentCommentToDeleteId) {
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
      }
      catch (error) {
          console.error("Error:", error);

          Toast.fire({
              icon: "error",
              title: "Error al eliminar comentario",
          });
      }
      finally {
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



  loadDeleteCommentEvents(Toast);
  loadAddCommentEvents(Toast);
  loadDeletePostEvents(Toast);
};

document.addEventListener("DOMContentLoaded", main);
