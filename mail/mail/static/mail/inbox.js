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

    const exist_email = document.getElementById('parent-email');
    if (exist_email) {
        exist_email.remove();
    }
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

    const exist_email = document.getElementById('parent-email');
    if (exist_email) {
        exist_email.remove();
    }

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

            for (let email of emails) {

                const parentElement = document.createElement('div');
                parentElement.className = "d-flex p-2 border";
                document.querySelector('#emails-view').append(parentElement);
                parentElement.addEventListener('click', () => {
                    show_email(email.id, mailbox);
                    parentElement.style = "background-color: lightgray";
                });

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
        });
}

function show_email(email_id, mailbox) {

    const exist_email = document.getElementById('parent-email');
    if (exist_email) {
        exist_email.remove();
    }

    fetch(`/emails/${email_id}`)
        .then(response => response.json())
        .then(email => {
            console.log(email);

            const parentElement = document.createElement('div');
            parentElement.className = 'd-flex flex-column shadow-lg p-3 position-fixed bg-primary-subtle fw-medium';
            parentElement.id = 'parent-email';
            parentElement.style = "top: 25%; left: 25%; right: 25%; border-radius: 1rem";
            document.querySelector('.container').append(parentElement);

            const closeElement = document.createElement('button');
            closeElement.type = 'button';
            closeElement.className = 'btn-close ms-auto';
            parentElement.append(closeElement);
            closeElement.addEventListener('click', () => parentElement.remove())

            const senderElement = document.createElement('div');
            senderElement.className = 'p-1';
            senderElement.innerHTML = 'Sender: ' + email.sender;
            parentElement.append(senderElement);

            const recipientsElement = document.createElement('div');
            recipientsElement.className = 'p-1';
            recipientsElement.innerHTML = 'Recipients: ' + email.recipients.join(', ');
            parentElement.append(recipientsElement);

            const subjectElement = document.createElement('div');
            subjectElement.className = 'p-1';
            subjectElement.innerHTML = 'Subject: ' + email.subject;
            parentElement.append(subjectElement);

            const bodyElement = document.createElement('div');
            bodyElement.className = 'p-1';
            bodyElement.innerHTML = 'Body: ' + email.body;
            parentElement.append(bodyElement);

            const timestampElement = document.createElement('div');
            timestampElement.className = 'p-1';
            timestampElement.innerHTML = 'Timestamp: ' + email.timestamp;
            parentElement.append(timestampElement);

            const buttonsElement = document.createElement('div');
            buttonsElement.className = 'd-flex justify-content-evenly mt-4 mb-2';
            parentElement.append(buttonsElement);

            const archiveElement = document.createElement('button');
            archiveElement.type = 'button';
            archiveElement.className = 'btn btn-secondary';

            if (email.archived === true) {
                archiveElement.innerHTML = 'Unarchive';
            }
            else {
                archiveElement.innerHTML = 'Archive';
            }

            if (mailbox != 'sent') {
                buttonsElement.append(archiveElement);
            }
            

            archiveElement.addEventListener('click', () => {
                if (email.archived === true) {
                    unarchive(email.id);
                    parentElement.remove();
                    document.getElementById('inbox').click();    
                }
                else {
                    archive(email.id);
                    parentElement.remove();
                    document.getElementById('archived').click();
                }   
            })

            const replyElement = document.createElement('button');
            replyElement.type = 'button';
            replyElement.className = 'btn btn-secondary';
            replyElement.innerHTML = 'Reply';
            buttonsElement.append(replyElement);
            replyElement.addEventListener('click', () => show_reply_form(email))

            read_email(email_id);

        })
        .catch(error => {
            console.log('Error:', error);
        });
}

function read_email(email_id) {

    fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      });
}

function archive(email_id) {

    fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
      })
}

function unarchive(email_id) {

    fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: false
        })
      })
}

function show_reply_form(email) {

    compose_email();
    document.querySelector('#compose-recipients').value = email.sender;
    document.querySelector('#compose-subject').value = 'Re: ' + email.subject;
    document.querySelector('#compose-body').value = email.body;

    document.querySelector('#compose-form').onsubmit = reply_email;
}

function reply_email() {

    recipients = document.querySelector('#compose-recipients').value;
    subject = document.querySelector('#compose-subject').value;
    body = document.querySelector('#compose-body').value;

    fetch(`/emails`, {
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
        })
        .catch(error => {
            console.log('Error:', error);
        })
        return false;    
}