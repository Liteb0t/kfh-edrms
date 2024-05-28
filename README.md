This was a University assignment where we had to create a high-fidelity prototype of an Electronic Documents & Records Management System, or EDRMS, for our external client Kuwait Finance House. 


### Achievements
The software implementation was marked 90% (an A).

Our focus was functionality first, design second. Instead of bloating the website with javascript, we use pure CSS to show the user all that he or she needs to see.

We have a full account management system where admins can add and delete users, and manage permissions. Employees can reset their password with the help of a secure link sent by e-mail.

Documents can be uploaded, previewed and deleted, with permissions requirements for each action. On each document is an audit trail showing upload date and author, as well as who grants what permission to whom.

### Shortcomings
The goal of integrating a linux-style permission system was not fulfilled. An employee can not request permissions from groups, only individual users.

The biggest flaw is that an employee does not need any permissions to accept another's access request. This is a major security hole and would make this software a non-starter had it not been a prototype. I know how to fix this, but simply didn't have time before the deadline.
