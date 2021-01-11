import import_declare_test

import os
import sys
import time
import datetime

import modinput_wrapper.base_modinput
from solnlib.packages.splunklib import modularinput as smi



import input_module_sfdc_event_log as input_module


'''
    Do not edit this file!!!
    This file is generated by Add-on builder automatically.
    Add your modular input logic to file input_module_sfdc_event_log.py
'''
class ModInputsfdc_event_log(modinput_wrapper.base_modinput.BaseModInput):

    def __init__(self):
        if 'use_single_instance_mode' in dir(input_module):
            use_single_instance = input_module.use_single_instance_mode()
        else:
            use_single_instance = False
        super(ModInputsfdc_event_log, self).__init__("splunk_ta_salesforce", "sfdc_event_log", use_single_instance)
        self.global_checkbox_fields = None

    def get_scheme(self):
        """overloaded splunklib modularinput method"""
        scheme = super(ModInputsfdc_event_log, self).get_scheme()
        scheme.title = ("Salesforce Event Log")
        scheme.description = ("")
        scheme.use_external_validation = True
        scheme.streaming_mode_xml = True

        scheme.add_argument(smi.Argument("name", title="Name",
                                         description="",
                                         required_on_create=True))

        """
        For customized inputs, hard code the arguments here to hide argument detail from users.
        For other input types, arguments should be get from input_module. Defining new input types could be easier.
        """
        scheme.add_argument(smi.Argument("account", title="Salesforce Account",
                                         description="",
                                         required_on_create=True,
                                         required_on_edit=False))
        scheme.add_argument(smi.Argument("start_date", title="Query Start Date",
                                         description="The datetime from which to query and index records, in this format: \"YYYY-MM-DDThh:mm:ss.000z\".Defaults to 30 days earlier from now.",
                                         required_on_create=False,
                                         required_on_edit=False)),
        scheme.add_argument(smi.Argument("token", title="token",
                                         description="Deprected fields",
                                         required_on_create=False,
                                         required_on_edit=False)),
        scheme.add_argument(smi.Argument("endpoint", title="endpoint",
                                         description="Deprected fields",
                                         required_on_create=False,
                                         required_on_edit=False)),
        scheme.add_argument(smi.Argument("monitoring_interval", title="monitoring_interval",
                                         description="monitoring interval field",
                                         required_on_create=False,
                                         required_on_edit=False))
        return scheme

    def get_app_name(self):
        return "Splunk_TA_salesforce"

    def validate_input(self, definition):
        """validate the input stanza"""
        input_module.validate_input(self, definition)

    def collect_events(self, ew):
        """write out the events"""
        input_module.collect_events(self, ew)

    def get_account_fields(self):
        account_fields = []
        account_fields.append("account")
        return account_fields

    def get_checkbox_fields(self):
        checkbox_fields = []
        return checkbox_fields

    def get_global_checkbox_fields(self):
        if self.global_checkbox_fields is None:
            checkbox_fields = []
            customized_settings = {u'uuid': u'4dbf283cc20544ae95358d9785959239', u'data_inputs_options': [{u'type': u'customized_var', u'title': u'Salesforce Account', u'description': u'', u'required_on_create': True, u'required_on_edit': False, u'name': u'account', u'default_value': u'', u'possible_values': [], u'format_type': u'global_account', u'placeholder': u''}, {u'type': u'customized_var', u'title': u'Salesforce Environment', u'description': u'', u'required_on_create': True, u'required_on_edit': False, u'name': u'endpoint', u'default_value': u'', u'possible_values': [{u'value': u'login.salesforce.com', u'label': u'Production'}, {u'value': u'test.salesforce.com', u'label': u'Sandbox'}], u'format_type': u'dropdownlist', u'placeholder': u''}, {u'type': u'customized_var', u'title': u'Security Token', u'description': u'Enter the Salesforce security token.', u'required_on_create': False, u'required_on_edit': False, u'name': u'token', u'default_value': u'', u'format_type': u'password', u'placeholder': u''}, {u'type': u'customized_var', u'title': u'Query Start Date', u'description': u'The datetime from which to query and index records, in this format: "YYYY-MM-DDThh:mm:ss.000z".\nDefaults to 30 days earlier from now.', u'required_on_create': False, u'required_on_edit': False, u'name': u'start_date', u'default_value': u'', u'format_type': u'text', u'placeholder': u''}], u'description': u'', u'code': u'# encoding = utf-8\nimport splunk_ta_salesforce_declare\n\nimport logging\n\nimport sfdc_common as common\nfrom cloudconnectlib.core.task import CCESplitTask, CCEHTTPRequestTask\nfrom splunktaucclib.rest_handler import util\n\nutil.remove_http_proxy_env_vars()\n\n_DEFAULT_START_DATE = 30\n_DEFAULT_LIMIT = 1000\n\n\ndef validate_input(helper, definition):\n    pass\n\n\ndef _index_event_log_file(task_config, meta_config):\n    header = {\n        \'Authorization\': \'Bearer {{session_id}}\',\n        \'Accept-encoding\': \'gzip\',\n        \'X-PrettyPrint\': \'1\'\n    }\n    request = {\n        \'url\': \'{{server_url}}/services/data/{{API_VERSION}}/sobjects\'\n               \'/EventLogFile/{{event_log_file.Id}}/LogFile\',\n        \'method\': \'GET\',\n        \'headers\': header,\n    }\n    task = CCEHTTPRequestTask(request, \'EventLogFile\', meta_config, task_config)\n    task.set_iteration_count(1)\n    task.configure_checkpoint(\n        name=\'{{event_log_file.Id}}\',\n        content={\n            \'finished\': True\n        }\n    )\n    process_params = (\n        (\'set_var\', [\'sfdc_event_log://EventLog\'], \'source\'),\n        (\'read_event_log_file\', [\'{{__response__.body}}\', \'{{event_log_file}}\'], \'records\'),\n        (\'splunk_xml\', [\'{{records}}\', \'\', \'{{index}}\', \'{{host}}\', \'{{source}}\', \'{{sourcetype}}\'], \'events\'),\n        (\'std_output\', [\'{{events}}\'], \'\'),\n        (\'log\', [logging.INFO, \'{{records|count}} events collected\'], \'\'),\n    )\n    task.add_postprocess_handler_batch(process_params)\n    return task\n\n\ndef _build_query(task_config, logger):\n    """Filter event log by Interval to avoid duplication"""\n    interval = (task_config.get(\'monitoring_interval\') or \'\').strip()\n    terms = [\'SELECT Id,EventType,LogDate FROM EventLogFile WHERE\'\n             \' LogDate{{">" if is_greater_than.lower()=="true" else "="}}{{start_date}}\']\n    lv = interval.lower()\n\n    if lv in (\'daily\', \'hourly\'):\n        logger.info("Add-on will only collect event logs which interval is \'%s\'", interval)\n        terms.append("AND Interval=\'%s\'" % lv.capitalize())\n    else:\n        logger.info("Event monitoring interval=\'%s\', Add-on will not filter"\n                    " event logs with interval.", interval)\n    terms.append(\'ORDER BY LogDate LIMIT {{limit}}\')\n    return \' \'.join(terms)\n\n\ndef add_process_pipeline(task, task_config, logger):\n    soql = _build_query(task_config, logger)\n\n    pre_params = (\n        (\'exit_job_if_true\', [\'{{records_empty}}\'], \'\'),\n        (\'exit_if_true\', [\'{{records_not_empty}}\'], \'\'),\n\n        # Reset checkpoint, records is loaded from checkpoint\n        (\'refresh_checkpoint\', [\'{{name}}\', \'{{records}}\', task._checkpointer], \'records\'),\n        # Consume the records left in checkpoint\n        (\'exit_if_true\', [\'{{records|count>0}}\'], \'\'),\n\n        # Prepare query\n        (\'set_var\', [soql], \'query\'),\n        (\'log\', [logging.INFO, \'Query event logs soql={{query}}\'], \'\'),\n        (\'quote\', [\'{{query}}\'], \'query_string\')\n    )\n    task.add_preprocess_handler_batch(pre_params)\n    post_params = (\n        (\'json_path\', [\'{{__response__.body}}\', \'records\'], \'records\'),\n        (\'log\', [logging.INFO, \'{{records|count}} records found in response.\'], \'\'),\n        (\'set_var\', [\'{{records|count==0}}\'], \'result_empty\'),\n        (\'exclude_fields\', [\'{{records}}\'], \'records\'),\n\n        (\'json_path\', [\'{{records}}\', \'[-1].LogDate\'], \'new_start_date\'),\n\n        (\n            \'extract_ids_if_equal\',\n            [\'{{is_greater_than}}\', \'{{records}}\', \'{{records_on_start_date}}\'],\n            \'record_ids\'\n        ),\n\n        # For query > start_date, we cannot index all event log files in response.\n        (\n            \'filter_event_log_records\',\n            [\'{{is_greater_than}}\', \'{{records}}\', \'{{new_start_date}}\', \'{{records_on_start_date}}\'],\n            \'records\'\n        ),\n        (\'log\', [logging.INFO, \'Got {{records|count}} records after filtered.\'], \'\'),\n\n        (\'set_var\', [\'{{record_ids}}\'], \'records_on_start_date\'),\n\n        (\n            \'decide_next_start_date\',\n            [\'{{is_greater_than}}\', \'{{previous_empty}}\', \'{{start_date}}\', \'{{next_start_date}}\'],\n            \'start_date\'\n        ),\n        # Swap ">" --> "=" or "=" --> ">"\n        (\'set_var\', [\'{{false if is_greater_than.lower() == "true" else true}}\'], \'is_greater_than\'),\n\n        (\'set_var\', [\'{{new_start_date}}\'], \'next_start_date\'),\n\n        (\'set_var\', [\'{{result_empty}}\'], \'previous_empty\'),\n        (\'set_var\', [\'{{records|count>0}}\'], \'records_not_empty\'),\n        (\'set_var\', [\'{{records|count==0}}\'], \'records_empty\'),\n    )\n    task.add_postprocess_handler_batch(post_params)\n\n\ndef _list_event_log(task_config, meta_config, logger):\n    task = common.get_sfdc_task_template(\'EventLog\', task_config, meta_config)\n    task.set_iteration_count(2)\n    task.configure_checkpoint(\n        name=\'{{name}}\',\n        content={\n            \'start_date\': \'{{start_date}}\',\n            \'previous_empty\': \'{{previous_empty}}\',\n            \'next_start_date\': \'{{next_start_date}}\',\n            \'is_greater_than\': \'{{is_greater_than}}\',\n            \'records\': \'{{records}}\',\n            \'records_on_start_date\': \'{{records_on_start_date}}\',\n        }\n    )\n    common.check_login_result(task)\n    add_process_pipeline(task, task_config, logger)\n    return task\n\n\ndef _split_records_to_file():\n    """Split the EventLog file records to file downloading tasks"""\n    task = CCESplitTask(name=\'EventLogRecordsToFiles\')\n    task.configure_split(\n        method=\'split_by\',\n        source=\'{{records}}\',\n        output=\'event_log_file\'\n    )\n    return task\n\n\ndef collect_events(helper, ew):\n    """Collect events"""\n    stanza_name = helper.get_input_stanza_names()\n    logger = common.setup_logger(stanza_name, helper.get_log_level())\n    logger.info(\'Collecting events started.\')\n\n    task_config = helper.get_input_stanza(stanza_name)\n    if not task_config.get(\'account\'):\n        logger.warning(\'Salesforce account is not configured fully. Add-on is going to exit.\')\n        return\n\n    meta_config = helper._input_definition.metadata\n    meta_config[\'checkpoint_dir\'] = common.reset_checkpoint_dir(\n        meta_config[\'checkpoint_dir\'], task_config[\'name\'], logger\n    )\n    start_date = common.fix_start_date(\n        task_config.get(\'start_date\'), _DEFAULT_START_DATE, logger\n    )\n    task_config.update({\n        \'appname\': helper.get_app_name(),\n        \'stanza_name\': stanza_name,\n        \'limit\': _DEFAULT_LIMIT,\n        \'API_VERSION\': common.SFDC_API_VERSION,\n        \'start_date\': start_date,\n        \'is_greater_than\': \'true\',\n    })\n    tasks = (\n        common.login_sfdc(),\n        _list_event_log(task_config, meta_config, logger),\n        _split_records_to_file(),\n        _index_event_log_file(task_config, meta_config)\n    )\n    common.run_tasks(tasks, ctx=task_config, proxy=helper.proxy)\n\n    logger.info(\'Collecting events finished.\')\n', u'name': u'sfdc_event_log', 'interval': u'3600', 'index': u'default', u'type': u'customized', 'streaming_mode_xml': True, 'use_external_validation': True, u'sample_count': 0, u'is_loaded': False, u'parameters': [{u'type': u'global_account', u'label': u'Salesforce Account', u'help_string': u'', u'value': u'', u'name': u'account', u'default_value': u'', u'possible_values': [], u'format_type': u'global_account', u'placeholder': u'', u'required': True}, {u'type': u'dropdownlist', u'label': u'Salesforce Environment', u'help_string': u'', u'value': u'', u'name': u'endpoint', u'default_value': u'', u'possible_values': [{u'value': u'login.salesforce.com', u'label': u'Production'}, {u'value': u'test.salesforce.com', u'label': u'Sandbox'}], u'format_type': u'dropdownlist', u'placeholder': u'', u'required': True}, {u'type': u'password', u'label': u'Security Token', u'help_string': u'Enter the Salesforce security token.', u'value': u'', u'name': u'token', u'default_value': u'', u'format_type': u'password', u'placeholder': u'', u'required': False}, {u'type': u'text', u'label': u'Query Start Date', u'help_string': u'The datetime from which to query and index records, in this format: "YYYY-MM-DDThh:mm:ss.000z".\nDefaults to 30 days earlier from now.', u'value': u'', u'name': u'start_date', u'default_value': u'', u'format_type': u'text', u'placeholder': u'', u'required': False}], u'customized_options': [{u'value': u'', u'name': u'account'}, {u'value': u'', u'name': u'endpoint'}, {u'value': u'', u'name': u'token'}, {u'value': u'', u'name': u'start_date'}], 'sourcetype': u'sfdc:logfile', u'title': u'Salesforce Event Log'}.get('global_settings', {}).get('customized_settings', [])
            for global_var in customized_settings:
                if global_var.get('type', '') == 'checkbox':
                    checkbox_fields.append(global_var['name'])
            self.global_checkbox_fields = checkbox_fields
        return self.global_checkbox_fields

if __name__ == "__main__":
    exitcode = ModInputsfdc_event_log().run(sys.argv)
    sys.exit(exitcode)