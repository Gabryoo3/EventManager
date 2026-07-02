document.addEventListener('DOMContentLoaded', function () {
    const isOrganizerCheckbox = document.querySelector('#id_is_organizer');

    // Find the row elements wrapper in Django Admin (usually a div with .form-row)
    const stageNameRow = document.querySelector('.field-stage_name');
    const mainCategoryRow = document.querySelector('.field-main_category');

    function toggleOrganizerFields() {
        if (isOrganizerCheckbox && isOrganizerCheckbox.checked) {
            stageNameRow.style.display = 'block';
            mainCategoryRow.style.display = 'block';
        } else {
            if (stageNameRow) stageNameRow.style.display = 'none';
            if (mainCategoryRow) mainCategoryRow.style.display = 'none';
        }
    }

    if (isOrganizerCheckbox) {
        // Run immediately on page load to set initial state
        toggleOrganizerFields();
        // Run every time the checkbox is clicked
        isOrganizerCheckbox.addEventListener('change', toggleOrganizerFields);
    }
});