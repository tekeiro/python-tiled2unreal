
import json
import sys


def get_prop(obj, key, default_value):
    if key in obj:
        return obj[key]
    else:
        return default_value


def calculate_coordinates(x, y, tile_width, tile_height, obj_width, obj_height):
    return (x - (tile_width/2.0) + (obj_width/2.0),
        y - (tile_height/2.0) + (obj_height/2.0))


def process_tiled(tiled_map):
    """
    Process a Tiled Map Json and convert collision objects from Tiled
    coordinates into Unreal coordinates
    :param tiled_map: A dictionary converted from a Json file
    :return: A new dictionary with units converted
    """
    if 'tilesets' in tiled_map:
        tilesets = tiled_map['tilesets']
        for tileset in tilesets:
            tile_width = get_prop(tileset, 'tileheight', 0)
            tile_height = get_prop(tileset, 'tilewidth', 0)
            if 'tiles' in tileset:
                tiles = tileset['tiles']
                for tile_id, tile in tiles.items():
                    if 'objectgroup' in tile:
                        objgrps = tile['objectgroup']
                        if 'objects' in objgrps:
                            for obj in objgrps['objects']:
                                x = get_prop(obj, 'x', 0)
                                y = get_prop(obj, 'y', 0)
                                width = get_prop(obj, 'width', 0)
                                height = get_prop(obj, 'height', 0)
                                coords = calculate_coordinates(
                                    x,
                                    y,
                                    tile_width,
                                    tile_height,
                                    width,
                                    height
                                )
                                obj.update(
                                    x=coords[0],
                                    y=coords[1],
                                    old_x=x,
                                    old_y=y
                                )
                                print("Converted ({0} , {1}) to ({2} , {3})".format(
                                    x, y, *coords
                                ))


    return tiled_map

input_file = sys.argv[1]
output_file = input_file + '_new'
if len(sys.argv) > 2:
    output_file = sys.argv[2]

new_map = None

with open(input_file, 'r',  encoding='utf-8') as input:
    read = input.read()
    data = json.loads(read)
    new_map = process_tiled(data)

with open(output_file, 'w', encoding='utf-8') as out:
    out.write(json.dumps(new_map, indent=4, sort_keys=True))