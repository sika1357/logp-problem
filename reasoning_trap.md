# Reasoning trap

The trap
Three archives, three benzamide-piperazine candidates differing only by a halogen. The prompt names
which candidate is graded but not which archive holds it, and separately frames an "optimal drug"
log P window (1.0-5.0) as background color - nothing in the prompt connects that framing to archive
identity, or warns against using it that way. A solver who runs the (otherwise correct) HPLC-to-logP
procedure on all three archives and picks whichever result looks like the most plausible drug
candidate, instead of working through the disclosed exact-mass match, lands on a clean,
self-consistent, wrong number.

The numbers
The plausibility pick (a clean, mid-range value) is roughly 37x the 0.05 tolerance away from the
mass-spectrometry-confirmed archive's value.

The tell
Every candidate's SMILES (hence exact mass, computable with RDKit) is disclosed, and a
high-resolution mass reading per archive is available via query_oracle - a solver has everything
needed to make the match unprompted. Nothing in the prompt states that this is the intended route,
or that plausibility is the wrong one; the resolution has to be originated, not followed.

Why it is fair
The disclosed formulas plus the oracle's mass reading are the only route to a confident, factual
resolution of archive identity. The drug-optimal framing is real domain color, stated once, never
tied to archive identity anywhere in the prompt - a solver who reaches for it as a shortcut is
applying their own (incorrect) inference, not following a hint the task planted.
