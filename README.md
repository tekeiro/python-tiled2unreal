# tiled2unreal
Convert Tiled Json file properly to be imported to Unreal Engine TileMap.
Currently, there is a problem importing a TiledMap json file with tile collision information 
into Unreal, due to Unreal understand collision box of a different way of Tiled.  

## How to use
When you export a tmx map into a json file, before import into Unreal, execute
this script to adjust collision box coordinates. Use following command:

`python tiled2unreal.py %input_file% %output_file%`


# rpgtex2tiled
Convert all terrain in a RPG Maker Image into a spritesheet of tiles
ready for Tiled Map.

## Dependencies
You need to install Pillow module for Python

`pip install Pillow`

##How to use
Use following way:
`python rpgtex2tiled.py %img_file_path%`

