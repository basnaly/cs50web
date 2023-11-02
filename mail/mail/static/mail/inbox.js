document.addEventListener('DOMContentLoaded', function () {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);

    // By default, load the inbox
    load_mailbox('inbox');
});

function compose_email() {
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';

    document.querySelector('#compose-form').onsubmit = save_form;
}

function load_mailbox(mailbox) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    show_emails(mailbox);
}

function save_form() {

    recipients = document.querySelector('#compose-recipients').value;
    subject = document.querySelector('#compose-subject').value;
    body = document.querySelector('#compose-body').value;

    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: body
        })
    })
        .then(response => response.json())
        .then(result => {
            console.log(result);

            document.querySelector('#compose-message').innerHTML = result.message
            setTimeout(() => {
                document.querySelector('#compose-message').innerHTML = '';
                document.getElementById('sent').click(); //move to sent page
            }, 5000)

            document.querySelector('#compose-recipients').value = '';
            document.querySelector('#compose-subject').value = '';
            document.querySelector('#compose-body').value = '';
        })
        .catch(error => {
            console.log('Error:', error);
        });
    return false; //to avoid default form action
}

function show_emails(mailbox) {

    fetch(`/emails/${mailbox}`)
        .then(response => response.json())
        .then(emails => {
            console.log(emails);

            for (let email of emails) {

                const parentElement = document.createElement('div');
                parentElement.className = "d-flex p-2 border ";
                document.querySelector('#emails-view').append(parentElement);

                if (email.read === true) {
                    parentElement.style = "background-color: lightgray";
                }
                
                const senderElement = document.createElement('div');
                senderElement.className = "me-3";
                senderElement.innerHTML = email.sender;
                parentElement.append(senderElement);

                const subjectElement = document.createElement('div');
                subjectElement.className = "fw-bold";
                subjectElement.innerHTML = email.subject;
                parentElement.append(subjectElement);

                const timestampElement = document.createElement('div');
                timestampElement.className = "ms-auto";
                timestampElement.innerHTML = email.timestamp;
                parentElement.append(timestampElement);
            }
            
        })
        .catch(error => {
            console.log('Error:', error);
        })

}