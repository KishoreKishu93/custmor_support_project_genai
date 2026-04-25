import yaml

def load_config(config_path:str =r"E:\custmor_support_project_genai\config\config.yaml")-> dict:
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config
