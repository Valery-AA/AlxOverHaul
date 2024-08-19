from copy import copy
import random
from pathlib import Path

import bpy
from bpy_extras import image_utils


class Alx_OT_UVTools_udim_square_compressor(bpy.types.Operator):
    """"""

    bl_label = "UVTools - Square UDIM Compressor"
    bl_idname = "alx.operator_uvtools_udim_square_compressor"

    bl_description = "currently requires the udim to be formatted in a square without an empty image, compresses it into a single image with the resolution as the total of the udims images"

    def execute(self, context: bpy.types.Context):
        image_pointer = context.window_manager.alx_session_properties.udim_texture_compressor_texture_target

        if (image_pointer is not None):
            source_image : bpy.types.Image = bpy.data.images.get(image_pointer.name)
            source_colorspace = source_image.colorspace_settings.name

            if (source_image is not None):
                error_string = ""
                if (  not source_image.name.__contains__( ".<UDIM>." ) ):
                    self.report({"ERROR"}, message="Error: image name missing '<UDIM>'. image might not be a udim\n")
                    return {"CANCELLED"}
                    
                if ( len( source_image.name ) > 63):
                    self.report({"ERROR"}, message="Error: image name exceeds blender's 63 characters limit and has been truncated\n")
                    return {"CANCELLED"}

                if  ( len( Path( source_image.filepath ).name ) > 63 ):
                    self.report({"ERROR"}, message="Error: image file name exceeds blender's 63 characters limit and has been truncated\n")
                    return {"CANCELLED"}

                target_image_name = f"""{source_image.name.replace(".<UDIM>", "")}"""
                
                udim_tiles = { tile.number : tile for tile in source_image.tiles}
                udim_tiles_numbers = udim_tiles.keys()
                high_tile = max(udim_tiles_numbers)

                if ( high_tile > 1100 ):
                    self.report({"ERROR"}, message="Error: udim image tiles number exceed the maximum supported for a square: 100 tiles of maximum index 1100")
                    return {"CANCELLED"}

                if ( high_tile not in range(1012, 1100, 11) ):
                    self.report({"ERROR"}, message="Error: udim image tile with the highest tile number breaks square shape, maintain the last tile as the top right corner of a square")
                    return {"CANCELLED"}


                tile_side_max_size = max( int( str( high_tile )[2] ), high_tile % 10)
                _tile_numbers_generated_template = {i for i in range(1001, high_tile + 1) if (i % 10 <= tile_side_max_size) and ( (i % 10 != 0) and (tile_side_max_size != 10) )}

                existing_tiles_numbers = set(udim_tiles_numbers).intersection(_tile_numbers_generated_template)
                missing_tiles_numbers = existing_tiles_numbers.symmetric_difference(_tile_numbers_generated_template)

                if ( tile_side_max_size == 0 ):
                    self.report({"ERROR"}, message="Error: tiles could not be identified, make sure all the images are saved to disk")
                    return {"CANCELLED"}

                minimum_resolution_x = max([tile.size[0] for tile in udim_tiles.values()])
                minimum_resolution_y = max([tile.size[1] for tile in udim_tiles.values()])

                minimum_resolution = max(minimum_resolution_x, minimum_resolution_y) 

                if (bpy.data.images.get(target_image_name) is not None):
                    bpy.data.images.remove(bpy.data.images.get(target_image_name))

                udim_images_pixel_map : dict[int, list] = dict()

                udim_images_paths = { udim_number : source_image.filepath.replace("<UDIM>", f"{udim_number}") 
                                     for udim_number in existing_tiles_numbers 
                                     if (source_image.filepath.replace("<UDIM>", f"{udim_number}") != "")
                                     }

                udim_images = { image_tile_number : image_utils.load_image( image_path ) for image_tile_number, image_path in udim_images_paths.items() if ( Path(image_path).exists() ) }
                for image_tile_number, image in udim_images.items():
                    udim_images_pixel_map[image_tile_number] = list(copy(image.pixels[:]))

                udim_images_pixel_map.update({ tile_key : [val for i in range(0, minimum_resolution*minimum_resolution) for val in [0, 0, 0, 1]]
                                              for tile_key in missing_tiles_numbers
                                              })

                target_image : bpy.types.Image = bpy.data.images.new(
                    name=target_image_name, 
                    width=minimum_resolution * tile_side_max_size, 
                    height=minimum_resolution * tile_side_max_size
                    ) 
                
                target_image.generated_width = minimum_resolution * tile_side_max_size
                target_image.generated_height = minimum_resolution * tile_side_max_size
                


                target_image_pixels = list()
                udim_row = 0
                for i in range(tile_side_max_size):
                    for pixel_row in range(0, minimum_resolution):                     
                        for udim_tile_number in sorted(list(udim_images_pixel_map.keys())):
                            if ( udim_tile_number in range(1001 + (10 * udim_row), 1010 + (10 * udim_row))):
                                target_image_pixels.extend( udim_images_pixel_map[udim_tile_number][(minimum_resolution * 4) * pixel_row : (minimum_resolution * 4) * (1 + pixel_row)] )

                    udim_row += 1

                target_image.source = "GENERATED"
                target_image.pixels[:len(target_image_pixels)] = target_image_pixels

                for image in udim_images.values():
                    bpy.data.images.remove(image)

        return {"FINISHED"}
    
    def draw(self, context: bpy.types.Context):
        properties = context.window_manager.alx_session_properties
        self.layout.prop(properties, "udim_texture_compressor_texture_target")

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        return context.window_manager.invoke_props_dialog(self, width=300)