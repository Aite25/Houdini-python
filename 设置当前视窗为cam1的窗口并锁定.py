# 获取当前 Scene View 的视窗和视口
pane_tab = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
viewport = pane_tab.curViewport()

# 获取当前选择的相机节点
selected_camera = None
for node in hou.selectedNodes():
    if node.type().name() == "cam":  # 检查节点是否为相机
        selected_camera = node
        break

# 如果没有选中相机，则尝试获取或创建 cam1
if not selected_camera:
    selected_camera = hou.node("/obj/cam1")
    if not selected_camera:
        # 创建 cam1 相机
        selected_camera = hou.node("/obj").createNode("cam", "cam1")
        # hou.ui.displayMessage("未找到 cam1，相机已新建为 cam1")

# 获取当前视口的变换矩阵
view_transform = viewport.viewTransform()

# 设置选定相机或 cam1 的世界变换矩阵
selected_camera.setWorldTransform(view_transform)

# 设置视窗使用该相机
viewport.setCamera(selected_camera)

# 锁定相机
viewport.lockCameraToView(True)
