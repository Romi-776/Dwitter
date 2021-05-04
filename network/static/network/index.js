document.addEventListener('DOMContentLoaded', () => {
    var exampleModal = document.getElementById('exampleModal')
    exampleModal.addEventListener('show.bs.modal', function (event) {
        // Button that triggered the modal
        var button = event.relatedTarget
        // Extract info from data-bs-* attributes
        var recipient = button.getAttribute('data-bs-post_owner')
        var content = button.getAttribute('data-bs-post')
        var post_no = button.getAttribute('data-bs-post_no')
        
        // Update the modal's content.
        var modalTitle = exampleModal.querySelector('.modal-title')
        var modalBodyTextarea = exampleModal.querySelector('.modal-body textarea')
    
        modalTitle.textContent = 'Posted by - ' + recipient
        modalBodyTextarea.value = content

        // save the changes that i had made in the textarea
        var saveChangesButton = exampleModal.querySelector('#save-changes')

        saveChangesButton.onclick = () => {
            var data = modalBodyTextarea.value

            document.querySelector(`#post-${post_no}`).innerHTML = data
            document.querySelector('#close-modal').click()
        }
    })
})

