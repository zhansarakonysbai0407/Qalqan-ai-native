# Qalqan — brainstorm history

This document records the actual brainstorming decisions captured in the ChatGPT conversation. It is a concise reconstruction of the conversation's decisions, not a complete export of the chat UI.

## Idea
**Qalqan** (Қалқан, “shield”) is a proposed personal-safety app for people in Kazakhstan who may need help during an emergency, including domestic violence, street attacks, or other dangerous situations.

Potential core flow: activate SOS, notify trusted contacts, share location, and provide access to emergency-service contact information. The app must not imply that police or emergency services receive a signal unless an official, tested integration exists.

## Decisions captured

1. **Risk-zone map:** Option B — defer the risk-zone map to a later version.
2. **MVP languages:** Option C — Kazakh, Russian, and English.
3. **SOS ending:** Option C — end an SOS only after the user enters a PIN set in advance.
4. **SOS activation:** Option C — two activation methods: tap with confirmation, or press and hold for rapid activation.
5. **Trusted-contact notifications:** Option D — push notifications and SMS through configured services. Actual delivery depends on integration and testing.
6. **Trusted contacts limit:** Up to five contacts.
7. **Location sharing:** Option B — update location in real time during an active alarm. This depends on location permissions, GPS, connectivity, and OS background restrictions.

## Open requirement
**Safe Walk is not decided.** The assistant asked whether it should be included in the MVP, deferred, or include automatic escalation after a missed check-in. No user answer has been recorded yet. Do not assume a choice.

## Safety and reliability constraints
- Ask permission before accessing location and explain when location is shared.
- Do not claim continuous location updates when permissions, GPS, network or OS behavior prevent them.
- Do not claim SOS notifications were delivered without a confirmed provider response.
- Emergency-service integration is out of scope unless separately researched, authorized and tested.
- A PIN helps prevent accidental termination but is not a substitute for a carefully designed threat model.
- Document offline and service-failure behavior before implementation.

## Workflow rule
Do not start application coding until MVP requirements are clarified and the plan/backlog have been reviewed.