from workers.worker_classes.chat_workers.ChatWorkerModule import ChatWorker
from workers.utils.task_definitions import *
import streamlit as st


class FieldInputer(ChatWorker):
    def __init__(self):
        super().__init__()

    def work(self, task_instance):

        empty_fields = self._find_empty_fields(task_instance)

        field_values = {}
        for name, properties in empty_fields.items():
            field_values[name] = st.text_input(name, value="", help=properties['description'])

        return field_values


    def _find_empty_fields(self, task_instance):

        empty_fields = {}
        properties_dict = task_instance.model_json_schema()["properties"]
        for name, properties in properties_dict.items():
            if properties["default"] is None:
                empty_fields[name] = properties
        
        return empty_fields
