# slides have moved

The maintained slides are at <https://talks.baggiponte.com/pymi-pyo3/>.
Their source and shared build live in [baggiponte/talks](https://github.com/baggiponte/talks).

This repository now publishes only dependency-free redirects from its original
GitHub Pages URLs. No repository or history was deleted or renamed.

[Original slides and examples](https://github.com/baggiponte/pymi-pyo3/tree/slides-before-migration-2026-10-24)
are retained in the `slides-before-migration-2026-10-24` tag and Git history.
Those examples are historical, unmaintained, and may contain vulnerable dependencies;
do not use them as current production templates.

The manually dispatched `pages.yaml` workflow publishes only `site/`. Deep links
first return a Pages 404, then redirect in the browser while preserving path,
query and fragment. Without JavaScript the fallback opens the new deck root.
