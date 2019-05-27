import boto3
import re

ec2res = boto3.resource('ec2')
ec2client = boto3.client('ec2')
ssmClient = boto3.client('ssm')

#your inputs
newInstancesIds = ['***']

sendCommandResponse = ssmClient.send_command(
    InstanceIds=newInstancesIds,
    DocumentName='AWS-RunShellScript',
    Parameters={'commands': [
        "fio --numjobs=1 --iodepth=128 --direct=1 --ioengine=libaio --sync=1 --rw=randwrite --bs=1M --size=1G --time_based --runtime=60 --name=Fio --directory=/mnt/nfs-disk"]},
)

# FOR RANDOM READ AND WRITE "fio --directory=/mnt/nfs-disk --direct=1 --rw=randrw --refill_buffers --norandommap --randrepeat=0 --ioengine=libaio --bs=4k --size=2G --rwmixread=70 --iodepth=32 --numjobs=16 --runtime=60 --group_reporting --name=4k_mixed"
# FOR RANDOM READ ONLY "fio -numjobs=1 -iodepth=128 -direct=1 -ioengine=libaio -sync=1 -rw=randread -bs=1M -size=1G -time_based -runtime=60 -name=Fio --directory=/mnt/nfs-disk"
# FOR RANDOM WRITE ONLY "fio -numjobs=1 -iodepth=128 -direct=1 -ioengine=libaio -sync=1 -rw=randwrite -bs=1M -size=1G -time_based -runtime=60 -name=Fio --directory=/mnt/nfs-disk"

commandId = sendCommandResponse.get('Command').get('CommandId')
print('commandId' + commandId)
for instId in newInstancesIds:
    # print('InstanceId: ' + instId)
    respSingleInst = ssmClient.list_command_invocations(
        CommandId=commandId,
        InstanceId=instId,
        Details=True
    )
    # print(respSingleInst)
    i = 0
    # stupid wait for command executing complete
    while len(respSingleInst.get('CommandInvocations')) == 0 or respSingleInst.get('CommandInvocations')[0].get(
            'Status') != 'Success':
        if (i % 6000 == 0):
            print(".", end=" ")
            respSingleInst = ssmClient.list_command_invocations(
                CommandId=commandId,
                InstanceId=instId,
                Details=True
            )
        i = i + 1
    result_log = respSingleInst.get('CommandInvocations')[0].get('CommandPlugins')[0].get('Output')
    #get the target number we need
    wbw = re.findall(r"bw=(.+?),", result_log)
    print('')
    print(wbw[0])

#Stop the new instances for saving cost
response = ec2client.stop_instances(
    InstanceIds=newInstancesIds,
    Force=True
)
