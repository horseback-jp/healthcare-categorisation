# Build Checklist — Evergreen Healthcare Intelligent Routing Agent

- [x] 1. Initialize project configuration (`gecx-config.json`, `.active-project`)
- [x] 2. Create app configuration (`cxas_app/evergreen_voice_assistant/app.json`) with variables and Zephyr voice
- [x] 3. Create agent configuration and XML instructions (`evergreen_voice_assistant`)
- [x] 4. Create `set_session_state` tool
- [x] 5. Create `transfer_call` tool
- [x] 6. Create `medical_entity_lookup` tool
- [x] 7. Create `before_model` callback (silence handling + transfer interception)
- [x] 8. Create `after_model` callback (farewell prepending)
- [x] 9. Create golden evaluation YAMLs
- [x] 10. Create simulation evaluation YAML
- [x] 11. Create tool tests and callback tests
- [x] 12. Configure GitHub Actions workflow (`.github/workflows/deploy.yml`)
- [x] 13. Verify with `cxas lint` and commit/push to GitHub
