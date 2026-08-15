## Summary

Describe the public website or repository-quality change and why it is needed.

## Scope

List the files, pages, validators, metadata, or GitHub configuration intentionally changed.

## Validation

- [ ] I ran the relevant dependency-free Python validators.
- [ ] I ran `node --check js/theme-init.js` and `node --check js/main.js` when JavaScript changed.
- [ ] I reviewed the final diff for unrelated or accidental changes.
- [ ] Public-facing claims in this pull request match the implemented or documented GoreeCloud state.

## Accessibility and resilience

- [ ] Interactive or navigation changes preserve keyboard access and visible focus behavior.
- [ ] The site remains useful when JavaScript is unavailable unless the changed feature is explicitly progressive enhancement.
- [ ] Reduced-motion, contrast, forced-colors, print, and error-page behavior were considered when relevant.

## Privacy and security boundary

- [ ] This pull request contains no passwords, API keys, tokens, private keys, credentials, private hostnames, private IP addresses, internal-only service locations, private family information, or recovery secrets.
- [ ] External browser resources were not introduced without explicit justification and review.
- [ ] Security vulnerability details are not disclosed in this pull request; sensitive reports use https://www.goreecloud.com/security.html.
- [ ] Public security/privacy statements were updated if this change materially alters the behavior they describe.

## Release boundary

- [ ] I understand that passing CI does not by itself authorize merging, production deployment changes, DNS changes, or repository-visibility changes.
- [ ] Any source-license or repository-publication decision remains governed separately until issue #5 is explicitly resolved.

## Notes for review

Add any remaining tradeoffs, visual-review notes, follow-up work, or intentionally deferred decisions.
