import json

from fastapi.datastructures import Headers

from src.api.planning.data.birthday.step_auto_done import auto_done_json
from src.api.planning.data.birthday.step_party_manual import party_manual_json, party_manual_reload_json
from src.api.planning.model.planning_flow_type import PlanningTypeEnum
from src.api.planning.model.planning_interaction import PlanningInteraction
from src.store.birthday.party_preferences_store import party_preferences_store


def parse_plan_flow_name_from_headers(headers: Headers) -> PlanningTypeEnum:
    """
    从请求头中解析 plan_flow_name 字段

    参数:
        headers: fastapi.Request.headers

    返回:
        PlanningTypeEnum
    """

    plan_flow_name = headers.get("plan-flow-name", "")
    planFlow = PlanningTypeEnum.from_string(plan_flow_name)
    return planFlow


def response_by_interactions(
    interactions: list[PlanningInteraction], planFlow: PlanningTypeEnum, session_id: str = ""
) -> tuple[str, str]:
    default_step = "step_1.json"
    if planFlow == PlanningTypeEnum.aTob:
        path_prefix = "atob/"
    elif planFlow == PlanningTypeEnum.birthday:
        path_prefix = "birthday/"
    else:
        path_prefix = ""
        default_step = "empty.json"

    default = f"{path_prefix}{default_step}"

    if len(interactions) == 0:
        return default, ""
    else:
        interaction = interactions[0]
        if planFlow == PlanningTypeEnum.aTob:
            if interaction.type == "onCalendar":
                return f"{path_prefix}step_2.json", ""
            elif interaction.type == "onAccessPermissionReject":
                return f"{path_prefix}step_1.json", ""
            elif interaction.type == "onAccessPermissionConfirm":
                return f"{path_prefix}step_3.json", ""
            elif interaction.type == "onViewRoute":
                return f"{path_prefix}step_4.json", ""
            elif interaction.type == "onTapPhoneNotification":
                return f"{path_prefix}step_5.json", ""
            elif interaction.type == "onNotificationConfirm":
                return f"{path_prefix}step_6.json", ""
            elif interaction.type == "onNotificationCancel":
                return f"{path_prefix}step_3.json", ""
            else:
                return default, ""
        elif planFlow == PlanningTypeEnum.birthday:
            if interaction.type == "onGoalConfirm":
                return f"{path_prefix}step_2.json", ""
            elif interaction.type == "onAccessPermissionConfirm":
                return f"{path_prefix}step_3.json", ""
            elif interaction.type == "onAccessPermissionReject":
                return f"{path_prefix}step_1.json", ""
            elif interaction.type == "onContactConfirm":
                return f"{path_prefix}step_4.json", ""
            elif interaction.type == "onBirthdayAgentUpdatePartyStart":
                return f"{path_prefix}step_5.json", ""
            elif interaction.type == "onBirthdayAgentUpdatePartyAttendant":
                return f"{path_prefix}step_6.json", ""
            elif interaction.type == "onBirthdayAgentUpdatePartyAllergy":
                return f"{path_prefix}step_7.json", ""
            elif interaction.type == "onBirthdayAgentUpdatePartyGroceryList":
                return f"{path_prefix}step_8.json", ""
            elif interaction.type == "onBirthdayPlanningDone":
                return f"{path_prefix}step_agent_done.json", ""
            elif interaction.type == "onChooseMealConfirm":
                return f"{path_prefix}step_choose_meal.json", ""
            elif interaction.type == "onBirthdayPlanningReload":
                return handle_on_birthday_planning_reload(interaction, session_id)
            elif interaction.type in ["onGoalCancel", "onPartyStartSave", "onPartyAttendantSave", "onPartyAllergySave"]:
                return "", create_response_data(interaction, session_id)
            else:
                return default, ""
        else:
            return default, ""


def get_next_interaction_type(interaction: PlanningInteraction) -> str:
    if interaction.type == "onContactConfirm":
        return "onBirthdayAgentUpdatePartyStart"
    elif interaction.type == "onBirthdayAgentUpdatePartyStart":
        return "onBirthdayAgentUpdatePartyAttendant"
    elif interaction.type == "onBirthdayAgentUpdatePartyAttendant":
        return "onBirthdayAgentUpdatePartyAllergy"
    elif interaction.type == "onBirthdayAgentUpdatePartyAllergy":
        return "onBirthdayAgentUpdatePartyGroceryList"
    else:
        return ""


def create_response_data(interaction: PlanningInteraction, session_id: str = "") -> str:
    origin_data_str = json.dumps(party_manual_json)

    current_preferences = party_preferences_store.get_party_preferences(session_id)

    if interaction.type == "onGoalCancel":
        # 清空所有偏好数据
        party_preferences_store.clear_session(session_id)
        return (
            origin_data_str.replace("{{party_start}}", "")
            .replace("{{party_attendant}}", "")
            .replace("{{party_allergy}}", "")
            .replace("{{grocery_list}}", "")
            .replace("{{party_start_state}}", "active")
            .replace("{{party_attendant_state}}", "inactive")
            .replace("{{party_allergy_state}}", "inactive")
            .replace("{{grocery_list_state}}", "inactive")
        )
    elif interaction.type == "onPartyStartSave":
        # 保存开始时间偏好
        start_time = interaction.value or ""
        party_preferences_store.set_party_start_time(session_id, start_time)
        return (
            origin_data_str.replace("{{party_start}}", start_time)
            .replace("{{party_attendant}}", current_preferences.party_attendant)
            .replace("{{party_allergy}}", current_preferences.party_allergy)
            .replace("{{grocery_list}}", "")
            .replace("{{party_start_state}}", "inactive")
            .replace("{{party_attendant_state}}", "active")
            .replace("{{party_allergy_state}}", "inactive")
            .replace("{{grocery_list_state}}", "inactive")
        )
    elif interaction.type == "onPartyAttendantSave":
        # 保存出席人员偏好
        attendant = interaction.value or ""
        party_preferences_store.set_party_attendant(session_id, attendant)
        return (
            origin_data_str.replace("{{party_start}}", current_preferences.party_start)
            .replace("{{party_attendant}}", attendant)
            .replace("{{party_allergy}}", current_preferences.party_allergy)
            .replace("{{grocery_list}}", "")
            .replace("{{party_start_state}}", "inactive")
            .replace("{{party_attendant_state}}", "inactive")
            .replace("{{party_allergy_state}}", "active")
            .replace("{{grocery_list_state}}", "inactive")
        )
    elif interaction.type == "onPartyAllergySave":
        # 保存忌口信息偏好
        allergy = interaction.value or ""
        party_preferences_store.set_party_allergy(session_id, allergy)
        return (
            origin_data_str.replace("{{party_start}}", current_preferences.party_start)
            .replace("{{party_attendant}}", current_preferences.party_attendant)
            .replace("{{party_allergy}}", allergy)
            .replace("{{grocery_list}}", "Genterated")
            .replace("{{party_start_state}}", "inactive")
            .replace("{{party_attendant_state}}", "inactive")
            .replace("{{party_allergy_state}}", "inactive")
            .replace("{{grocery_list_state}}", "active")
        )
    elif interaction.type == "onBirthdayPlanningReload":
        origin_data_reload_str = json.dumps(party_manual_reload_json)
        return (
            origin_data_reload_str.replace("{{party_start}}", current_preferences.party_start)
            .replace("{{party_attendant}}", current_preferences.party_attendant)
            .replace("{{party_allergy}}", current_preferences.party_allergy)
        )
    else:
        return ""


def handle_on_birthday_planning_reload(interaction: PlanningInteraction, session_id: str = "") -> tuple[str, str]:
    if not party_preferences_store.has_preferences(session_id):
        return "birthday/step_9.json", ""
    else:
        origin_data_str = json.dumps(auto_done_json)
        return "", origin_data_str.replace("{{meal}}", party_preferences_store.get_party_meal(session_id))
