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
transfer_call — Transfer Tool

PURPOSE:
    Records transfer destination and summary in session state, setting _action_trigger
    to trigger deterministic handoff via before_model_callback.
"""


def transfer_call(transfer_destination: str = "", summary: str = "") -> dict:
    """Write transfer details to session state and set trigger.

    Args:
        transfer_destination: Destination queue (e.g., 'specialist', 'billing', 'triage').
        summary: Summary of captured details for UUI transfer.

    Returns:
        dict: Confirmation of transfer trigger.
    """
    if not transfer_destination:
        return {
            "agent_action": "You must provide a valid transfer_destination ('specialist', 'billing', or 'triage')."
        }

    context.state["_action_trigger"] = f"transfer_{transfer_destination}"
    if summary:
        context.state["summary"] = summary

    return {
        "status": "success",
        "transfer_destination": transfer_destination,
        "summary": summary
    }
