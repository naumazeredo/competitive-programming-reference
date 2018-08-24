# Storyboard

## Pages

- index (/)

- login (/login, (hidden) /authentication)

- profile (/profile/\<name\>)
  - User profile (name, avatar, github, problems solved, completion graph?,
    recommended problems?, configure repo)

- repos (/repos)
  - Configured repositories

- subjects (/subjects)
  - Graph with subjects (and completion by user)

- subject page (/subject/\<subject\_name\>)
  - Reference to study, problems to practice and all problems available

- problems (/problems)
  - Problem catalog

- user repositories (/user-repos)
  - User repositories with .cpref file (list all available, which are configured
    already and button to configure a new one. Give option to remove
    configuration and call update on repo)

- user repository info (/user-repo/\<repo\_name\>)
  - Show repository information (problems on catalog, if is up-to-date)

- user repository configuration (/user-repo/\<repo\_name\>/config)
  - Create webhook and add problems to database (if already have webhook just
    updates problems)

- webhook callback ((hidden) /webhook)
  - Call update on repository
