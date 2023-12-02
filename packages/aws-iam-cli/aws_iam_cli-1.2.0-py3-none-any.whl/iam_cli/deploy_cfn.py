import boto3
from datetime import datetime
from dateutil import tz
from inquirer import prompt, Confirm, Text
from prettytable import PrettyTable
from cfn_visualizer import visualizer

from iam_cli.validators import stack_name_validator
from iam_cli.tools import bright_red, bright_green


class DeployCfn:
    client = None
    deploy = False
    name = ''
    profile = 'default'

    def __init__(self):
        self.project = 'IAM'
        self.region = 'ap-northeast-2'
        profile='default'
        self.ask_deployment()
        self.input_stack_name()
        self.deployment(self.project, self.name, self.region, profile)


    def ask_deployment(self):
        questions = [
            Confirm(
                name='required',
                message='CloudFormation에 바로 배포하길 원하신가요?',
                default=True
            )
        ]

        self.deploy = prompt(questions=questions, raise_keyboard_interrupt=True)['required']
    
    def input_stack_name(self):
        questions = [
            Text(
                name='name',
                message='CloudFormation 스택 이름을 지정해주세요',
                validate=lambda _, x: stack_name_validator(x, self.region, self.profile)
            )
        ]

        self.name = prompt(questions=questions, raise_keyboard_interrupt=True)['name']
    
    def deployment(self, project, name, region, profile='default'):
        if self.deploy:  # deploy using cloudformation
            self.client = boto3.session.Session(profile_name=profile, region_name=region).client('cloudformation')
            response = self.client.create_stack(
                StackName=name,
                TemplateBody=self.get_template(),
                TimeoutInMinutes=15,
                Tags=[{'Key': 'Name', 'Value': name}, {'Key': 'project', 'Value': project}],
                Capabilities=['CAPABILITY_NAMED_IAM'],
            )
            stack_id = response['StackId']

            while True:
                # 1. get stack status
                response = self.client.describe_stacks(
                    StackName=name
                )
                stack_status = response['Stacks'][0]['StackStatus']

                if stack_status in ['CREATE_FAILED', 'ROLLBACK_FAILED',
                                    'ROLLBACK_COMPLETE']:  # create failed
                    print()
                    print(f'{bright_red("Failed!")}')
                    print()
                    print(f'{bright_red("해당 에러 로그를 아래 URL로 접속하여 확인하세요")}')
                    print()
                    print(
                        f'{bright_red(f"https://{region}.console.aws.amazon.com/cloudformation/home?region={region}#/stacks/stackinfo?stackId={stack_id}")}')

                    break

                elif stack_status == 'CREATE_COMPLETE':  # create complete successful
                    print()
                    self.print_table()
                    print(f'{bright_green("Success!")}')

                    break

                else:
                    visualizer(client=self.client, stack_name=self.name)

        else:
            print('끝났습니다!\n\n')
            print('해당 AWS CLI를 사용해서 IAM User를 배포할 수 있습니다!\n\n\n')
            print(
                'aws cloudformation deploy --stack-name {} --region {} --template-file ./iam_users.yaml'.format(
                    name, region))
            
    def get_template(self):
        with open('iam_users.yaml', 'r') as f:
            # content = yaml.full_load(f)
            content = f.read()

        # content = json.dumps(content)

        return content

    def get_timestamp(self, timestamp: datetime):
        return timestamp.replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal()).strftime('%I:%M:%S %p')

    def get_color(self, status: str):
        if 'ROLLBACK' in status or 'FAILED' in status:
            return '91m'

        elif 'PROGRESS' in status:
            return '96m'

        elif 'COMPLETE' in status:
            return '92m'

    def print_table(self):
        table = PrettyTable()
        table.set_style(15)
        table.field_names = ['Logical ID', 'Physical ID', 'Type']
        table.vrules = 0
        table.hrules = 1
        table.align = 'l'
        rows = []

        response = self.client.describe_stack_resources(StackName=self.name)['StackResources']

        for resource in response:
            rows.append([resource['LogicalResourceId'], resource['PhysicalResourceId'], resource['ResourceType']])

        rows = sorted(rows, key=lambda x: (x[2], x[0]))
        table.add_rows(rows)
        print(table)