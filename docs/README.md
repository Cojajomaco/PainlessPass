# User Stories and Mis-User Stories
My goal is to implement all of these use-cases, time and ability willing. 
<br><br>

Format: 
1. Story
    * Acceptance/Mitigation Criteria
<br><br>
## User Stories
1. As a user, I want to store my passwords, so I can have secure access to all of my logins. 
    * Passwords are stored within the program. 

2. As a user, I want to generate passwords, so I can create secure default logins. 
    * A password generator is available in the web application.

3. As a user, I want to search my passwords, so I can access them easily. 
    * User passwords are searchable via certain fields (title, description, website).

4. As a user, I don’t want others to view my passwords, so my passwords are kept secure. 
    * Passwords are hidden by default and locked behind access controls (only user A can access user A's passwords).

5. As a user, I want to organize my passwords, so they can be accessed easily. 
    * A folder structure is available to sort passwords.

6. As a user, I want to store information with my passwords, so I can know what purpose they had. 
    * Passwords have multiple fields to indicate website, description, and title. 

7. As a user, I want to use MFA for my account, to guarantee the security of my passwords. 
    * Security settings allow mutlifactor to be set-up (maybe set as a secure default?).

8. As an admin, I want to use MFA for my account, to guarantee the security of my deployment. 
    * Admin accounts can enable MFA manually. 

9. As an admin, I want to restrict access to the admin console, to guarantee the security of my deployment. 
    * The web console should be restricted with an easy toggle or flag (perhaps included in instructions for Docker?).

10. As an admin, I want the application to be deployed easily, so I can lower administrative overhead. 
    * The application is deployable via Docker with minimal steps required. 

11. As an admin, I want to delete users, so I can clean up the database to prevent liability. 
    * The application includes a webpage for deleting users (perhaps sortability via last logon timestamp?).

12. As an admin, I do not want to view user passwords, so I cannot be held liable for their accounts. 
    * The application does not store passwords in a way where administrators can view user passwords. 

13. As a user or admin, I want to view log data, so I can see unauthorized access to my account.
    * The application stores log data of user actions, such as: viewing a password, changing a password, deleting a password, logging into the account, changing settings.
 
14. As a user, I want to have copies of my passwords, so I can access them if the service goes offline.
    * The application allows users to export their passwords for offline storage. 

## Mis-User Stories

1. As a malicious actor, I want to view other account's passwords, so I can user other people’s credentials. 
    * User passwords are only available to the user who created the password entry. 

2. As a malicious actor, I want to deny access to the service, so the site’s reputation is harmed. 
    * The application recovers gracefully from errors or exceptions and scales workloads efficiently. 

3. As a malicious actor, I want to inject bad data to corrupt the database, so the web application is harmed. 
    * All user input is sanitized prior to entering the database.

4. As a malicious actor, I want to upload malicious code, to exploit the web server. 
    * All user input is sanitized prior to being processed by the server. 

5. As a rogue admin, I want to view user’s passwords in plaintext, so I can utilize their data for my own gain. 
    * All user passwords are stored in a way which requires the user's application credentials to view. 
