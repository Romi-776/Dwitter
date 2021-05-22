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

})


function update_profile(event) {
    alert("Profile is updating")
    // Button that triggered the modal
    var button = document.querySelector("#save-changes")

    // getting the user whose profile is being updated
    var user = button.dataset.user

    // get all the info. of this user like
    // images and description
    // bg_img and profile_pic will contain blob url something like the below one
    // url("blob%3Ahttp%3A/127.0.0.1%3A8000/9924a072-76c6-45d3-82c6-1bdbe4fda8e6")
    //var bg_img = document.getElementById('background_profile').style.backgroundImage
    //var profile_pic = document.getElementsByClassName('wrapper')[0].style.backgroundImage
    var name = document.getElementById("Name_here").value
    var bio = document.getElementById("Bio_here").value


    document.getElementById('change_profile_pic').click()
    // updating it in the db
    fetch('/update_profile', {
        method: 'POST',
        body: JSON.stringify({
            name: `${name}`,
            bio: `${bio}`,
            user: `${user}`,
        })
    })
        .then(response => response.json())
        .then(result => {
            console.log(result)
        })

    document.querySelector('#close-modal').click()
    return true;
}

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

