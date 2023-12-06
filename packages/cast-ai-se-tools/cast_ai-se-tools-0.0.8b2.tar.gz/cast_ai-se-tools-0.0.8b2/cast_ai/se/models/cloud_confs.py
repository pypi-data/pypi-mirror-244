from cast_ai.se.misc_utils import get_environment_variable


class AwsConfig:
    def __init__(self):
        self.region = get_environment_variable("AWS_REGION")
        self.default_node_group = get_environment_variable("AWS_DEFAULT_NODE_GROUP")
        self.access_key = get_environment_variable("AWS_ACCESS_KEY")
        self.access_secret_key = get_environment_variable("AWS_ACCESS_SECRET_KEY")
