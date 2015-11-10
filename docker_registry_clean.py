# /usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'Kuhn'
# company = 'Asiainfo'
# qq:170478063

import os,sys,shutil,re
import json
from delete_image import Nodes
from delete_image import Metadata
from delete_image import Delete_image





def usage():
    print "Usage:"
    print "    python delete-image.py  {registry_path}  {image_name:image_tag}"

if __name__ == '__main__':
    if len(sys.argv) == 3 :
        registry_path = sys.argv[1]
        if re.search(':',sys.argv[2]) == None:    #清理指定镜像内的无用层
            image_name =  sys.argv[2].split(':')[0]
            nodes_J = Nodes(registry_path)
            nodes = nodes_J.nodes()
            #删除指定的镜像tag
            delete_image = Delete_image(registry_path,image_name,nodes)
            delete_image.clean_run()
        else:                                      #删除指定镜像指定tag
            image_name =  sys.argv[2].split(':')[0]
            image_tag =  sys.argv[2].split(':')[1]
            nodes_J = Nodes(registry_path)
            nodes = nodes_J.nodes()
            #删除指定的镜像tag
            delete_image = Delete_image(registry_path,image_name,nodes,image_tag)
            delete_image.run()
    else:
        usage()
        sys.exit(0)


