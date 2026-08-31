from workers.worker_classes.chat_workers.ChatWorkerModule import ChatWorker
from workers.utils.task_definitions import *
import streamlit as st


class FieldInputer(ChatWorker):
    def __init__(self):
        super().__init__()

    def work(self, task_instance):

        validators = {}
        for _, value in type(task_instance).__pydantic_decorators__.field_validators.items():
            for field_name in value.info.fields:
                validators[field_name] = value.func

        empty_fields = self._find_empty_fields(task_instance)

        field_values = {}
        for name, properties in empty_fields.items():
            curr_field_value = st.text_input(name, help=properties['description'])
            if name in validators:
                try:
                    validators[name](curr_field_value)
                    field_values[name] = curr_field_value
                except Exception as e:
                    st.error(e)
                    field_values[name] = ""
            else:
                field_values[name] = curr_field_value
        return field_values


    def _find_empty_fields(self, task_instance):

        empty_fields = {}
        properties_dict = task_instance.model_json_schema()["properties"]
        for name, properties in properties_dict.items():
            if properties["default"] is None:
                empty_fields[name] = properties
        
        return empty_fields
