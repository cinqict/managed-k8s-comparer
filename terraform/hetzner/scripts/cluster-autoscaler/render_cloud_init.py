import os
from jinja2 import Template

def render_cloud_init(template_path, output_path, context):
    with open(template_path) as f:
        template = Template(f.read())
    user_data = template.render(**context)
    with open(output_path, "w") as out:
        out.write(user_data)
    return user_data

if __name__ == "__main__":
    context = {
        "worker_public_key": os.environ.get("WORKER_PUBLIC_KEY"),
        "worker_private_key": os.environ.get("WORKER_PRIVATE_KEY"),
    }
    render_cloud_init(
        os.environ.get("CLOUD_INIT_TEMPLATE", "cloud-init-worker.yaml"),
        os.environ.get("CLOUD_INIT_RENDERED", "cloud-init-worker-rendered.yaml"),
        context
    )
