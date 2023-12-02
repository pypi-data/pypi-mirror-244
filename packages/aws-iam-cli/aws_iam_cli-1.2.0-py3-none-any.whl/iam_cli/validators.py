import boto3
from botocore.exceptions import ClientError, ProfileNotFound
from inquirer.errors import ValidationError

def stack_name_validator(text, region, profile='default'):
    if not len(text):
        return False

    else:
        try:
            boto3.session.Session(profile_name=profile, region_name=region).client('cloudformation') \
                .describe_stacks(StackName=text)

        except ProfileNotFound as e:
            raise ValidationError('', reason=e.__str__())

        except ClientError:  # stack doest
            return True

        except Exception as e:
            print(e)

            return False