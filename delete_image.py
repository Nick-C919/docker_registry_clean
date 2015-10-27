# /usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'Kuhn'
# company = 'Asiainfo'
# qq:170478063

import os,sys,shutil
import json


#将仓库中所有节点关系导出
class Nodes:
    # 初始化
    def __init__(self, registry_path):
        self.registry_path = registry_path

    #节点信息
    def nodes(self):
        #获取仓库下所有images名
        images_list = os.listdir(self.registry_path+ "/images/")
        #images
        image_id_parent = {}
        image_parent_list = []
        # print  images_list
        for image in images_list:
            image_json_file = self.registry_path + "/images/" + image + "/json"
            image_json_f = open( image_json_file  , "r" )
            image_json = json.loads( image_json_f.readline())
            image_json_f.close()
            image_id = image_json['id']
            if image_json.has_key('parent'):
                image_parent = image_json['parent']
                image_id_parent[image_id]=image_parent
                image_parent_list.append(image_parent)
            else:
                image_id_parent[image_id]=""
        return [image_id_parent,image_parent_list]

#元数据处理
class Metadata:
    # 初始化
    def __init__(self, registry_path,image_name,image_tag):
        self.registry_path = registry_path
        self.image_name  = image_name
        self.image_tag  = image_tag
    #获取目标image_name：image_name的ID
    def get_image_id(self):
        try:
            image_id_file = self.registry_path + "/repositories/library/" + self.image_name + "/tag_" + self.image_tag
            if os.path.isfile(image_id_file) :
                # image_id_file = self.registry_path + "/repositories/library/" + self.image_name + "/tag_" + self.image_tag
                image_id_f = open( image_id_file  , "r" )
                image_id =  image_id_f.readline()
                image_id_f.close()
            else:
                print "[ERROR]   " + self.image_name + ":" + self.image_tag + "元数据不存在！！请检查输入是否正确"
                sys.exit(0)
        except Exception , e:
            print  e
            sys.exit(0)
        return image_id
    #删除镜像对应的tag
    def delete_tag(self):
        os.remove(self.registry_path + "/repositories/library/" + self.image_name + "/tag_" + self.image_tag)
        os.remove(self.registry_path + "/repositories/library/" + self.image_name + "/tag" + self.image_tag + "_json")
    #删除镜像对应的index
    def delete_index(self,image_id):
        image_index_file = self.registry_path + "/repositories/library/" + self.image_name + "/_index_images"
        image_index_f = open( image_index_file  , "r" )
        image_index =  image_index_f.readline()
        image_index_f.close()
        index_list = json.loads(image_index)
        index_list_new = []
        for index in index_list:
            if index['id'] != image_id:
                index_list_new.append({'id':str(index['id'])})
        image_index_new = json.dumps(index_list_new)
        image_index_file = self.registry_path + "/repositories/library/" + self.image_name + "/_index_images"
        image_index_f = open( image_index_file  , "w" )
        image_index_f.write(image_index_new)
        image_index_f.close()

#删除某个镜像
class Delete_image:
    # 初始化
    def __init__(self, registry_path,image_name,image_tag,nodes):
        self.registry_path = registry_path
        self.image_name  = image_name
        self.image_tag  = image_tag
        self.nodes  = nodes
        # print self.nodes

    #打印镜像递归列表：
    def print_image_list(self):
        print "print_image_list"

    #删除镜像实体
    def delete_image(self,image_id_t,metadata,begin='Y'):
        print "[INFO]   ID：" + str(image_id_t)
        if (self.nodes[1].count(image_id_t) == 0 and begin=='Y') or ( self.nodes[1].count(image_id_t) == 1 and begin=='N' ) :#判断是否被依赖
            print "[INFO]   删除元数据index信息"
            metadata.delete_index(str(image_id_t))
            if str(image_id_t) in self.nodes[0]:#判断镜像是否能找到实体

                print "[INFO]   删除image实体"
                # os.remove(self.registry_path + "/images/" + image_id_t)
                shutil.rmtree(self.registry_path + "/images/" + str(image_id_t))
                #找出父镜像ID
                parent_id = self.nodes[0][image_id_t]
                #更新self.nodes
                del self.nodes[0][image_id_t]
                if image_id_t in self.nodes[1]:
                    self.nodes[1].remove(image_id_t)
                # print  self.nodes
                self.delete_image(parent_id,metadata,begin='N')
            else:
                print str(image_id_t)+"不存在，不需要删除"
        else:
            print "[INFO]   ID：" + str(image_id_t) + "被依赖"

    #删除某个镜像，以及递归的父镜像，如果父镜像有其他依赖，则退出
    def run(self):
        print "[BEGIN]   删除镜像"+self.image_name+":"+self.image_tag
        #打印镜像递归列表
        # self.print_image_list()
        #根据元数据获取image_ID
        metadata = Metadata(self.registry_path,self.image_name,self.image_tag)
        image_id = metadata.get_image_id()
        #删除该image的元数据信息
        print "[INFO]   删除元数据tag信息"
        metadata.delete_tag()
        #根据树结构删除Image节点以及对应index信息
        self.delete_image(image_id,metadata)

        #如果镜像已经不存在tag，则根据_index_images删除所有多余的
        image_index_file = self.registry_path + "/repositories/library/" + self.image_name + "/_index_images"
        if  (len(os.listdir( self.registry_path + "/repositories/library/" + self.image_name )) == 1) and  os.path.isfile(image_index_file) :
            image_index_f = open( image_index_file  , "r" )
            image_index =  json.loads( image_index_f.readline())
            print  "[INFO]   该镜像已无任何tag，需要清理遗留层！！！"
            for image_index_t in image_index:
                #根据树结构删除Image节点以及对应index信息
                # print image_index_t['id']
                self.delete_image(image_index_t['id'],metadata)
            image_index_f.close()

        # image_index_files = os.listdir( self.registry_path + "/repositories/library/" + self.image_name )
        # if len(image_index_files) == 1:
        #     print "[INFO]   镜像"+self.image_name+"已清空，删除对应元数据信息"
        #     shutil.rmtree(self.registry_path + "/repositories/library/" + self.image_name)
        print "[END]   删除镜像"+self.image_name+"完成"

# def usage():
#     print "Usage:"
#     print "    python delete-image.py  {registry_path}  {image_name:image_tag}"
#
# if __name__ == '__main__':
#     if len(sys.argv) == 3:
#         registry_path = sys.argv[1]
#         image_name =  sys.argv[2].split(':')[0]
#         image_tag =  sys.argv[2].split(':')[1]
#     else:
#         usage()
#         sys.exit(0)
#     nodes_J = Nodes(registry_path)
#     nodes = nodes_J.nodes()
#     # print nodes[0]
#     # print nodes[1]
#     #删除指定的镜像tag
#     delete_image = Delete_image(registry_path,image_name,image_tag,nodes)
#     delete_image.run()


