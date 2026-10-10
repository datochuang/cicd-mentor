This directory is the fake Perforce depot for the simulation.
- "p4 changes" = read .p4/changes.txt ; "p4 describe N" = the row for N (no per-file diff available)
- The depot is READ-ONLY for the agent. Shelving a CL = writing a directory shelved/CL-<name>/ (outside the depot)
  containing the new/changed files plus a DESCRIPTION.md (what/why/how verified), nothing else.
- There is no real vcs/p4. "Running sanity" = describe what you ran; if a script references things that do not exist here, that is the finding.
- A pending shelved CL from a person appears as .p4/shelved-<CL>/ (files at their depot-relative paths + DESCRIPTION.txt).
  "p4 unshelve" = read those files. It is not in the depot until the owner submits.
