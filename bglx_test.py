import bpy
import bglx
import bgl


bl_info = {
    "name": "bglx test",
    "author": "N",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "bglx test",
    "description": "bglx testing",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"
}


class BGLX_OT_Render(bpy.types.Operator):

    bl_idname = "view_3d.bglx_render"
    bl_label = "BGLX"
    bl_description = "BGLX"

    __handle = None

    def __handle_add(self, context):
        if BGLX_OT_Render.__handle is None:
            BGLX_OT_Render.__handle = bpy.types.SpaceView3D.draw_handler_add(
                BGLX_OT_Render.__render,
                (context, ), 'WINDOW', 'POST_PIXEL'
            )

    def __handle_remove(self, context):
        if BGLX_OT_Render.__handle is not None:
            bpy.types.SpaceView3D.draw_handler_remove(
                BGLX_OT_Render.__handle, 'WINDOW'
            )
            BGLX_OT_Render.__handle = None

    @classmethod
    def is_running(cls):
        return cls.__handle is not None

    @staticmethod
    def __render(context):
        img = bpy.data.images["uv_checker large.png"]
        if img.gl_load():
            raise Exception("Failed to load image")

        # OpenGL configuration
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glEnable(bgl.GL_TEXTURE_2D)
        bgl.glActiveTexture(bgl.GL_TEXTURE0)
        if img.bindcode:
            bind = img.bindcode
            bgl.glBindTexture(bgl.GL_TEXTURE_2D, bind)

        bglx.glBegin(bglx.GL_QUADS)
        bglx.glColor4f(1.0, 0.2, 1.0, 0.5)
        bglx.glVertex2f(100.0, 100.0)
        bglx.glTexCoord2f(0.0, 0.0)
        bglx.glVertex2f(100.0, 300.0)
        bglx.glTexCoord2f(0.0, 1.0)
        bglx.glVertex2f(300.0, 300.0)
        bglx.glTexCoord2f(1.0, 1.0)
        bglx.glVertex2f(300.0, 100.0)
        bglx.glTexCoord2f(1.0, 0.0)
        bglx.glEnd()


    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            if not BGLX_OT_Render.is_running():
                self.__handle_add(context)
            else:
                self.__handle_remove(context)

            if context.area:
                context.area.tag_redraw()
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class BGLX_PT_Testing(bpy.types.Panel):
    bl_label = "bglx"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        if BGLX_OT_Render.is_running():
            layout.operator(BGLX_OT_Render.bl_idname, text="end", icon="PAUSE")
        else:
            layout.operator(BGLX_OT_Render.bl_idname, text="start", icon="PLAY")


def register():
    bpy.utils.register_class(BGLX_OT_Render)
    bpy.utils.register_class(BGLX_PT_Testing)


def unregister():
    bpy.utils.unregister_class(BGLX_PT_Testing)
    bpy.utils.unregister_class(BGLX_OT_Render)


if __name__ == "__main__":
    register()
