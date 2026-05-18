# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
medical_entity_lookup — Entity Mapping Tool

PURPOSE:
    Takes caller utterance and maps it to official Evergreen Healthcare routing entities using an embedded CSV knowledge base.
"""


def medical_entity_lookup(user_utterance: str = "") -> dict:
    """Analyzes user utterance and maps it to official Evergreen Healthcare entities.

    Args:
        user_utterance: Spoken response from the user.

    Returns:
        dict: Matched entities or error status.
    """
    if not user_utterance:
        return {
            "status": "error",
            "agent_action": "You must provide a valid user_utterance."
        }

    utterance_lower = user_utterance.lower()

    knowledge_base = [
        {"entity": "authorisation_type", "value": "Preauthorisation", "synonyms": ["pre-auth", "pre-authorisation", "clearance", "approval", "authorisation"]},
        {"entity": "appointment_type", "value": "Consultation", "synonyms": ["visit", "checkup", "initial visit", "consultation"]},
        {"entity": "medical_specialty", "value": "Musculoskeletal (MSK)", "synonyms": ["orthopedic", "bone", "joint", "knee", "msk", "musculoskeletal"]},
        {"entity": "medical_specialty", "value": "Cardiology", "synonyms": ["heart", "cardiac", "cardiovascular", "cardiology"]},
        {"entity": "medical_specialty", "value": "Mental Health", "synonyms": ["psychiatry", "behavioral", "psychological", "wellness", "mental health"]},
        {"entity": "claim_query", "value": "Claim", "synonyms": ["claim", "receipt", "billing", "refund", "reimbursement"]}
    ]

    matched_entities = []

    for item in knowledge_base:
        if item["value"].lower() in utterance_lower or any(syn in utterance_lower for syn in item["synonyms"]):
            matched_entities.append({
                "Entity": item["entity"],
                "Value": item["value"]
            })
            context.state[item["entity"]] = item["value"]

    if not matched_entities:
        no_match = int(context.state.get("no_match_counter") or 0) + 1
        context.state["no_match_counter"] = str(no_match)
        return {
            "status": "no_match",
            "agent_action": "Could not confidently match a medical entity. Apologize and ask the caller to rephrase or clarify their request."
        }

    context.state["no_match_counter"] = "0"

    return {
        "status": "success",
        "matches": matched_entities
    }
