# Contributing
- [How to contribute](#How to contribute)
- [What to contribute](#What to contribute)
- [Discussion](#Discussion)
  * [Code of Conduct](#Code of Conduct)
  * [Highlighted rules](#Highlighted rules)
- [Roles](#Roles)
- [Development](#Development)
  * [Installation](#Installation)
  * [RTC Model](#RTC Model)
  * [Coding style guidelines](#Coding style guidelines)
  * [Pull request guidelines](#Pull request guidelines)
- [Infrastructure](#Infrastructure)
  * [Continuous integration](#Continuous integration)

## How to contribute
Contributions are welcome and are greatly appreciated! Every little bit helps, and credit will always be given.

## What to Contribute
Check out our open list of [issues](https://github.com/epam/OSCI/issues).

## Discussion

If you've run into behavior in OSCI you don't understand, or you're
having trouble working out a good way to apply it to your code, or
you've found a bug or would like a feature it doesn't have, we want to
hear from you!

Our main forum for discussion is the project's [GitHub issue
tracker](https://github.com/epam/OSCI/issues).  This is the right
place to start a discussion of any of the above or most any other
topic concerning the project.

#### Code of Conduct

Everyone participating in the OSCI community, and in particular in our
issue tracker, pull requests is expected to treat
other people with respect and more generally to follow the guidelines
articulated in the [Python Community Code of
Conduct](https://www.python.org/psf/codeofconduct/).

#### Highlighted rules

   * Don't take it personally if your contribution is not accepted. The reviewer should have explained the reasons clearly.
   * All discussions of issues and review feedback must be objective and use neutral tone of language. We are professionals.

## Roles
OSCI recognizes two types of roles:
  * __A Contributor__ is a user who contributes to a project in the form of code 
  	or documentation. Developers take extra steps to participate in a project,
  	are active on the developer forums, participate in discussions, 
  	provide PRs (patches), documentation, suggestions, and criticism.
  	Contributors are also known as developers.
  * __A Committer__ is a developer that was given write access to the code 
  	repository. Not needing to depend on other people to commit their patches,
  	they are actually making short-term decisions for the project. By submitting 
  	your code or other content to the project via PR or a patch, a Committer
  	agrees to transfer the contribution rights to the Project.
  From time to time, the project's committership will go through the list of 
  contributions and make a decision to invite new developers to become a project
  committer.


## Development

### Installation
Find OSCI installation guide in our [README file](README.md).

### RTC model

OSCI supports Review-Then-Commit model of development. The following rules are 
used in the RTC process:
  * a developer should seek peer-review and/or feedback from other developers
  	through the PR mechanism (aka code review).
  * a developer should make a reasonable effort to test the changes before 
  	submitting a PR for review.
  * any non-document PR is required to be opened for at least 24 hours for
    community feedback before it gets committed unless it has an explicit +1
    from a committer
  * any non-document PR needs to address all the comment and reach consensus
    before it gets committed without a +1 from other commiters
  * a committer can commit documentation patches without explicit review process.
  	However, we encourage you to seek the feedback.
  	
### Coding style guidelines
OSCI uses [PEP - 8 for Python Styleguide](https://www.python.org/dev/peps/pep-0008/) - the most common coding conventions.

### Pull Request Guidelines

Before you submit a pull request from your forked repo, check that it
meets these guidelines:
 
* Always wait for tests to pass before merging PRs.
* Always create tests covering new functionality. All tests should be included in the pipeline testing.
* Don't mix more than one issue or feature in a single PR. This complicates the review and merge process.
* All PR reviews should be done objectively and in-line with the goals and standards of the project.
* All PR feedback should justify clearly the reasons why changes are needed or the PR not accepted.
* Add an [GPLv3 License](https://www.gnu.org/licenses/gpl-3.0.en.html) header to all new files
* Use "[Squash and merge](https://github.com/blog/2141-squash-your-commits)"
  to merge PRs.
* Edit the final commit message before merging to conform to the following
  style (we wish to have a clean `git log` output):
  * When merging a multi-commit PR make sure that the commit message doesn't
    contain the local history from the committer and the review history from
    the PR. Edit the message to only describe the end state of the PR.
  * Make sure there is a *single* newline at the end of the commit message.
    This way there is a single empty line between commits in `git log`
    output.
  * Split lines as needed so that the maximum line length of the commit
    message is under 80 characters, including the subject line.
  * Capitalize the subject and each paragraph.
  * Make sure that the subject of the commit message has no trailing dot.
  * Use the imperative mood in the subject line (e.g. "Fix typo in README").
  * If the PR fixes an issue, make sure something like "Fixes #xxx." occurs
    in the body of the message (not in the subject).
  * Use Markdown for formatting.

PS: Please read this excellent [article](http://chris.beams.io/posts/git-commit/) on
commit messages and adhere to them. It makes the lives of those who
come after you a lot easier.

## Infrastructure

### Continuous integration
All committed code is tested using [Travis CI](https://travis-ci.org/). Configuration file: [.travis.yml](.travis.yml) For every commit, Travis runs all the unit tests.

