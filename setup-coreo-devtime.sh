#!/bin/sh

# Default Parameters
TemplateUrl=https://s3.amazonaws.com/cloudcoreo-files/devtime/devtime_cfn.yml
Stack=cloudcoreo-events
Version=1
Regions=( eu-north-1 ap-south-1 eu-west-3 eu-west-2 eu-west-1 ap-northeast-2 ap-northeast-1 sa-east-1 ca-central-1 ap-southeast-1 ap-southeast-2 eu-central-1 us-east-1 us-east-2 us-west-1 us-west-2 )
CloudCoreoDevTimeQueueArn=arn:aws:sqs:us-west-2:910887748405:cloudcoreo-events-queue
CloudCoreoDevTimeTopicName=cloudcoreo-events
CloudCoreoDevTimeMonitorRule=cloudcoreo-events
Stack=cloudcoreo-events

aws_params=""
[ "$#" -ne 1 ] && aws_params="$@"

# Checks whether aws command exists - exit if not
if ! command -v aws >/dev/null 2>&1
then
    echo "Please install AWS Command Line Interface first: http://docs.aws.amazon.com/cli/latest/userguide/installing.html"
    exit 1
fi

for Region in "${Regions[@]}"
do
    echo "Verifying that cloudtrail is enabled for region $Region"

    check=`aws cloudtrail describe-trails $aws_params --region $Region --output json --query "trailList[].IsMultiRegionTrail" | grep true`
    if [ -z "$check" ];
    then
        check=`aws cloudtrail describe-trails $aws_params --region $Region --output json --query "trailList[].HomeRegion" | grep $Region`
        if [ -z "$check" ];
        then
            echo "CloudTrail is not enabled in region $Region. Please enable cloudtrail for region $Region and then re-run this script."
            exit 1
        fi
    fi
done

echo

for Region in "${Regions[@]}"
do
    echo "Verifying that cloudtrail is enabled for region $Region"

    check=`aws cloudtrail describe-trails $aws_params --region $Region --output json --query "trailList[].IsMultiRegionTrail" | grep true`
    if [ -z "$check" ];
    then
        check=`aws cloudtrail describe-trails $aws_params --region $Region --output json --query "trailList[].HomeRegion" | grep $Region`
        if [ -z "$check" ];
        then
            echo "CloudTrail is not enabled in region $Region, skipping setup for region $Region."
            echo
            continue
        fi
    fi

    if aws cloudformation describe-stacks --stack-name $Stack $aws_params --region $Region >/dev/null 2>&1
    then
        echo "Updating $Stack - v$Version on $Region"
        aws cloudformation update-stack $aws_params \
            --stack-name $Stack \
            --region $Region \
            --template-url $TemplateUrl \
            --parameters \
                ParameterKey=CloudCoreoDevTimeQueueArn,ParameterValue=$CloudCoreoDevTimeQueueArn \
                ParameterKey=CloudCoreoDevTimeTopicName,ParameterValue=$CloudCoreoDevTimeTopicName \
                ParameterKey=CloudCoreoDevTimeMonitorRule,ParameterValue=$CloudCoreoDevTimeMonitorRule \
            --tags \
                Key=Version,Value=$Version Key=LastUpdatedTime,Value="`date`"
        if [ $? -eq 0 ]
        then
            echo "Sucessfully updated $Stack on $Region"
        fi
    else
        echo "Installing $Stack - v$Version on $Region ..."
        aws cloudformation create-stack $aws_params \
            --stack-name $Stack \
            --region $Region \
            --template-url $TemplateUrl \
            --parameters \
                ParameterKey=CloudCoreoDevTimeQueueArn,ParameterValue=$CloudCoreoDevTimeQueueArn \
                ParameterKey=CloudCoreoDevTimeTopicName,ParameterValue=$CloudCoreoDevTimeTopicName \
                ParameterKey=CloudCoreoDevTimeMonitorRule,ParameterValue=$CloudCoreoDevTimeMonitorRule \
            --on-failure DO_NOTHING \
            --tags \
                Key=Version,Value=$Version Key=LastUpdatedTime,Value="`date`"
        if [ $? -eq 0 ]
        then
            echo "Successfully installed $Stack on $Region"
        fi
    fi

    echo

done
