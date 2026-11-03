# Qalqan — brainstorm history

This document records the actual brainstorming decisions and the subsequent product decision authorized by the project owner. It is a concise record, not a complete export of the chat UI.

## Idea
**Qalqan** (Қалқан, “shield”) is a proposed personal-safety app for people in Kazakhstan who may need help during an emergency, including domestic violence, street attacks, or other dangerous situations.

Potential core flow: activate SOS, notify trusted contacts, share location, and provide access to emergency-service contact information. The app must not imply that police or emergency services receive a signal unless an official, tested integration exists.

## Confirmed MVP decisions
1. **Risk-zone map:** defer to a later version.
2. **MVP languages:** Kazakh, Russian, and English.
3. **SOS ending:** end an SOS only after the user enters a PIN set in advance.
4. **SOS activation:** tap with confirmation, or press and hold for rapid activation.
5. **Trusted-contact notifications:** push notifications and SMS through configured services. Actual delivery depends on integration and testing.
6. **Trusted contacts limit:** up to five contacts.
7. **Location sharing:** location updates during an active alarm, subject to permission, GPS, connectivity and OS background limits.
8. **Safe Walk:** include a limited MVP with a timer and manual safe check-ins. Do not automatically alert contacts after a missed check-in in this MVP. This is the conservative choice to avoid false-positive escalation; automatic escalation can be reconsidered after explicit product and safety review.

## Safety and reliability constraints
- Ask permission before accessing location and explain when location is shared.
- Do not claim continuous location updates when permissions, GPS, network or OS behavior prevent them.
- Do not claim SOS notifications were delivered without a confirmed provider response.
- Emergency-service integration is out of scope unless separately researched, authorized and tested.
- A PIN helps prevent accidental termination but is not a substitute for a carefully designed threat model.
- Document offline and service-failure behavior before release.

## Workflow rule
Every implementation task must have a GitHub Issue with verifiable acceptance criteria. QA must record actual evidence; do not invent test results or deployment status.
