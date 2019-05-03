import bpy
import sys
from math import sqrt,pi,radians, sin, cos, tan, asin, degrees,acos
from mathutils import Vector,Matrix
sys.path.append("/root/Software/anaconda3/lib/python3.7/site-packages")

try :
    import openbabel
    import pybel
except:
    pass

from bpy.props import (
    EnumProperty,
    PointerProperty,
    StringProperty,
    BoolProperty,
    IntProperty,
    FloatProperty,
    )

from bpy.types import (
    Panel, 
    Operator,
    Menu,
    PropertyGroup,
    SpaceView3D,
    WindowManager,
    )

atom_data = {
    "Ac": {"color": [0.439216, 0.670588, 0.980392,0.9], "radius": 1.114285},
    "Ag": {"color": [0.752941, 0.752941, 0.752941,0.9], "radius": 0.914285},
    "Al": {"color": [0.74902, 0.65098, 0.65098,0.9], "radius": 0.714285},
    "Am": {"color": [0.329412, 0.360784, 0.94902,0.9], "radius": 1.0},
    "Ar": {"color": [0.501961, 0.819608, 0.890196,0.9], "radius": 0.4057145},
    "As": {"color": [0.741176, 0.501961, 0.890196,0.9], "radius": 0.657145},
    "Au": {"color": [1, 0.819608, 0.137255,0.9], "radius": 0.77143},
    "B": {"color": [1, 0.709804, 0.709804,0.9], "radius": 0.4857145},
    "Ba": {"color": [0, 0.788235, 0,0.9], "radius": 1.22857},
    "Be": {"color": [0.760784, 1, 0,0.9], "radius": 0.6},
    "Bi": {"color": [0.619608, 0.309804, 0.709804,0.9], "radius": 0.914285},
    "Br": {"color": [0.65098, 0.160784, 0.160784,0.9], "radius": 0.657145},
    "C": {"color": [0.564706, 0.564706, 0.564706,0.9], "radius": 0.4},
    "Ca": {"color": [0.239216, 1, 0,0.9], "radius": 1.02857},
    "Cd": {"color": [1, 0.85098, 0.560784,0.9], "radius": 0.885715},
    "Ce": {"color": [1, 1, 0.780392,0.9], "radius": 1.057145},
    "Cl": {"color": [0.121569, 0.941176, 0.121569,0.9], "radius": 0.57143},
    "Co": {"color": [0.941176, 0.564706, 0.627451,0.9], "radius": 0.77143},
    "Cr": {"color": [0.541176, 0.6, 0.780392,0.9], "radius": 0.8},
    "Cs": {"color": [0.341176, 0.0901961, 0.560784,0.9], "radius": 1.485715},
    "Cu": {"color": [0.784314, 0.501961, 0.2,0.9], "radius": 0.77143},
    "Dy": {"color": [0.121569, 1, 0.780392,0.9], "radius": 1.0},
    "Er": {"color": [0, 0.901961, 0.458824,0.9], "radius": 1.0},
    "Eu": {"color": [0.380392, 1, 0.780392,0.9], "radius": 1.057145},
    "F": {"color": [0.564706, 0.878431, 0.313725,0.9], "radius": 0.2857145},
    "Fe": {"color": [0.878431, 0.4, 0.2,0.9], "radius": 0.8},
    "Ga": {"color": [0.760784, 0.560784, 0.560784,0.9], "radius": 0.742855},
    "Gd": {"color": [0.270588, 1, 0.780392,0.9], "radius": 1.02857},
    "Ge": {"color": [0.4, 0.560784, 0.560784,0.9], "radius": 0.714285},
    "H": {"color": [1, 1, 1,0.9], "radius": 0.142857},
    "Hf": {"color": [0.301961, 0.760784, 1,0.9], "radius": 0.885715},
    "Hg": {"color": [0.721569, 0.721569, 0.815686,0.9], "radius": 0.857145},
    "Ho": {"color": [0, 1, 0.611765,0.9], "radius": 1.0},
    "I": {"color": [0.580392, 0, 0.580392,0.9], "radius": 0.8},
    "In": {"color": [0.65098, 0.458824, 0.45098,0.9], "radius": 0.885715},
    "Ir": {"color": [0.0901961, 0.329412, 0.529412,0.9], "radius": 0.77143},
    "K": {"color": [0.560784, 0.25098, 0.831373,0.9], "radius": 1.257145},
    "La": {"color": [0.439216, 0.831373, 1,0.9], "radius": 1.114285},
    "Li": {"color": [0.8, 0.501961, 1,0.9], "radius": 0.82857},
    "Lu": {"color": [0, 0.670588, 0.141176,0.9], "radius": 1.0},
    "Mg": {"color": [0.541176, 1, 0,0.9], "radius": 0.857145},
    "Mn": {"color": [0.611765, 0.478431, 0.780392,0.9], "radius": 0.8},
    "Mo": {"color": [0.329412, 0.709804, 0.709804,0.9], "radius": 0.82857},
    "N": {"color": [0.188235, 0.313725, 0.972549,0.9], "radius": 0.3714285},
    "Na": {"color": [0.670588, 0.360784, 0.94902,0.9], "radius": 1.02857},
    "Nb": {"color": [0.45098, 0.760784, 0.788235,0.9], "radius": 0.82857},
    "Nd": {"color": [0.780392, 1, 0.780392,0.9], "radius": 1.057145},
    "Ni": {"color": [0.313725, 0.815686, 0.313725,0.9], "radius": 0.77143},
    "Np": {"color": [0, 0.501961, 1,0.9], "radius": 1.0},
    "O": {"color": [1, 0.0509804, 0.0509804,0.9], "radius": 0.342857},
    "Os": {"color": [0.14902, 0.4, 0.588235,0.9], "radius": 0.742855},
    "P": {"color": [1, 0.501961, 0,0.9], "radius": 0.57143},
    "Pa": {"color": [0, 0.631373, 1,0.9], "radius": 1.02857},
    "Pb": {"color": [0.341176, 0.34902, 0.380392,0.9], "radius": 1.02857},
    "Pd": {"color": [0, 0.411765, 0.521569,0.9], "radius": 0.8},
    "Pm": {"color": [0.639216, 1, 0.780392,0.9], "radius": 1.057145},
    "Po": {"color": [0.670588, 0.360784, 0,0.9], "radius": 1.085715},
    "Pr": {"color": [0.85098, 1, 0.780392,0.9], "radius": 1.057145},
    "Pt": {"color": [0.815686, 0.815686, 0.878431,0.9], "radius": 0.77143},
    "Pu": {"color": [0, 0.419608, 1,0.9], "radius": 1.0},
    "Ra": {"color": [0, 0.490196, 0,0.9], "radius": 1.22857},
    "Rb": {"color": [0.439216, 0.180392, 0.690196,0.9], "radius": 1.342855},
    "Re": {"color": [0.14902, 0.490196, 0.670588,0.9], "radius": 0.77143},
    "Rh": {"color": [0.0392157, 0.490196, 0.54902,0.9], "radius": 0.77143},
    "Ru": {"color": [0.141176, 0.560784, 0.560784,0.9], "radius": 0.742855},
    "S": {"color": [1, 1, 0.188235,0.9], "radius": 0.57143},
    "Sb": {"color": [0.619608, 0.388235, 0.709804,0.9], "radius": 0.82857},
    "Sc": {"color": [0.901961, 0.901961, 0.901961,0.9], "radius": 0.914285},
    "Se": {"color": [1, 0.631373, 0,0.9], "radius": 0.657145},
    "Si": {"color": [0.941176, 0.784314, 0.627451,0.9], "radius": 0.62857},
    "Sm": {"color": [0.560784, 1, 0.780392,0.9], "radius": 1.057145},
    "Sn": {"color": [0.4, 0.501961, 0.501961,0.9], "radius": 0.82857},
    "Sr": {"color": [0, 1, 0,0.9], "radius": 1.142855},
    "Ta": {"color": [0.301961, 0.65098, 1,0.9], "radius": 0.82857},
    "Tb": {"color": [0.188235, 1, 0.780392,0.9], "radius": 1.0},
    "Tc": {"color": [0.231373, 0.619608, 0.619608,0.9], "radius": 0.77143},
    "Te": {"color": [0.831373, 0.478431, 0,0.9], "radius": 0.8},
    "Th": {"color": [0, 0.729412, 1,0.9], "radius": 1.02857},
    "Ti": {"color": [0.74902, 0.760784, 0.780392,0.9], "radius": 0.8},
    "Tl": {"color": [0.65098, 0.329412, 0.301961,0.9], "radius": 1.085715},
    "Tm": {"color": [0, 0.831373, 0.321569,0.9], "radius": 1.0},
    "U": {"color": [0, 0.560784, 1,0.9], "radius": 1.0},
    "V": {"color": [0.65098, 0.65098, 0.670588,0.9], "radius": 0.77143},
    "W": {"color": [0.129412, 0.580392, 0.839216,0.9], "radius": 0.77143},
    "Y": {"color": [0.580392, 1, 1,0.9], "radius": 1.02857},
    "Yb": {"color": [0, 0.74902, 0.219608,0.9], "radius": 1.0},
    "Zn": {"color": [0.490196, 0.501961, 0.690196,0.9], "radius": 0.77143},
    "Zr": {"color": [0.580392, 0.878431, 0.878431,0.9], "radius": 0.885715},
    "undefined": {"color": [0, 0, 0,0.9], "radius": 0.405},
    "bond": {"color": [0.05, 0.05, 0.05,0.9], "radius": 0.103}
}



class MOLECULE_PROPERTY(PropertyGroup):
    smile_format : StringProperty(
        name = "Smile",
        description="smile format",
        default="CCO"
        )

class LEARNBGAME_PT_MOLECULE(Panel):
    bl_label = "Molecule"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "chem3D"




    def draw(self,context):
        layout = self.layout
        scene = context.scene

        molecule = scene.molecule
        row = layout.row()
        row.prop(
            molecule,
            "smile_format",
            )
        row.operator(MOLECULE_ADD.bl_idname,text="add",icon="ADD")

class MOLECULE_ADD(Operator):
    bl_idname = "molecule.add"
    bl_label = "Molecule+"

    def execute(self,context):
        self.draw_molecule(context,center=(0, 0, 0), show_bonds=True, join=True)

        return {'FINISHED'}

    def draw_molecule(self,context,center=(0, 0, 0), show_bonds=True, join=True):

        smile_text = context.scene.molecule.smile_format
        molecule = pybel.readstring("smi", smile_text)
        molecule.make3D()

        shapes = []

        bpy.ops.mesh.primitive_uv_sphere_add()
        sphere = bpy.context.object

        # Initialize bond material if it's going to be used.
        if show_bonds:
            bond_material = bpy.data.materials.new(name='bond')
            bond_material.use_nodes = True
            bond_material.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = atom_data['bond']['color']
            bond_material.node_tree.nodes["Principled BSDF"].inputs['Metallic'].default_value = 1
            bond_material.node_tree.nodes["Principled BSDF"].inputs['Roughness'].default_value = 0
            bpy.ops.mesh.primitive_cylinder_add()
            cylinder = bpy.context.object
            cylinder.data.materials.append(bond_material)



        for atom in molecule.atoms:
            element = atom.type
            if element not in atom_data:
                element = 'undefined'

            if element not in bpy.data.materials:
                key = element
                atom_material = bpy.data.materials.new(name=key)
                atom_material.use_nodes = True
                atom_material.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = atom_data[key]['color']
                atom_material.node_tree.nodes["Principled BSDF"].inputs['Metallic'].default_value = 1
                atom_material.node_tree.nodes["Principled BSDF"].inputs['Roughness'].default_value = 0

            atom_sphere = sphere.copy()
            atom_sphere.data = sphere.data.copy()
            atom_sphere.location = [l + c for l, c in
                                    zip(atom.coords, center)]
            scale = 1 if show_bonds else 2.5
            atom_sphere.dimensions = [atom_data[element]['radius'] *scale * 2] * 3
            atom_sphere.data.materials.append(bpy.data.materials[element])
            bpy.context.scene.collection.objects.link(atom_sphere)
            shapes.append(atom_sphere)

        for bond in (openbabel.OBMolBondIter(molecule.OBMol) if show_bonds else []):
            start = molecule.atoms[bond.GetBeginAtom().GetIndex()].coords
            end = molecule.atoms[bond.GetEndAtom().GetIndex()].coords
            diff = [c2 - c1 for c2, c1 in zip(start, end)]
            cent = [(c2 + c1) / 2 for c2, c1 in zip(start, end)]
            mag = sum([(c2 - c1) ** 2 for c1, c2 in zip(start, end)]) ** 0.5

            v_axis = Vector(diff).normalized()
            v_obj = Vector((0, 0, 1))
            v_rot = v_obj.cross(v_axis)

            # This check prevents gimbal lock (ie. weird behavior when v_axis is
            # close to (0, 0, 1))
            if v_rot.length > 0.01:
                v_rot = v_rot.normalized()
                axis_angle = [acos(v_obj.dot(v_axis))] + list(v_rot)
            else:
                v_rot = Vector((1, 0, 0))
                axis_angle = [0] * 4
            order = bond.GetBondOrder()
            if order not in range(1, 4):
                sys.stderr.write("Improper number of bonds! Defaulting to 1.\n")
                bond.GetBondOrder = 1

            if order == 1:
                trans = [[0] * 3]
            elif order == 2:
                trans = [[1.4 * atom_data['bond']['radius'] * x for x in v_rot],
                         [-1.4 * atom_data['bond']['radius'] * x for x in v_rot]]
            elif order == 3:
                trans = [[0] * 3,
                         [2.2 * atom_data['bond']['radius'] * x for x in v_rot],
                         [-2.2 * atom_data['bond']['radius'] * x for x in v_rot]]

            for i in range(order):
                bond_cylinder = cylinder.copy()
                bond_cylinder.data = cylinder.data.copy()
                bond_cylinder.dimensions = [atom_data['bond']['radius'] * scale *2] * 2 + [mag]
                bond_cylinder.location = [c + scale * v for c,v in zip(cent, trans[i])]
                bond_cylinder.rotation_mode = 'AXIS_ANGLE'
                bond_cylinder.rotation_axis_angle = axis_angle
                bpy.context.scene.collection.objects.link(bond_cylinder)
                shapes.append(bond_cylinder)

        sphere.select_set(True)
        if show_bonds:
            cylinder.select_set(True)
        bpy.ops.object.delete()

        for shape in shapes:
            shape.select_set(True)
        bpy.context.view_layer.objects.active = shapes[0]
        bpy.ops.object.shade_smooth()
        if join:
            bpy.ops.object.join()

        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        bpy.context.scene.update()
        obj = bpy.context.selected_objects
        obj[0].name = smile_text
        obj[0].location = bpy.context.scene.cursor.location

        return {'FINISHED'}


def register():
    bpy.utils.register_class(LEARNBGAME_PT_MOLECULE)
    bpy.utils.register_class(MOLECULE_PROPERTY)
    bpy.utils.register_class(MOLECULE_ADD)
    bpy.types.Scene.molecule = PointerProperty(type=MOLECULE_PROPERTY)

def unregister():
    bpy.utils.unregister_class(LEARNBGAME_PT_MOLECULE)
    bpy.utils.unregister_class(MOLECULE_PROPERTY)
    bpy.utils.unregister_class(MOLECULE_ADD)

if __name__ == '__main__':
    register()



