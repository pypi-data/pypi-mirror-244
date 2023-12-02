import boto3
import csv
import glob
from botocore.config import Config
from inquirer import List, prompt, Confirm, Text
from datetime import datetime

from iam_cli.tools import print_figlet
from iam_cli.create_yaml import CreateYAML
from iam_cli.deploy_cfn import DeployCfn
from iam_cli.validators import stack_name_validator


class Command:
    ban = None
    role = None
    num = None
    num_name = None
    created_date = None
    name = None

    csv_files_list = []
    choose_csv_file = None
    student_info = {}
    student_list = []
    teacher_info = {}
    teacher_list = []
    now = datetime.now()

    def __init__(self):
        print_figlet()
        self.get_csv_files()
        self.choose_csv_files()
        self.process_csv()

        yaml_file = CreateYAML(student_list=self.student_list, teacher_list=self.teacher_list)
        yaml_file.create_yaml()
        DeployCfn()

    def get_csv_files(self):
        csv_files = glob.glob('*.csv')

        # 파일 이름 출력
        for file_name in csv_files:
            self.csv_files_list.append(file_name)

    def choose_csv_files(self):
        questions = [
            List(
                name='csv_files',
                message='csv 파일을 선택하세요' ,
                choices=self.csv_files_list
            )
        ]

        answer = prompt(questions=questions, raise_keyboard_interrupt=True)
        self.choose_csv_file = answer.get('csv_files')

    def process_csv(self):
        # CSV 파일을 읽어 들임
        with open(self.choose_csv_file, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)

            if self.choose_csv_file.startswith('student'):
                self.role = 'student'

                for row in reader:
                    self.ban = row['학번'][2]
                    self.num = str(row['학번'])
                    self.num_name = str(row['학번']) + str(row['이름'])
                    self.created_date = self.now.strftime("%Y-%m-%d")

                    self.student_info = {
                        'ban': self.ban,
                        'role': self.role,
                        'num': self.num,
                        'num_name': self.num_name,
                        'created_date': self.created_date
                    }

                    self.student_list.append(self.student_info)
            elif self.choose_csv_file.startswith('teacher'):
                self.role = 'teacher'

                for row in reader:
                    self.name = row['이름']
                    self.created_date = self.now.strftime("%Y-%m-%d")

                    self.teacher_info = {
                        'name': self.name,
                        'role': self.role,
                        'created_date': self.created_date
                    }

                    self.teacher_list.append(self.teacher_info)

    def create_stack(self):
        questions = [
            Confirm(
                name='deploy',
                message='Do you want to deploy stack in \033[1m\033[96m{}\033[0mtest?'.format(self.region),
                default=True
            )
        ]

        answer = prompt(questions, raise_keyboard_interrupt=True)

        if answer['deploy']:
            questions = [
                Text(
                    name='stack-name',
                    message='Type your stack name',
                    validate=lambda _, x: stack_name_validator(x, self.region)
                )
            ]

            answer = prompt(questions, raise_keyboard_interrupt=True)

            try:
                client = boto3.client('cloudformation', config=Config(region_name=self.region))

                response = client.create_stack(
                    StackName=answer['stack-name'],
                    TemplateBody='file://template.yaml'
                )
                stack_id = response['StackId']

            except Exception as e:
                print(e)