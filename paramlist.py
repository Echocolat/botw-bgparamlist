from bcml import util
import os
import oead
import json
from pathlib import Path

actor_folder = os.listdir(str(util.get_update_dir()) + '\\Actor\\Pack')

def oead_to_normal(obj):
    obj_type = type(obj)
    if obj_type not in [oead.S32, oead.U32, oead.F32, oead.byml.Array, oead.byml.Hash, oead.FixedSafeString64, oead.FixedSafeString32, oead.Vector3f,
    oead.FixedSafeString256]:
        return obj
    if obj_type is oead.S32 or obj_type is oead.U32:
        return int(obj)
    elif obj_type is oead.F32:
        return float(obj)
    elif obj_type is oead.FixedSafeString64 or obj_type is oead.FixedSafeString32 or obj_type is oead.FixedSafeString256:
        return str(obj)
    elif obj_type is oead.Vector3f:
        return (oead_to_normal(obj.x), oead_to_normal(obj.y), oead_to_normal(obj.z))
    elif obj_type is oead.byml.Array:
        _list = list()
        for item in list(obj):
            _list.append(oead_to_normal(item))

        return _list
    elif obj_type is oead.byml.Hash:
        _dict = dict()
        for key, value in dict(obj).items():
            _dict[oead_to_normal(key)] = oead_to_normal(value)

        return _dict

def create_jsons():

    all_params = {}

    for file in actor_folder:
        sarc = oead.Sarc(oead.yaz0.decompress(util.get_game_file('Actor\\Pack\\' + file).read_bytes()))
        for small_file in sarc.get_files():
            if 'bgparamlist' in small_file.name:
                data_small_file = oead.aamp.ParameterIO.from_binary(small_file.data)
                for (name, other) in data_small_file.objects.items():
                    name: str = str(oead.aamp.NameTable.get_name(oead.aamp.get_default_name_table(), name.hash, 100, 0))
                    if not oead_to_normal(name) in all_params:
                        all_params[oead_to_normal(name)] = {}
                    all_params[oead_to_normal(name)][file] = {}
                    for param_name in other.params:
                        param_name: str = str(oead.aamp.NameTable.get_name(oead.aamp.get_default_name_table(), param_name.hash, 100, oead.aamp.Name(name).hash))
                        all_params[name][file][param_name] = oead_to_normal(other.params[param_name].v)
        
        print(f'Processed {file}')

    for file in os.listdir('TitleBG'):
        sarc = oead.Sarc(oead.yaz0.decompress(Path('TitleBG\\'+file).read_bytes()))
        for small_file in sarc.get_files():
            if 'bgparamlist' in small_file.name:
                data_small_file = oead.aamp.ParameterIO.from_binary(small_file.data)
                for (name, other) in data_small_file.objects.items():
                    name: str = str(oead.aamp.NameTable.get_name(oead.aamp.get_default_name_table(), name.hash, 100, 0))
                    if not oead_to_normal(name) in all_params:
                        all_params[oead_to_normal(name)] = {}
                    all_params[oead_to_normal(name)][file] = {}
                    for param_name in other.params:
                        param_name: str = str(oead.aamp.NameTable.get_name(oead.aamp.get_default_name_table(), param_name.hash, 100, oead.aamp.Name(name).hash))
                        all_params[name][file][param_name] = oead_to_normal(other.params[param_name].v)
        
        print(f'Processed {file}')

    for json_type_file in all_params:
        with open('json\\' + str(json_type_file) + '.json', 'w') as json_file:
            json_file.write(json.dumps(all_params[str(json_type_file)], indent = 2))
        
        print(f'Processed {json_type_file}')

create_jsons()