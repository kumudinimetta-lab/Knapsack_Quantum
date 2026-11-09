# Compilation attempts

No research experiment or raw data was modified. These are document-build attempts.

1. Restricted MiKTeX invocation exited3221226505 before compiling: RegOpenKeyExW access denied for Software/MiKTeX.org/MiKTeX/2.9/Core and CreateDirectoryW denied under the user MiKTeX profile. It misleadingly reported a fresh installation. No package installation was attempted.
2. Normal settings access was approved by the tool reviewer. The first normal invocation reached the original paper/main.aux and failed at its stale `\\Newlabel` command, which belongs to the earlier template. No source workaround was added.
3. A clean build directory was created under this audit folder, with copies of the revised source, bibliography and figures. pdflatex/bibtex/pdflatex/pdflatex completed. A rerun warning remained, so a final extra pdflatex pass was added after the last semantic corrections.
4. The final five passes all exited0. BUILD_RESULTS.json and build_1.log through build_5.log describe this final build. A previous build log was overwritten by the routine driver before attempt-specific logging was introduced; its failure details are preserved here from the observed tool output, not represented as surviving raw stdout. Final artifacts reside in latex_build; only its successfully compiled PDF is copied to paper/main.pdf. Old paper/main.aux and .bbl are not used for the final PDF.

Final warnings: one float-placement substitution and a33.33115pt overfull table in the untouched bounding-oracle body section (source lines265--277). No undefined citations or references; no BibTeX warnings. The reviewed literature table and references were visually checked separately. A clean document build does not approve the stale scientific content outside the literature-review scope.
