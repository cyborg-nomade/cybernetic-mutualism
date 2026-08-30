# project workflow

## unit of work

Each research item is developed in its own chat. This normally includes every
item in the roadmap, while allowing separate chats for editorial,
infrastructural, or exploratory work that falls outside the roadmap.

One chat corresponds to one feature branch and one pull request:

```text
chat → feature branch → commits → pull request → review and merge
```

This keeps the conversation, research scope, repository history, and review
boundary aligned.

## lifecycle

1. Start a new chat with a clearly scoped outcome.
2. Update local `main` from `origin/main` before creating the branch.
3. Create a descriptive feature branch for that chat.
4. Keep all of the chat's deliverables on that branch, including texts, sources,
   models, code, data, and documentation.
5. Validate the deliverables in proportion to their form: check citations and
   claims, run tests for code, and inspect rendered publication drafts.
6. Commit coherent milestones as the work develops.
7. End the chat by opening a pull request against `main` that summarizes the
   deliverables, unresolved questions, and verification performed.
8. The project owner reviews and merges the pull request.

Follow-up work discovered during a chat may remain in the same branch when it is
necessary to complete that chat's outcome. A materially separate research item
belongs in a new chat and feature branch.

## branch names

Use short lowercase names separated by hyphens. Prefer the subject of the work
over a generic task number, for example:

```text
manifesto-point-01-antinomies
case-platform-cooperatives
simulation-federation-topology
publishing-citations
```

The pull-request title should describe the outcome rather than repeat the branch
name mechanically.

## merging

Do not commit new project work directly to `main`. After a pull request is
merged, update local `main` before starting the next chat's branch. Delete merged
feature branches when convenient; the pull request and Git history preserve the
record.
