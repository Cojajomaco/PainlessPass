// Function that returns true if a value is in a row. Used to determine
// further search filtering in later functions.
function checkRowForValue(row, value) {
  // Iterate through each cell in the row
  if (value == null || value === "") {
      return true
  }
  // Check if value matches
  return $(row).find('td').filter(function() {
    return ($(this).text().toLowerCase().indexOf(value) > -1);
  }).length > 0;
  return false; // Value not found in the row
}


// Confirm before deleting something; taken from https://stackoverflow.com/questions/37398416/django-delete-confirmation
function confirmDelete(event) {
    if (!confirm("Are you sure you want to delete this item?\n\nThere is no way to restore.")) {
        event.preventDefault();
  } else {
        const baseURL = window.location.origin;
        window.location(baseURL + "/pass_list/");
    }
}

// Confirmation for deletion buttons
const confirmDeleteButtons = document.querySelectorAll(".confirm-delete");
confirmDeleteButtons.forEach(button => {
  button.addEventListener("click", confirmDelete);
});

// Filtering table by Folders (dropdown menu) and Search bar
$(document).ready(function() {
    if($('#folderChoice')) {
        // Folder dropdown filter
        $("#folderChoice").change(function () {
            let searchValue = $("#passSearch").val().toLowerCase();
            if (searchValue === null)
            {
                searchValue = "";
            }
            let selectedValue = $(this).val();

            // Table filter, and Search bar filter, if available
            $("#passTable tbody tr").each(function () {
                let columnValue = $(this).find("td:nth-child(5)").text(); // Assuming the column to filter is the second one
                if ((selectedValue === "" || columnValue === selectedValue) && (checkRowForValue($(this), searchValue))) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });
        });


        // Filter with search changes instead
        $("#passSearch").on("keyup", function () {
            let searchValue = $("#passSearch").val().toLowerCase();
            if (searchValue === null)
            {
                searchValue = "";
            }
            let selectedValue = $("#folderChoice").val();

            // Table filter, and Search bar filter, if available
            $("#passTable tbody tr").each(function () {
                let columnValue = $(this).find("td:nth-child(5)").text(); // Assuming the column to filter is the second one
                if ((selectedValue === "" || columnValue === selectedValue) && (checkRowForValue($(this), searchValue))) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });
        });
    }
});
