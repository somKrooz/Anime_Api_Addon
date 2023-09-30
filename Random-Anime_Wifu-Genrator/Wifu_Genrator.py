bl_info = {
    "name": "Anime_girl_genrator",
    "author": "SomKrooz",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View_3D > Anime_girl_genrator",
    "description": "Genrates random images of anime girls",
    "category": "Materials",
}


import bpy
import requests
import requests
import random
import time
import os
import bpy



class Main_OT_Panel(bpy.types.Panel):
    bl_label = "Anime Girl Genrator"
    bl_idname = "OBJECT_PT_texttool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Anime Girl Genrator"
    
 
    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("plane.create",text = "Create Planes",icon="OUTLINER_OB_LATTICE")
        row = layout.row()
        row.label(text= "Select items before Runing it")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("api.recall",text="Run",icon="DISCLOSURE_TRI_RIGHT")


def Api_Recall(context):
    a = 0
    step = 0
    filename = "Cache"

    def createFile():
        dir = os.path.expanduser('~/documents')   #Here
        path= os.path.join(dir,filename)

        if filename in os.listdir(dir):
            pass
        else:
            os.mkdir(path)
    
        print(path)
        return path

    images_dir = createFile()

    for i in os.listdir(images_dir):
        os.remove(os.path.join(images_dir,i))


    querries = ['maid','waifu','mori-calliope','oppai','selfies','uniform','raiden-shogun','marin-kitagawa']

    #Fetch_Api
    def getdata():
        rand_querry = random.choices(querries)

        params={
            'include_tags': rand_querry,
        }
        res = requests.get('https://api.waifu.im/search',params=params)
        data = res.json()
        print(rand_querry)
        url = data['images'][0]['url']
        name = str(url).split('/')


        img = requests.get(url)
        fp = open(f"{os.path.expanduser('~/documents')}/{filename}/{name[-1]}", 'wb')   #Here
        fp.write(img.content)
        fp.close()
        print(url)

    for i in bpy.context.selected_objects:
        a=a+1

    for i in range(a):
        getdata()
        time.sleep(0.2)


    #make array of images relative path
    path = os.path.join(os.path.expanduser('~/documents'),filename)  #Here
    arr = []
    for i in os.listdir(path):
        new_path = os.path.join(path,i)
        bpy.data.images.load(new_path)
        arr.append(new_path)


    for i in bpy.context.selected_objects:
        step = step+1
        mat = bpy.data.materials.new(f"random-api:"+"Anime")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Roughness"].default_value = 0
        texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
        texImage.image = bpy.data.images.load(arr[step-1])
        mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
        # mat.node_tree.links.new(bsdf.inputs['Emission'], texImage.outputs['Color'])
    
        if i.data.materials:

            i.data.materials[0] = mat
        else:

            i.data.materials.append(mat)

    for img in bpy.data.images:
        if not img.users:
            bpy.data.images.remove(img)

    for material in bpy.data.materials:
        if not material.users:
            bpy.data.materials.remove(material)


class Api_OT_Recall_API(bpy.types.Operator):

    bl_label = "Anime Girl Genrator"
    bl_idname = "api.recall"

    def execute(self, context):
        Api_Recall(context)
        return {'FINISHED'}


class Plane_OT_Create_Plane(bpy.types.Operator):
    bl_label = "Anime Girl Genrator"
    bl_idname = "plane.create"

    text : bpy.props.IntProperty(name="Enter number", default=1)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
        
 
    def execute(self, context):
        
        t = self.text

        gap = 6

        for i in range(t):
            bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            bpy.context.object.scale[0] = 2.6
            bpy.context.object.scale[1] = 4
            bpy.context.object.scale[2] = 4
            bpy.ops.transform.translate(value=(gap*i, 0, 0), orient_type='GLOBAL')
        return {'FINISHED'} 




 
def register():
    bpy.utils.register_class(Main_OT_Panel)
    bpy.utils.register_class(Api_OT_Recall_API)
    bpy.utils.register_class(Plane_OT_Create_Plane)
 
 
def unregister():
    bpy.utils.unregister_class(Main_OT_Panel)
    bpy.utils.unregister_class(Api_OT_Recall_API)
    bpy.utils.unregister_class(Plane_OT_Create_Plane)
 
 
if __name__ == "__main__":
    register()