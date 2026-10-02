# Validation record

Scope: Global root login, password authentication, empty passwords and X11 forwarding set to yes.

Local checks to rerun:

```sh
python -m unittest discover -s tests -v
python cli.py --help
python -m compileall -q review.py cli.py tests
```

Check the exact public GitHub commit and its workflow run separately after publishing. Tests use synthetic input; no production system or external target is exercised. Include and Match blocks, defaults, command-line overrides and server-effective configuration are not evaluated.

## Current source result (2026-10-02)

- Python 3.14.6: 7/7 unit and CLI integration tests passed.
- Tests include the specific malformed-input, incomplete-review and declaration cases added during the source audit.
- Quoted selected values and equals separators are interpreted. Include directives remain explicit unresolved findings; selected declarations in Match sections are reviewed without asserting which connections match them.
- Test input is synthetic. No external target, live credential or production cluster is exercised.
- The public commit and its corresponding GitHub workflow must be verified separately after this update.
