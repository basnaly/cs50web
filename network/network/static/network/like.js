
function like(post_id) {

    fetch(`/like/${post_id}`, {
        method: 'POST',
    }).then(response => response.json())
        .then(result => {

            const message = result.message;
            let counter = document.getElementById(`like_${post_id}`).innerHTML; 
            counter = +counter + 1;
            document.getElementById(`like_${post_id}`).innerHTML = counter;
            document.getElementById(`click_button_${post_id}`).classList.remove("btn-light");
            document.getElementById(`click_button_${post_id}`).classList.add("bg-success-subtle");
            document.getElementById(`click_button_${post_id}`).onclick = () => unlike(post_id);

        })
        .catch(error => {
            show_message(error);
        })
}

function unlike(post_id) {

    fetch(`/unlike/${post_id}`, {
        method: 'POST',
    }).then(response => response.json())
        .then(result => {

            let counter = document.getElementById(`like_${post_id}`).innerHTML; 
            counter = +counter - 1;
            document.getElementById(`like_${post_id}`).innerHTML = counter;
            document.getElementById(`click_button_${post_id}`).onclick = () => like(post_id);
            document.getElementById(`click_button_${post_id}`).classList.add("btn-light");
            document.getElementById(`click_button_${post_id}`).classList.remove("bg-success-subtle");
        })
        .catch(error => {
            show_message(error);
        })
}
