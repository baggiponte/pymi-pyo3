bump:
    cz bump --check-consistency || exit
    git push
    git push --tag

dry-bump:
    cz bump --check-consistency --dry-run
