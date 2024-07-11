from copy import copy
from pathlib import Path

import bpy
from bpy_extras import image_utils


class Alx_OT_UV_UDIM_SquareCompressor(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.operator_uv_udim_square_compressor"

    @classmethod
    def poll(self, context: bpy.types.Context):
        return True
    
    def execute(self, context: bpy.types.Context):
        properties = context.window_manager.alx_session_properties
        if (properties.udim_texture_compressor_texture_target is not None):
            source_image : bpy.types.Image = bpy.data.images.get(properties.udim_texture_compressor_texture_target.name)
            source_colorspace = source_image.colorspace_settings.name

            if (source_image is not None):
                if ( len( Path( source_image.filepath.replace("<UDIM>", "1001") ).name ) > 63 ):
                    self.report({"ERROR"}, message="File name exceeds the 63 character limit")
                    return {"CANCELLED"}

                target_image_name = source_image.name.replace(".<UDIM>", "")
                
                tiles = {tile.number: tile for tile in source_image.tiles}
                pixel_base_x = sum([ tiles[tile_number].size[0] for tile_number in tiles.keys() if (tile_number < 1011)])
                pixel_base_y = sum([ tiles[tile_number].size[1] for tile_number in tiles.keys() if ((tile_number - 1000) % 10 == 1)])

                target_image : bpy.types.Image = bpy.data.images.new(
                    name=target_image_name, 
                    width=pixel_base_x, 
                    height=pixel_base_y, 
                    alpha=(source_image.alpha_mode != "NONE"),
                    ) if bpy.data.images.get(target_image_name) is None else bpy.data.images.get(target_image_name)
                
                target_image.generated_width = pixel_base_x
                target_image.generated_height = pixel_base_y

                udim_images_paths = {udim_number : source_image.filepath.replace("<UDIM>", f"{udim_number}") for udim_number in sorted(tiles.keys())}
                udim_images = { udim_image_index : image_utils.load_image( udim_images_paths[udim_image_index] ) if bpy.data.images.get( Path( udim_images_paths[udim_image_index] ).name ) is None else bpy.data.images.get( Path( udim_images_paths[udim_image_index] ).name ) for udim_image_index in sorted(udim_images_paths.keys()) }
                udim_pixel_map = {udim_image_index : copy(udim_images[udim_image_index].pixels[:])  for udim_image_index in sorted(udim_images.keys()) if (udim_images[udim_image_index] is not None) }


                target_pixels = []
                target_size = udim_images[1001].size[0]
                for udim_tile_index in sorted(tiles.keys()):
                    if ( (udim_tile_index - 1000) % 10 == 1):

                        for pixel_row in range(0, udim_images[udim_tile_index].size[1]):
                            current_pixel = pixel_row * udim_images[udim_tile_index].size[0] * 4

                            for i in range(0, 10):
                                seqence_tile_index = udim_tile_index + i
                                if ( seqence_tile_index in udim_pixel_map.keys() ):
                                    target_pixels.extend( udim_pixel_map[seqence_tile_index][current_pixel : current_pixel + udim_images[seqence_tile_index].size[0]*4] )
                                else:
                                    pass
                                    #target_pixels.extend(  )

                target_image.source = "GENERATED"
                target_image.pixels[:len(target_pixels)] = target_pixels

                for image in udim_images.values():
                    bpy.data.images.remove(image)

        return {"FINISHED"}
    
    def draw(self, context: bpy.types.Context):
        properties = context.window_manager.alx_session_properties
        self.layout.prop(properties, "udim_texture_compressor_texture_target")

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        return context.window_manager.invoke_props_dialog(self, width=300)