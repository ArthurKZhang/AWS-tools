import boto3

ec2res = boto3.resource('ec2')
ec2client = boto3.client('ec2')
ssmClient = boto3.client('ssm')


# input the ImageId here
imageId = ''
# input the number of instances you wnat to launch here
Number =
# ...
InstanceType = 'c5d.large'
KeyName = 'standard'
# Needs AmazonSSMFullAccess policy
IamInstanceProfile = {'Arn': 'arn:aws-cn:iam::***:instance-profile/*****',
                      }

newInstances = ec2res.create_instances(ImageId=imageId,
                                       InstanceType=InstanceType,
                                       KeyName=KeyName,
                                       MaxCount=Number,
                                       MinCount=Number,
                                       IamInstanceProfile=IamInstanceProfile)
newInstancesIds = []
for inst in newInstances:
    newInstancesIds.append(inst.instance_id)
    print('Created InstanceId: ' + inst.instance_id)
print(newInstancesIds)
