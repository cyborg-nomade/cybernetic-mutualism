# project workflow

## unit of work

Each research cycle is coordinated in its own chat. The chat retains the
decisions, dependencies, and handoffs that connect the cycle's individual
research items. Separate chats remain appropriate for editorial,
infrastructural, or exploratory work outside the active cycle.

Branches and pull requests remain item-sized:

```text
cycle chat → item branch → commits → pull request → review and merge
           → next item branch → commits → pull request → review and merge
```

This keeps the cycle's reasoning in one conversation without forcing models,
essays, evidence passes, and decision records into one oversized review.

## lifecycle

1. Start a new chat for a declared research cycle and record its completion and
   decision criteria.
2. Select the next item whose dependencies are satisfied.
3. Update local `main` from `origin/main` before creating the item branch.
4. Create a descriptive feature branch for that item.
5. Keep the item's deliverables on that branch, including texts, sources,
   models, code, data, and documentation.
6. Validate the deliverables in proportion to their form: check citations and
   claims, run tests for code, and inspect rendered publication drafts.
7. Commit coherent milestones as the work develops.
8. Open a pull request against `main` that summarizes the
   deliverables, unresolved questions, and verification performed.
9. The project owner reviews and merges the pull request.
10. Return to the cycle chat, update `main`, and select the next unblocked item.
11. Close the chat only when the cycle's decision record applies its declared
    completion criteria or explicitly records why the cycle stopped.

Follow-up work may remain in the same branch when it is necessary to complete
that item's outcome. A materially separate item normally receives a new branch
and pull request while remaining in the same cycle chat.

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
merged, update local `main` before starting the next item branch. Delete merged
feature branches when convenient; the pull request and Git history preserve the
record.
