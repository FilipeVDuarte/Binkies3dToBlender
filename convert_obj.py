import json
import os

# ── Config ──────────────────────────────────────────
geometry_json  = 'geometry.geometries.json'
full_json      = 'geometry.json'
obj_path       = 'output_model.obj'
mtl_path       = 'output_model.mtl'
scale          = 1000.0
mirror_axis    = "x"

# Opcoes disponiveis: "Cosmic Orange", "Deep Blue", "Silver"
# Use None para materiais base sem cor
COLOR_OPTION   = "Cosmic Orange"
# ────────────────────────────────────────────────────


# Mapeamento explicito: node_name -> sufixo do material
# {COLOR} sera substituido pela keyword da cor (Orange, Blue, Silver...)
NODE_MATERIAL_MAP = {
    # Partes coloridas do aparelho
    "Back_Panel":               "COLOUR_{COLOR}_Backpanel",
    "Back_Cam_Base":            "COLOUR_{COLOR}_Backpanel",
    "Back_Cam_Black":           "IBL_BASE_Black",
    "Back_Logo":                "IBL_COLOUR_{COLOR}_Apple",
    "Back_Panel_detail":        "COLOUR_{COLOR}_Backpanel",

    # Camera traseira - materiais base (nao mudam com a cor)
    "Back_Cam_Lens":            "IBL_BASE_Cam_Lens01",
    "Back_Cam_Lens_02":         "IBL_BASE_Cam_Lens02",
    "Back_Cam_Lens_03":         "IBL_BASE_Cam_Lens03",
    "Back_Cam_Lens_Outer":      "IBL_BASE_Cam_Lens_Outer",
    "Back_Cam_Edge":            "IBL_BASE_Chrome_Dark",
    "Back_Cam_Edge_black":      "IBL_BASE_Glass_Black",
    "Back_Cam_Glass":           "IBL_BASE_Glass",
    "Back_IR_Glass":            "IBL_BASE_Glass",

    # Flash
    "Back_Flash_Glass":         "BASE_Flash_Glass",
    "Back_Flash_Glass_Matte":   "BASE_Flash_Glass",
    "Back_Flash_Base":          "IBL_BASE_Flash_Base",
    "Back_Flash_Light":         "IBL_BASE_Flash_Light",
    "Back_Flash_Ref":           "IBL_BASE_Flash_Ref",

    # Botoes laterais
    "Side_Button_Detail":       "IBL_COLOUR_{COLOR}_Side_Button_Detail",
    "Side_Button_Detail_Border":"IBL_COLOUR_{COLOR}_Button_Detail_Border",
    "Side_buttons":             "IBL_COLOUR_{COLOR}_Side_Panel",
    "Side_Panel_Speakers":      "IBL_COLOUR_{COLOR}_Side_Panel",
    "Side_Panel_eSIM":          "IBL_COLOUR_{COLOR}_Side_Panel",

    # Outros
    "Back_Mic":                 "IBL_BASE_Chrome_Dark",
    "Gradient":                 "IBL_BASE_Flash_Ref_Gradient",
    "Front_Sensor":             "IBL_BASE_Sensor",
    "Holes":                    "IBL_BASE_Chrome_Dark",
    "Front_Speaker":            "IBL_BASE_Speakers",
    "Front_Screen":             "IBL_COLOUR_{COLOR}_Screen",
    "Screws_Aniso_01":          "IBL_COLOUR_{COLOR}_Screws",
    "Screws_Aniso_02":          "IBL_COLOUR_{COLOR}_Aniso_02",
}


def normalize_color(r, g, b):
    return r / 255.0, g / 255.0, b / 255.0


def get_color_keyword(option_name):
    if not option_name:
        return None
    keywords = ['Orange', 'Blue', 'Silver', 'Black', 'Gold', 'White', 'Red', 'Green', 'Purple']
    for kw in keywords:
        if kw.lower() in option_name.lower():
            return kw
    return None


def find_material_by_name(name_pattern, materials):
    """Busca material pelo nome exato (case-insensitive)."""
    name_clean = name_pattern.replace(' ', '_').lower()
    for mat in materials:
        if mat['name'].replace(' ', '_').lower() == name_clean:
            return mat
    # Tentativa parcial se exato falhar
    for mat in materials:
        if name_clean in mat['name'].replace(' ', '_').lower():
            return mat
    return None


def find_material_auto(node_name, materials, color_keyword):
    """Fallback automatico por matching de nome."""
    node_key = node_name.replace('_', '').lower()
    color_candidates = []
    base_candidates = []

    for mat in materials:
        mat_key = mat['name'].replace('_', '').replace(' ', '').lower()
        has_color = color_keyword and color_keyword.lower() in mat_key

        name_match = False
        parts = node_name.lower().split('_')
        for part in parts:
            if len(part) >= 5 and part in mat_key:
                name_match = True
                break
        if node_key in mat_key:
            name_match = True

        if name_match:
            if has_color:
                color_candidates.append(mat)
            else:
                base_candidates.append(mat)

    if color_candidates:
        return color_candidates[0]
    if base_candidates:
        return base_candidates[0]
    return materials[0]


def resolve_material(node_name, materials, color_keyword):
    """Resolve material: override explicito primeiro, depois auto."""
    if node_name in NODE_MATERIAL_MAP:
        pattern = NODE_MATERIAL_MAP[node_name]
        if '{COLOR}' in pattern:
            mat_name = pattern.replace('{COLOR}', color_keyword or 'Base')
        else:
            mat_name = pattern
        mat = find_material_by_name(mat_name, materials)
        if mat:
            return mat, "override"
        # Se nao encontrou o override, cai no auto
    mat = find_material_auto(node_name, materials, color_keyword)
    return mat, "auto"


def build_mtl(materials_used, mtl_path):
    written = set()
    with open(mtl_path, 'w') as f:
        for mat in materials_used:
            if mat['name'] in written:
                continue
            written.add(mat['name'])
            name = mat['name'].replace(' ', '_')
            colors = mat.get('colors', {})
            values = mat.get('values', {})

            f.write(f"newmtl {name}\n")

            base = colors.get('baseColor', {'r': 200, 'g': 200, 'b': 200})
            r, g, b = normalize_color(base['r'], base['g'], base['b'])
            f.write(f"Kd {r:.4f} {g:.4f} {b:.4f}\n")
            f.write(f"Ka {r:.4f} {g:.4f} {b:.4f}\n")

            spec = colors.get('specularity', {'r': 0, 'g': 0, 'b': 0})
            sr, sg, sb = normalize_color(spec['r'], spec['g'], spec['b'])
            f.write(f"Ks {sr:.4f} {sg:.4f} {sb:.4f}\n")

            roughness = values.get('roughness', 0.5)
            ns = max(0.0, (1.0 - roughness) * 1000.0)
            f.write(f"Ns {ns:.2f}\n")

            opacity = values.get('opacity', 1.0)
            f.write(f"d {opacity:.4f}\n")

            metallic = values.get('metallic', 0)
            illum = 3 if metallic > 0.5 else 2
            f.write(f"illum {illum}\n\n")

    print(f"MTL criado: {mtl_path} ({len(written)} materiais)")


def create_obj(geometry_json, full_json, obj_path, mtl_path,
               color_option=None, scale=1000.0, mirror_axis="x"):

    with open(geometry_json, 'r') as f:
        geo_data = json.load(f)

    nodes = []
    materials = []
    if os.path.exists(full_json):
        with open(full_json, 'r') as f:
            full = json.load(f)
        nodes = full.get('nodes', [])
        materials = full.get('materials', [])

    color_keyword = get_color_keyword(color_option)
    print(f"Opcao de cor: {color_option or 'Nenhuma'} | Keyword: {color_keyword or 'N/A'}\n")

    mtl_name = os.path.basename(mtl_path)
    obj_lines = [f"# Gerado por convert_obj.py", f"# Opcao: {color_option or 'base'}"]
    if materials:
        obj_lines.append(f"mtllib {mtl_name}")

    vertex_offset = 1
    materials_used = []
    mapping_log = []

    for obj_idx, geo in enumerate(geo_data):
        positions = geo['positions'][0]
        indices = geo['indices']

        node_name = nodes[obj_idx]['name'] if obj_idx < len(nodes) else f"object_{obj_idx}"
        obj_lines.append(f"\no {node_name}")

        if materials:
            mat, source = resolve_material(node_name, materials, color_keyword)
            mat_name = mat['name'].replace(' ', '_')
            obj_lines.append(f"usemtl {mat_name}")
            materials_used.append(mat)
            mapping_log.append((node_name, mat['name'], source))

        # Vertices
        position_keys = sorted(positions.keys(), key=int)
        vertices = []
        for i in range(len(position_keys) // 3):
            x = float(positions[position_keys[i * 3]]) * scale
            y = float(positions[position_keys[i * 3 + 1]]) * scale
            z = float(positions[position_keys[i * 3 + 2]]) * scale

            if mirror_axis and mirror_axis.lower() == "x":
                x *= -1
            elif mirror_axis and mirror_axis.lower() == "y":
                y *= -1
            elif mirror_axis and mirror_axis.lower() == "z":
                z *= -1

            vertices.append((x, y, z))
            obj_lines.append(f"v {x:.6f} {y:.6f} {z:.6f}")

        # Faces
        index_keys = sorted(indices.keys(), key=int)
        for i in range(0, len(index_keys), 3):
            i0 = indices[index_keys[i]] + vertex_offset
            i1 = indices[index_keys[i + 1]] + vertex_offset
            i2 = indices[index_keys[i + 2]] + vertex_offset
            if mirror_axis:
                obj_lines.append(f"f {i1} {i0} {i2}")
            else:
                obj_lines.append(f"f {i0} {i1} {i2}")

        vertex_offset += len(vertices)

    with open(obj_path, 'w') as f:
        f.write("\n".join(obj_lines))

    if materials_used:
        build_mtl(materials_used, mtl_path)

    print(f"OBJ criado: {obj_path}")
    print(f"Total de objetos: {len(geo_data)} | Total de vertices: {vertex_offset - 1}")

    print("\n=== Mapeamento node -> material ===")
    for node_name, mat_name, source in mapping_log:
        tag = "[override]" if source == "override" else "[auto]   "
        print(f"  {tag} {node_name:35s} -> {mat_name}")


create_obj(geometry_json, full_json, obj_path, mtl_path,
           color_option=COLOR_OPTION, scale=scale, mirror_axis=mirror_axis)
