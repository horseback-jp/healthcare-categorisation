# Technical Design Document (TDD) — Bupa UK Intelligent Routing & Pre-Authorisation Agent

> This is a **living document** — update it whenever requirements, agent behavior, or evals change.

## Agent Design

### Architecture
- **Single Agent:** `bupa_voice_assistant`. Acts as the first point of contact for customers calling the Bupa support line.
- **Persona & Tone:** Friendly, professional, highly empathetic, and efficient Bupa Assistant representing a premium healthcare brand.
- **Scope:** Greeting, caller intent capture (pre-authorisation, consultation, claims), dynamic medical specialty prompting (when required for authorisations), entity resolution (mapping synonyms to official Bupa values), and deterministic telephony handoff with SIP UUI data.

### Tools
| Tool Name | Type | Purpose |
|-----------|------|---------|
| `medical_entity_lookup` | Python function | Takes caller utterance and maps it to official Bupa routing entities (`authorisation_type`, `appointment_type`, `medical_specialty`) using an embedded CSV knowledge base |
| `transfer_call` | Python function | Records transfer destination/queue and context in session state, setting internal trigger for deterministic handoff |
| `set_session_state` | Python function | Generic state management tool for internal flags and counters |

### Routing Logic
- **Phase 1: Greeting:** Welcome caller to Bupa UK, introduce as digital assistant, and ask how to help.
- **Phase 2: Intent Capture:** Listen to response and immediately invoke `medical_entity_lookup` to identify intent.
- **Phase 3: Authorisation Handling (Conditional):** If intent matches `authorisation_type` (e.g., Preauthorisation), verify if `medical_specialty` was also captured. If missing, prompt caller for condition/specialty and re-invoke `medical_entity_lookup`.
- **Phase 4: Telephony Handoff:** Once primary intent and required specialty are resolved, state a reassuring confirmation message and invoke `transfer_call` to trigger deterministic transfer to the specialist queue.
- **Phase 5: Fallback & Constraints:** Strictly no medical advice. If `medical_entity_lookup` fails to find a match after two attempts, apologize and invoke `transfer_call` with destination `triage` ("Unknown - Requires Triage").

### Variables
| Variable | Source | Notes |
|----------|--------|-------|
| `authorisation_type` | Tool output | String (e.g., 'Preauthorisation') |
| `appointment_type` | Tool output | String (e.g., 'Consultation') |
| `medical_specialty` | Tool output | String (e.g., 'Musculoskeletal (MSK)', 'Cardiology') |
| `caller_intent` | State variable | String |
| `_action_trigger` | Internal trigger | Set by tools/LLM to invoke deterministic transfer callbacks |
| `no_match_counter` | State variable | Counts consecutive failed entity lookup attempts |
| `no_input_counter` | State variable | Counts consecutive silence / no-input turns |

### Callbacks
| Callback | Agent | Purpose |
|----------|-------|---------|
| `before_model` | `bupa_voice_assistant` | Intercepts `_action_trigger` to execute deterministic transfer tool calls; handles silence retry logic |
| `after_model` | `bupa_voice_assistant` | Prepends professional goodbye / transfer confirmation before ending session |

---

## Eval Design

### Coverage Map
| Requirement | Eval Type | Rationale | Priority | Severity | Tags |
|-------------|-----------|-----------|----------|----------|------|
| Scenario 1: Knee Injury (Prompt Specialty) | Golden | Deterministic multi-turn extraction of authorisation and specialty | P0 | NO-GO | `authorisation, knee-injury, prompt-specialty` |
| Scenario 2: Cardiovascular (Upfront Info) | Golden | Deterministic single-turn extraction of authorisation and specialty | P0 | NO-GO | `authorisation, upfront-info, cardiology` |
| Scenario 3: General Claims Query | Golden | Deterministic routing without requiring medical specialty | P0 | NO-GO | `claims, no-specialty` |
| Guardrail & Vague Intent | Sim | Verifies clarification of vague symptoms without providing medical advice | P1 | HIGH | `guardrails, intent-capture` |

### Golden vs Sim Decision
- **Use goldens** for deterministic entity mapping, structured specialty prompting, and transfer trigger execution.
- **Use sims** for evaluating natural language clarification and verifying adherence to medical advice guardrails.

### Test Data (Customer Profiles)
| Profile | Scenario | Description |
|---------|----------|-------------|
| Arthur Pendelton | Scenario 1 | Calling for pre-authorisation for knee surgery (requires prompting for MSK) |
| Beatrice Vance | Scenario 2 | Calling for approval for cardiovascular tests (provides all info upfront) |
| Colin Creevey | Scenario 3 | Calling to check status of a dental claim receipt (no specialty required) |

---

## Build Steps

1. Create app configuration (`app.json`) with multilingual support (`en-GB` default) and Zephyr voice settings
2. Define variables in `app.json`
3. Create agent configuration and structured XML instructions (`bupa_voice_assistant`)
4. Create tools + tool configurations (`medical_entity_lookup`, `transfer_call`, `set_session_state`)
5. Implement deterministic callbacks (`before_model`, `after_model`)
6. Write golden YAML evaluation files (`scenario_1_knee_injury.yaml`, `scenario_2_cardiovascular.yaml`, `scenario_3_claims.yaml`)
7. Write simulation YAML entries
8. Write tool test YAML files
9. Write callback test files
10. Configure GitHub Actions CI/CD deployment workflow (`.github/workflows/deploy.yml`)
11. Run initial baseline evaluation suite

---

## Pass Rate History

| Date | Goldens | Sims | Tool Tests | Callback Tests | Notes |
|------|---------|------|------------|----------------|-------|
| 2026-05-15 | TBD | TBD | TBD | TBD | Initial baseline run pending |

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| 2026-05-15 | Initial TDD drafted | Antigravity |
