# Retained operational corrections

The first checkpoint script completed archive creation and CRC validation, then its final size-print statement failed with `TypeError: 'int' object is not callable` because `stat().st_size()` incorrectly called a property. Corrected to `stat().st_size` and regenerated the checkpoint/manifest. No experimental data or numerical conclusions were changed.

The certificate selector initially labelled only four-member certificate timing. Independent review identified that the archived control executes one-, two- and four-member certificate calculations separately. The generated selector output now reports their summed recorded timing and labels four-member reuse separately. Ratios and method selections are unchanged. Candidate compilation/setup remains excluded from quantum gate units. The independent selector audit passed after the schema correction.
