
from typing import List
from model.auth_data import DemographicsModel
import csv
from dynaconf import Dynaconf
import json
from pydantic import create_model


class SeedDataReader(object):

    def __init__(self, seeder_config: Dynaconf):
        self.file_path = seeder_config.input.file_path
        self.separator = seeder_config.input.separator
        self.no_json_fields = seeder_config.json.skip_fields.split(',')
        self.language = 'language'
        self.value = 'value'

    
    def read_and_parse_data(self) -> List:

        print ('Started Reading the input file.')
        data_list = []
        with open(self.file_path, 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter='|')
            for line in csv_reader:
                line['name'] = SeedDataReader._get_json_obj(line['name'])
                line['gender'] = SeedDataReader._get_json_obj(line['gender'])
                line['addressLine1'] = SeedDataReader._get_json_obj(line['addressLine1'])
                line['addressLine2'] = SeedDataReader._get_json_obj(line['addressLine2'])
                line['addressLine3'] = SeedDataReader._get_json_obj(line['addressLine3'])
                line['city'] = SeedDataReader._get_json_obj(line['city'])
                line['province'] = SeedDataReader._get_json_obj(line['province'])
                line['region'] = SeedDataReader._get_json_obj(line['region'])
                line['zone'] = SeedDataReader._get_json_obj(line['zone'])

                data_list.append(DemographicsModel(**line))

        print ('Completed reading data from input file. Total Number of rows found: ' + str(len(data_list)))
        return data_list

    def read_and_parse_dyn_data(self) -> List:

        print ('Started Reading the input file with dynamic fields.')
        record_data_list = {}
        with open(self.file_path, 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter='|')
            if not any(val in csv_reader.fieldnames for val in ['id', 'vid']):
                print ('Error: "id/vid" column is not available in input CSV.')
                raise ValueError('"id/vid" column is not available in input CSV')

            if self.language not in csv_reader.fieldnames:
                print ('Error: "language" column is not available in input CSV.')
                raise ValueError('"language" column is not available in input CSV')

            id_field_key = ''
            id_field_value = ''
            for line in csv_reader:
                field_names = csv_reader.fieldnames
                data_dict = {}
                id_field_key, id_field_value = self._get_id_key_value(line, field_names)
                found_data_dict = record_data_list.get(id_field_value, None)
                if found_data_dict:
                    print ('Found record in dictionary..')
                    self.add_other_language_data(field_names, line, found_data_dict)
                    continue
                for field_name in field_names:
                    if field_name == self.language:
                        continue
                    if field_name in self.no_json_fields:
                        data_dict[field_name] = line[field_name]
                        continue
                    
                    field_dict = {}
                    field_dict[self.language] = line[self.language]
                    field_dict[self.value] = line[field_name]

                    field_data_list = data_dict.get(field_name, None)
                    if field_data_list is None:
                        field_data_list = []

                    field_data_list.append(field_dict)
                    data_dict[field_name] = field_data_list

                DynamicDemoModel = create_model('DynamicDemoModel', **data_dict)
                record_data_list[id_field_value] = DynamicDemoModel

        print ('Completed reading data from input file. Total Number of rows found: ' + str(len(record_data_list)))
        return record_data_list.values(), id_field_key

    @staticmethod
    def _get_json_obj(field_value: str):
        if not field_value or len(field_value.strip()) == 0:
            return list()
        
        return json.loads(field_value)

    def _get_id_key_value(self, line: object, field_names: list):

        for field_name in field_names:
            if field_name in self.no_json_fields and field_name in ['id', 'vid']:
                return field_name, line[field_name]

    def add_other_language_data(self, field_names: list, line: object, found_data_dict: dict):
        for field_name in field_names:
            if field_name == self.language or field_name in self.no_json_fields:
                continue
            
            field_dict = {}
            field_dict[self.language] = line[self.language]
            field_dict[self.value] = line[field_name]

            field_data_list = found_data_dict.__fields__[field_name].default
            if field_data_list is None:
                field_data_list = []

            field_data_list.append(field_dict)