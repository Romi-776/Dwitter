document.addEventListener('DOMContentLoaded', () => {

    // Modal related even listener which will work only if user
    // wants to edit his post
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

        /*
            This will change the description of the post when user
            hits the save changes button
        */
        saveChangesButton.onclick = () => {
            alert('saving your changes')

            // changing the post's description from html
            var data = modalBodyTextarea.value
            document.querySelector(`#post-${post_no}`).innerHTML = data

            // getting the current date time
            var today = new Date();
            var date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();;
            var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
            var dateTime = date + ' ' + time;


            // updating it in the db
            fetch('/update_post', {
                method: 'POST',
                body: JSON.stringify({
                    post_id : `${post_no}`,
                    updated_on: `${dateTime}`,
                    updated_description: `${data}`
                })
            })
                .then(response => response.json())
                .then(result => {
                })

            document.querySelector('#close-modal').click()
            return true;
        }
    })
})

