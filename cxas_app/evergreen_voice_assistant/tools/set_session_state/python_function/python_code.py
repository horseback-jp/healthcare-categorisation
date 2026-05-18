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
set_session_state — State-Setting Tool

PURPOSE:
    Writes internal trigger variables to session state. Used by the LLM to signal
    deterministic transfer or escalation actions to the before_model_callback.
"""


def set_session_state(_action_trigger: str = "") -> dict:
    """Write trigger variables to session state.

    Args:
        _action_trigger: Action to trigger (e.g., 'transfer_specialist', 'transfer_triage'). Read by before_model_callback.

    Returns:
        dict: Confirmation of which variables were set.
    """
    if not _action_trigger:
        return {
            "agent_action": "You must provide a valid _action_trigger to set_session_state."
        }

    context.state["_action_trigger"] = _action_trigger

    return {
        "status": "success",
        "updated_variables": {
            "_action_trigger": _action_trigger
        }
    }
