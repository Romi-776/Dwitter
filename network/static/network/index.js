document.addEventListener('DOMContentLoaded', () => {


    // Modal related event listener which will work only if user
    // wants to edit his post
    var postModal = document.getElementById('postModal')
    postModal.addEventListener('show.bs.modal', function (event) {

        // Button that triggered the modal
        var button = event.relatedTarget

        // Extract info from data-bs-* attributes
        var recipient = button.getAttribute('data-bs-post_owner')
        var content = button.getAttribute('data-bs-post')
        var post_no = button.getAttribute('data-bs-post_no')

        // Update the modal's content.
        var modalTitle = postModal.querySelector('.modal-title')
        var modalBodyTextarea = postModal.querySelector('.modal-body textarea')

        modalTitle.textContent = 'Posted by - ' + recipient
        modalBodyTextarea.value = content

        // save the changes that i had made in the textarea
        var saveChangesButton = postModal.querySelector('#save-changes')

        /*
            This will change the description of the post when user
            hits the save changes button
        */
        saveChangesButton.onclick = () => {
            // changing the post's description from html
            var data = modalBodyTextarea.value
            document.querySelector(`#post-${post_no}`).innerHTML = data

            // updating it in the db
            fetch('/update_post', {
                method: 'POST',
                body: JSON.stringify({
                    post_id: `${post_no}`,
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


    var profileModal = document.getElementById('profileModal')
    profileModal.addEventListener('show.bs.modal', function (event) {

        // Button that triggered the modal
        var button = event.relatedTarget

        // Extract info from data-bs-* attributes


    })

    var profilePicModal = document.getElementById('profilePicModal')
    profilePicModal.addEventListener('show.bs.modal', function (event) {

        // Button that triggered the modal
        var button = event.relatedTarget

        // Extract info from data-bs-* attributes


    })
})


// function to change the background image of the user
function showPreview(event) {

    if (event.target.files.length > 0) {
        // my div which will show an image in background
        var img = document.getElementById('background_profile')

        // image that I want to show in background which I had chosen 
        const file = event.target.files[0];

        // changing the chosen image into its path url
        const src = URL.createObjectURL(file);

        // inserting the url into the div background image
        img.style.backgroundImage = `url(${src})`;
    }
}

// function to change the profile pic of the user
function showImage(event) {

    if (event.target.files.length > 0) {
        // my div which will show an image in background
        var img = document.getElementsByClassName('wrapper')

        // image that I want to show in background which I had chosen 
        const file = event.target.files[0];

        // changing the chosen image into its path url
        const src = URL.createObjectURL(file);

        // inserting the url into the div background image
        img[0].style.backgroundImage = `url(${src})`;
    }
}

