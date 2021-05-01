document.addEventListener('DOMContentLoaded', function() {

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



  document.querySelector('#compose-form').addEventListener('submit', function(event){
    event.preventDefault();
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    })
    .then(load_mailbox('sent'));
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  });


  return false
};


function show_mails(mailbox, mails){
  const mailsDiv = document.querySelector('#emails-view');
  mailsDiv.value = ''

  mails.forEach(mail => {
    const div = document.createElement('div')
    div.className = "row mail";
    div.innerHTML = "<div class='col 2'>"+ mail.sender + "</div>" +
      "<div class='col 2 float-left'>" + mail.subject + "</div>" 
      + "<div class='col 8 float-right'>" + mail.timestamp + "</div>";

    // Change the mail div's backgroud color according to the read status
    if (mail.read === true){
      div.style.background = 'lightgray'
    } else {
      div.style.background = 'white'
    };

    div.addEventListener('click', function(){ 
      fetch(`/emails/${mail.id}`)
      .then(response => response.json())
      .then(data => {open_mail(mailbox, data);
      console.log(data)})
      .catch(error => {
          console.log('Error:', error);
      });

      // Mark a mail as read when it has been clicked on
      fetch(`/emails/${mail.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      });
      
    });

    mailsDiv.append(div)
  });
};

 function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none'
  document.querySelector('#compose-view').style.display = 'none';

  document.querySelector('#emails-view').value = '';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

   fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(data => {show_mails(mailbox, data);
    console.log(data)})
    .catch(error => {
      console.log('Error:', error);
    });
};


function open_mail(mailbox, mail){

  if (mailbox === 'inbox'){
    action = 'archive'
    archived = true
    document.querySelector('#email-view').innerHTML = `<button class='btn btn-sm btn-outline-primary float-right' id=${action}>${action}</button>` +
    "<button class='btn btn-sm btn-outline-primary float-right' id='reply'>reply</button>"
  } else if (mailbox === 'archive'){
    action = 'unarchive'
    archived = false
    document.querySelector('#email-view').innerHTML = `<button class='btn btn-sm btn-outline-primary float-right' id=${action}>${action}</button>`
  } else{
    document.querySelector('#email-view').innerHTML = ""
  };

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  const email_div = document.createElement('div');
  
  email_div.innerHTML = 
  "<div class=''><strong>From:</strong> " + mail.sender + "</div>" +
  "<div class=''><strong>To:</strong> " + mail.recipients + "</div>" +
  "<div class=''><strong>Subject:</strong> " + mail.subject + "</div>" +
  "<div class=''><strong>Timestamp:</strong> " + mail.timestamp + "</div>" + 
  "<hr>" +
  "<div class=''>" + mail.body + "</div>";
  
  document.querySelector('#email-view').append(email_div)
  
  // Load inbox mailbox when a mail is archived or unarchived (frominbox and archive mailboxes only)
  if (['inbox', 'archive'].includes(mailbox)){
    // Mark a mail as archived or unarchived depending on the action that is called
    document.querySelector(`#${action}`).addEventListener('click', () => {
        fetch(`/emails/${mail.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: archived
        })
      })
      .then(// Load inbox after action on archive status
      load_mailbox('inbox'));
      
    });
    
    // Load compose mailbox when reply button is clicked and préfill the form (reply from inbox only)
    if (mailbox === 'inbox'){
      
        document.querySelector('#reply').addEventListener('click', function(){
          document.querySelector('#emails-view').value = '';
          document.querySelector('#compose-recipients').value = mail.sender;
          document.querySelector('#compose-subject').value = "Re:" + mail.subject;
          document.querySelector('#compose-body').value = `On ${mail.timestamp} ${mail.sender} wrote:` + mail.body + "\n" + "-----------" + "\n" 

          document.querySelector('#email-view').style.display = 'none';
          
          compose_email();
      });
    };
  };
};