import requests
import json
import urllib.parse


def input_config(policy_id_list):
    """get config files for the policy

    Args:
        policy_name_list (_type_): a list of policy from the "stacking_order"

    Returns:
        _type_: dictionary with the key of policy name and the value of policy config
    """
    # get baseline policy parameter
    policy_configs = {}
    for item in policy_id_list[1:]:
        url = "http://wits.pwbm-api.net/policy_files/all_files_by_policy/" + str(item)
        response = requests.get(url).json()
        policy_configs[item] = convert_response_to_parameter(response)

    return policy_configs


def convert_response_to_parameter(json_response):
    policy_parameter = {}
    for item in json_response:
        policy_parameter[str(item["name"])] = json.loads(item["data"])

    return policy_parameter


def get_runtime(policy_id):
    """get runtime options from the policyrun id

    Args:
        policy_id (_type_): policyrun id

    Returns:
        _type_: json format of runtime options
    """
    url = "https://wits.pwbm-api.net/run_list/" + str(policy_id)
    return requests.get(url).json()


def save_output(policy_id, policy_name):
    """get runtime options from the policyrun id

    Args:
        policy_id . policy_name

    Returns:
        _type_: json format of runtime options
    """
    policy_name_url = urllib.parse.quote(policy_name)
    url = "https://wits.pwbm-api.net/run_list/output_details/?id={}&path={}".format(
        str(policy_id), policy_name_url
    )
    return requests.post(url).json()


