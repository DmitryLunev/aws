import argparse
import json
import logging
import boto3
import docker
import watchtower
from botocore.exceptions import ClientError
from dotenv import load_dotenv


def run_docker(image, command, logger):
    client = docker.from_env()
    container = None
    try:
        container = client.containers.run(
            image, command, detach=True, remove=True, stdout=True, stderr=True)
        logger.info(f"Started container with command: {command}")
        for line in container.logs(stream=True):
            logger.info(line.decode('utf-8').strip())
    except docker.errors.ContainerError as e:
        logger.error(f"Error running container: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
    finally:
        if container is not None:
            try:
                container.stop()
                container.remove()
                logger.info("Container stopped and removed.")
            except docker.errors.APIError as e:
                if "removal of container" in str(e):
                    logger.info(
                        "Container is already in the process of being removed.")
                else:
                    logger.error(
                        f"Error stopping/removing container: {str(e)}")


def aws_setup_logs(log_group_name, log_stream_name, region_name, access_key, secret_key):
    boto3_client = boto3.client(
        'logs',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region_name
    )
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    handler = watchtower.CloudWatchLogHandler(
        boto3_client=boto3_client,
        log_group=log_group_name,
        stream_name=log_stream_name
    )
    logger.addHandler(handler)

    try:
        boto3_client.create_log_group(logGroupName=log_group_name)
    except ClientError as e:
        if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
            logger.error(f"Could not create log group: {str(e)}")

    try:
        boto3_client.create_log_stream(
            logGroupName=log_group_name, logStreamName=log_stream_name)
    except ClientError as e:
        if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
            logger.error(f"Could not create log stream: {str(e)}")

    return logger, boto3_client


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run Docker and log to AWS CloudWatch.")
    parser.add_argument(
        "--config", help="Path to config file.", default="config.json")
    parser.add_argument("--docker-image", help="Name of the Docker image.")
    parser.add_argument(
        "--bash-command", help="Bash command to run inside the Docker.")
    parser.add_argument("--aws-cloudwatch-group",
                        help="AWS CloudWatch log group name.")
    parser.add_argument("--aws-cloudwatch-stream",
                        help="AWS CloudWatch log stream name.")
    parser.add_argument("--aws-access-key-id", help="AWS access key ID.")
    parser.add_argument("--aws-secret-access-key",
                        help="AWS secret access key.")
    parser.add_argument("--aws-region", help="AWS region.")
    return parser.parse_args()


def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)


if __name__ == "__main__":
    load_dotenv()

    args = parse_args()
    config = load_config(args.config)

    docker_image = args.docker_image or config['docker_image']
    bash_command = args.bash_command or config['bash_command']
    aws_cloudwatch_group = args.aws_cloudwatch_group or config['aws_cloudwatch_group']
    aws_cloudwatch_stream = args.aws_cloudwatch_stream or config['aws_cloudwatch_stream']
    aws_access_key_id = args.aws_access_key_id or config['aws_access_key_id']
    aws_secret_access_key = args.aws_secret_access_key or config['aws_secret_access_key']
    aws_region = args.aws_region or config['aws_region']

    logger, aws_client = aws_setup_logs(
        aws_cloudwatch_group,
        aws_cloudwatch_stream,
        aws_region,
        aws_access_key_id,
        aws_secret_access_key
    )

    run_docker(docker_image, bash_command, logger)
