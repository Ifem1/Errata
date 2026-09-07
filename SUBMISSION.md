# Submission evidence

Errata is a standalone reusable Intelligent Contract primitive. It has no frontend, wallet UI, backend, database, or unrelated product layer.

The public evidence pages are:

- [initial publication](https://raw.githubusercontent.com/Ifem1/Errata/main/evidence/initial.txt)
- [confirmation publication](https://raw.githubusercontent.com/Ifem1/Errata/main/evidence/confirmation.txt)
- [correction publication](https://raw.githubusercontent.com/Ifem1/Errata/main/evidence/correction.txt)

Verified proof: claim 1 was current; CanonGate succeeded; confirmation revision 2 was `CONFIRMS` and left canon version 1/current revision 1 unchanged; CanonGate succeeded again; correction revision 3 advanced canon version to 2 and changed the canon hash; claim 1 read back as lazy `STALE`; CanonGate rejected it; claim 2 was created on revision 3 and CanonGate succeeded. All writes finalized with majority agreement. Transaction evidence is recorded in [DEPLOYMENT.md](DEPLOYMENT.md).
