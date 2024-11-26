// Confirm before deleting something; taken from https://stackoverflow.com/questions/37398416/django-delete-confirmation
function confirmDelete(event) {
    if (!confirm("Are you sure you want to delete this item?\n\nThere is no way to restore.")) {
        event.preventDefault();
  } else {
        const baseURL = window.location.origin;
        window.location(baseURL + "/pass_list/");
    }
}

const confirmDeleteButtons = document.querySelectorAll(".confirm-delete");
confirmDeleteButtons.forEach(button => {
  button.addEventListener("click", confirmDelete);
});