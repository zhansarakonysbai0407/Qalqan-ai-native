# Qalqan MVP plan

## Problem
A person facing a dangerous situation may need a fast way to alert trusted people and share their location. Qalqan is a proposed safety app, not a replacement for official emergency services.

## Intended users
People in Kazakhstan who want a prepared way to alert trusted contacts during an emergency.

## Goals
- Provide two deliberate SOS activation paths.
- Notify up to five trusted contacts using configured push and SMS services.
- Share location updates during an active SOS when device permissions and connectivity permit.
- Require a preconfigured PIN to end an active SOS.
- Support Kazakh, Russian and English in the MVP.

## Explicitly deferred
- Risk-zone map: deferred to a later version.
- Any direct integration with police/emergency dispatch: not assumed and requires separate verification/authorization.
- Application implementation: blocked until requirements, including Safe Walk, are finalized.

## Requirements already decided
- Activation: tap + confirmation, or press and hold for quick activation.
- End SOS: PIN required.
- Contacts: maximum five.
- Alerts: push and SMS through configured providers.
- Location: live updates during active SOS.
- Languages: Kazakh, Russian, English.

## Unresolved requirement
Safe Walk: decide whether it is included in MVP, deferred, or includes automatic escalation after a missed check-in.

## Non-functional and safety requirements
- Clear permission prompts and visible indication while location is shared.
- Handle denied permissions, lost GPS, no network, provider errors, and background restrictions.
- Do not state that an alert was delivered unless delivery is confirmed by the provider.
- Securely store PIN verification data; do not store a plaintext PIN.
- Minimize sensitive data retention and restrict access to location history.
- Provide localized interface and accessible SOS controls.

## Release gates
1. Brainstorm requirements complete.
2. PM review of scope and acceptance criteria.
3. Architecture and threat/risk review before implementation.
4. Implementation and QA only after scope approval.
5. Real provider integrations tested before any claim of real delivery.