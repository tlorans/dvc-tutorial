[Home](../README.md) › Page 4 of 4

# 4. Good habits

1. **Never put data in git.** If a file is bigger than a few hundred kilobytes, it belongs to DVC.
2. **Never edit an output by hand.** Change the code or a setting, then `repro`.
3. **Push after you commit a receipt.** A `dvc.lock` or `.dvc` file without pushed data is a broken
   promise to your colleagues.
4. **After switching branches or commits, pull (or `dvc checkout`).** Otherwise your data
   doesn't match your code.
5. **Put settings in a config file, not in the code.** Then DVC can track exactly which settings a
   stage uses, and `params diff` shows what changed.
6. **Keep small results as metrics.** They show up in every pull request.
7. **Pin downloads with a snapshot date.** Then you always know which data a result used.
8. **Agree on one commit rule** (A or B, [section 5](3-your-own-project.md#what-do-i-commit-after-a-run)) and write it down.
9. **When in doubt, `status` first.** It never changes anything.
10. **Keep repositories in `C:\projects`, outside OneDrive.**
11. **Close Excel before `pull`, `checkout` or `repro`.** Windows won't let DVC replace a file that
    Excel has open. To look at results, copy the file somewhere else first.

## You've finished the tutorial

- Keep the [cheat sheet](cheat-sheet.md) at hand.
- If something goes wrong, see [When something goes wrong](troubleshooting.md).

---

← [Previous: DVC in your own project](3-your-own-project.md)
