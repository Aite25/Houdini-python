import os
import hou

# material part
mat_node = hou.node("/mat").createNode("arnold_materialbuilder")
surf_node = mat_node.createNode("arnold::standard_surface", "standard_surface")

out_node = mat_node.children()[0]
out_node.setInput(0, surf_node, 0)

mat_node.layoutChildren()

# out part
arn_render_node = hou.node("/out").createNode("arnold")

imagerbuilder = hou.node("/out").createNode("arnold_imagerbuilder")
out_img_node = imagerbuilder.children()[0]
denoise_node = imagerbuilder.createNode("arnold::imager_denoiser_oidn")
out_img_node.setInput(0, denoise_node, 0)

arn_render_node.parm("ar_imagers").set("../" + imagerbuilder.name())
imagerbuilder.layoutChildren()

hou.node("/out").layoutChildren()

# geo node creat
# geo_node = hou.node("/obj").createNode("geo")

# geo_mat_node = geo_node.createNode("material") # geo mat
# geo_null_mat_node.parm("shop_materialpath1").set(mat_node.path())

# geo_grid_node = geo_node.createNode("grid") # grid create
# geo_mat_node = geo_node.createNode("material")
# geo_mat_node.parm("shop_materialpath1").set(mat_node.path())
# geo_mat_node.setDisplayFlag(1)
# geo_mat_node.setRenderFlag(1)
# geo_uv_node = geo_node.createNode("texture")

# geo_mat_node.setInput(0, geo_uv_node, 0)
# geo_uv_node.setInput(0, geo_grid_node, 0)
# geo_node.layoutChildren()

# set arnold light
arnl_node = hou.node("/obj").createNode("arnold_light","sky")
arnl_node.parm("ar_light_type").set(6)
arnl_node.setDisplayFlag(0)
arnl_node.moveToGoodPosition()

# hou.node("/obj").layoutChildren()
