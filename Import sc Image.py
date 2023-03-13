import os,re,hou

# D:/srvv/arnold sc test/Comp_2_Diffuse/Comp_2_diffuse_`padzero(5,min($F,39))`.jpg

folder_path = r"D:\srvv\arnold sc test\Comp_2_Diffuse"
format = ".jpg"

# replace string "sc_width, scmax_num, scmin_num" with file data 
scstr = r"`padzero(sc_width,min($F,max_scnum))`"

# scstr = r'`details(0,"scstr")`'

folder_name = re.split(r"\\|/",folder_path)[-1]

def scfolder_data_extract( folder_path , format, scstr):
    folder_path = folder_path.replace("\\","/")
    allfiles = os.listdir(folder_path)
    folder_name = re.split(r"\\|/",folder_path)[-1]
    
    partten = re.compile(r"(.*?)(\d+)" + format)
    
    scfile_list = []
    scfile_dict_list = []
    for eachfile in allfiles:
        if(eachfile.endswith(format)):
            partten_search = partten.search(eachfile)
            if partten_search is not None:
                scfile_list.append(eachfile)
                scidx_str = partten_search.group(2)
                scdict = {
                    "name":eachfile,
                    "format":format,
                    "scidx":scidx_str,
                    "sc_width":len(scidx_str),
                    "scidx_num":int(scidx_str),
                    "prefix":partten_search.group(1)
                }
                scfile_dict_list.append(scdict)
    
    max_scnum = scfile_dict_list[-1]["scidx_num"]
    min_scnum = scfile_dict_list[0]["scidx_num"]
    prefix = scfile_dict_list[0]["prefix"]
    sc_width = scfile_dict_list[0]["sc_width"]
    
    output_sc_dict = {
        "path":folder_path,
        "prefix":prefix,
        "min_scnum":min_scnum,
        "max_scnum":max_scnum,
        "sc_width":sc_width
    }
    print("folder path : " + folder_path)
    print("scwidth : " + str(output_sc_dict["sc_width"]))
    print("sc range : " + str(output_sc_dict["min_scnum"]) + "," + str(output_sc_dict["max_scnum"]))
    print('sprintf("%.' + str(output_sc_dict["sc_width"]) +'g",int(fit(@process,0,1,'+ str(output_sc_dict["min_scnum"]) + "," + str(output_sc_dict["max_scnum"]) + ')')
    
    scstr = scstr.replace("sc_width", str(output_sc_dict["sc_width"]))
    scstr = scstr.replace("min_scnum", str(output_sc_dict["min_scnum"]))
    scstr = scstr.replace("max_scnum", str(output_sc_dict["max_scnum"]))
    
    filename_str = output_sc_dict["path"] + "/" + scdict["prefix"] + scstr + format
    return filename_str
    
filename_str = scfolder_data_extract(folder_path, format, scstr)

print(filename_str)

def create_houdini_node(filename_str, nodepath = 0, nodetype = 0, filename_parm = "", extra_parm_dict = {}):
    if nodepath == 0:
        nodepath = "/obj"
        geo_node = hou.node( nodepath ).createNode("geo")
        sc_img_node = geo_node.createNode("uvquickshade")
        sc_img_node.parm("texture").set( filename_str )
        sc_img_node.parm("texture_sv").set( -1 )
        if extra_parm_dict != {}:
            for parmpath in extra_parm_dict:
                sc_img_node.parm(parmpath).set(extra_parm_dict[parmpath])
        
        return uvquickshade_node
        
    elif nodepath == 1:
        nodepath = "/mat"
        nodetype = "arnold::image"
        filename_parm = "filename"
        arn_node = hou.node( nodepath ).createNode("arnold_materialbuilder","arnold_import_imgsc")
        sc_img_node = arn_node.createNode(nodetype)
        sc_img_node.parm( filename_parm ).set( filename_str )
        sc_img_node.parm( "ignore_missing_textures" ).set( 1 )
        if extra_parm_dict != {}:
            for parmpath in extra_parm_dict:
                sc_img_node.parm(parmpath).set(extra_parm_dict[parmpath])
        return sc_img_node
        
    if nodetype == 0:
        nodetype = "uvquickshade"
        sc_img_node = hou.node(nodepath).createNode( nodetype )
        sc_img_node = geo_node.createNode( nodetype )
        sc_img_node.parm("texture").set( filename_str )
        sc_img_node.parm("texture_sv").set( -1 )
        if extra_parm_dict != {}:
            for parmpath in extra_parm_dict:
                sc_img_node.parm(parmpath).set(extra_parm_dict[parmpath])
        
        return uvquickshade_node
        
    elif nodetype == 1:
        nodetype = "arnold::image"
        filename_parm = "filename"
        sc_img_node = hou.node(nodepath).createNode(nodetype)
        sc_img_node.parm( filename_parm ).set( filename_str )
        sc_img_node.parm( "ignore_missing_textures" ).set( 1 )
        if extra_parm_dict != {}:
            for parmpath in extra_parm_dict:
                sc_img_node.parm(parmpath).set(extra_parm_dict[parmpath])
        
        return image_node
        
    sc_img_node = hou.node( nodepath ).createNode( nodetype )
    sc_img_node.parm( filename_parm ).set( filename_str )

    if extra_parm_dict != {}:
        for parmpath in extra_parm_dict:
            sc_img_node.parm(parmpath).set(extra_parm_dict[parmpath])
    
    return sc_img_node

# create_houdini_node( filename_str ,"/mat/arnold_materialbuilder1","arnold::image","filename",{"ignore_missing_textures":1,})
sc_img_node = create_houdini_node(filename_str, 1)
ss_node = hou.node('/mat/arnold_import_imgsc').createNode("arnold::standard_surface")

hou.node('/mat/arnold_import_imgsc/OUT_material').setInput(0,ss_node,0)
ss_node.parm("emission").set(1)
ss_node.setInput(1,sc_img_node,0)
ss_node.setInput(37,sc_img_node,0)
sc_img_node.setName(folder_name)
hou.node('/mat/arnold_import_imgsc').layoutChildren()

# sc_img_node = create_houdini_node(filename_str, '/obj/geo2','uvquickshade','texture',{"texture_sv":-1})








