# Issue tracker: GitHub

Issues and specs live in caw1517/D385-Assesment1.
Use the gh CLI with --repo caw1517/D385-Assesment1.

- Create: gh issue create --title "..." --body-file <path>
- Read: gh issue view <number> --comments
- List: gh issue list --state open --json number,title,body,labels
- Comment: gh issue comment <number> --body-file <path>
- Label: gh issue edit <number> --add-label "..."
- Remove label: gh issue edit <number> --remove-label "..."
- Close: gh issue close <number>

When a skill says “publish to the issue tracker,” create an issue.
When it says “fetch the relevant ticket,” read the issue and comments.

## Pull requests as a triage surface

PRs as a request surface: no.
