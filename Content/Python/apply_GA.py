import unreal
import importlib
import utils
import inspect
importlib.reload(utils)

from utils import str_to_enum

MEL = unreal.MaterialEditingLibrary

ML_PATH = "MaterialFunctionMaterialLayer'/Game/Tangerie/Materials/Layers/ML_Sample.ML_Sample'"

# override_ty is "scalar" | "vector" | "texture"
def set_mat_override(asset, override_map, override_ty : str):
    apply_func = getattr(MEL, f"set_material_instance_{override_ty}_parameter_value") 
    for key, value in override_map.items():
        apply_func(asset, key, value)

def update_mat(mat_params):
    sel_asset = unreal.EditorUtilityLibrary.get_selected_assets()[0]
    set_mat_override(sel_asset, mat_params.get_editor_property("ScalarOverrides"), "scalar")
    set_mat_override(sel_asset, mat_params.get_editor_property("VectorOverrides"), "vector")
    set_mat_override(sel_asset, mat_params.get_editor_property("TextureOverrides"), "texture")


def main(ga, use_house, house, position):
    asset = unreal.EditorUtilityLibrary.get_selected_assets()[0]
    MEL.clear_all_material_instance_parameters(asset)
    piece_def = ga.get_editor_property("OutfitItems").get(position)
    update_mat(piece_def.get_editor_property("MaterialParams"))
    if use_house:
        house = str_to_enum(house)
        update_mat(piece_def.get_editor_property("HouseMaterialParams").get(house))
    MEL.update_material_instance(asset)
    unreal.EditorAssetLibrary.save_loaded_asset(asset, False)