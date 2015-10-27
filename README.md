# docker_registry_clean
__author__ = 'Kuhn'

company = 'Asiainfo'

qq:170478063

清理docker私有仓库

目前支持v1版本的docker registry

当前功能：

1.清理指定image:tag

2.当image所有的tag均删除后，会尝试删除该image历史冗余的所有镜像

操作方法：

1.下载本工具包docker_registry_clean

2.将docker_registry_clean目录放在docker私有仓库所在主机的某个目录下（需要有操作仓库目录的权限）

3.执行如下命令

    python delete-image.py  {registry_path}  {image_name:image_tag}
    
    ----------{registry_path}是仓库所在目录，其实就是启动仓库的时候指定的目录（-v /home/registry-storage:/home/registry-storage -w /home/registry-storage） 默认V1版本的仓库根目录下有这两个目录：images  repositories
    
    ----------{image_name:image_tag}  镜像:tag
    


