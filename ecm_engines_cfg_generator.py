import part_data
from string import Template

tree_ecm_engines_header = """
//****************************************************************************************
//  ENTRY COST MODIFIERS
//	These are the engine configs
//
//	DO NOT EDIT THIS FILE DIRECTLY!!!
//	This file is generated from RP-0 Parts Browser
//
//****************************************************************************************

@ENTRYCOSTMODS:FOR[xxxRP-0]
{
"""

module_part_config_template = Template("    ${name} = ${ecm}\n")
tree_ecm_engines_footer = "}"

def generate_ecm_engines(parts):
    ecm_configs = ""
    for part in parts:
        if part['name'] is not None and len(part['name']) > 0:
            if part['mod'] == 'Engine_Config' and not part['orphan']:
                ecm_configs += module_part_config_template.substitute(name=part['name'], ecm=part['entry_cost_mods'])
    text_file = open("output/ECM-Engines.cfg", "w")
    text_file.write(tree_ecm_engines_header)
    text_file.write(ecm_configs)
    text_file.write(tree_ecm_engines_footer)
    text_file.close()
        