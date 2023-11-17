
function show_edit_form(post_id, post_body) {

    const parentElement = document.createElement('div');
    parentElement.id = "parent_post"
    parentElement.className = "modal d-flex flex-column p-3 align-items-center";
    parentElement.style = `top: 20%; 
        margin: auto; 
        right: 25%; 
        left: 25%; 
        width: 300px; 
        background-color: white; 
        height: auto; 
        border: 1px solid gray;
        border-radius: 10px`;
    document.querySelector('#container').append(parentElement)

    const textareaElement = document.createElement('textarea');
    textareaElement.className = "m-2 p-2";
    textareaElement.id = "updated_body";
    textareaElement.innerHTML = post_body;
    parentElement.append(textareaElement);

    const buttonsElement = document.createElement('div');
    buttonsElement.className = "d-flex justify-content-evenly";
    parentElement.append(buttonsElement);

    const saveButton = document.createElement('button');
    saveButton.className = "btn btn-success m-2";
    saveButton.type = "button";
    saveButton.innerHTML = "Save";
    buttonsElement.append(saveButton);
    saveButton.addEventListener('click', () => save_post(post_id));

    const cancelButton = document.createElement('button');
    cancelButton.className = "btn btn-danger m-2";
    cancelButton.type = "button";
    cancelButton.innerHTML = "Cancel";
    buttonsElement.append(cancelButton);
    cancelButton.addEventListener('click', () => cancel_edit(post_id));
}

function show_message(message) {

    const messageElement = document.createElement('div');
    messageElement.className = "m-2 p-2";
    messageElement.id = "message";
    messageElement.style = "position:fixed; top: 8%; left: 25%; right: 25%; color: red;"
    messageElement.innerHTML = message;
    document.querySelector('#container').append(messageElement);

    setTimeout(() => {
        document.getElementById('message').remove();
        document.getElementById('parent_post').remove();
    }, 3000)
}

function save_post(post_id) {

    const corrected_body = document.getElementById('updated_body').value;

    fetch(`/edit/${post_id}`, {
        method: 'POST',
        body: JSON.stringify({
            body: corrected_body,
        })
    })
    .then(async response => {
        
        if (!response.ok) { 
            const message = await response.text(); 
            throw new Error(message);
        }
        return await response.json();
    })
    .then(result => {

            const message = result.message;
            show_message(message);
            document.getElementById(`post_body_${post_id}`).innerHTML = corrected_body;

    })
    .catch( error => {
        show_message(error);
    })
}


function cancel_edit() {
    document.getElementById('parent_post').remove();
}
