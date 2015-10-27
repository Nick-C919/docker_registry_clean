# docker_registry_clean
清理docker私有仓库

目前支持v1版本的docker registry

当前功能：
1.清理指定image:tag
2.当image所有的tag均删除后，会尝试删除该image历史冗余的所有镜像

操作方法：
Usage:
    python delete-image.py  {registry_path}  {image_name:image_tag}




