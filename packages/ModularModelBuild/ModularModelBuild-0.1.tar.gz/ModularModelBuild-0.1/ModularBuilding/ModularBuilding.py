"""
Author: Mehmet Baris Batukan
Date: 2023-12-02
Description: This file contains the main class for the modular building.
Units: m, kN, C
"""

import os, sys, importlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import openseespy.opensees as ops
import opsvis as opsv
import utils.helper as helper


# Material properties
class steel_column(object):
    Fy = 350e3
    YoungModulus = 2e8
    ShearModulus = 77e6
    McMy = 1.05
    Lambda_UQ = 0.0
    ThetaP_UQ = 0.0
    ThetaPc_UQ = 0.0
    R0 = 20
    cR1 = 0.925
    cR2 = 0.15
    b = 0.10
    a2 = 1.0
    a1 = a2 * (Fy / YoungModulus)
    a4 = 1.0
    a3 = a4 * (Fy / YoungModulus)


# Material properties
class steel_beam(object):
    Fy = 345e3
    YoungModulus = 2e8
    ShearModulus = 77e6
    McMy = 1.11
    Lambda_UQ = 0.0
    ThetaP_UQ = 0.0
    ThetaPc_UQ = 0.0


# Material properties
class steel_brace(object):
    Fy = 350e3
    YoungModulus = 2e8
    ShearModulus = 77e6
    R0 = 20
    cR1 = 0.925
    cR2 = 0.15
    b = 0.01
    a2 = 1.0
    a1 = a2 * (Fy / YoungModulus)
    a4 = 1.0
    a3 = a4 * (Fy / YoungModulus)
    imperfection = 0.002
    fatigue_E0 = 0.01


class steel_plate(object):
    Fy = 200e3
    YoungModulus = 2e8
    ShearModulus = 77e6
    McMy = 1.05


class design(object):
    def __init__(self, name=None, directory=None):
        if name is None:
            raise ValueError(f"Please provide a name for the analysis.")
        self.name = name
        self.formatted_name = self.name.lower().replace(" ", "_")

        if directory is not None:
            if not os.path.exists(directory):
                raise ValueError(f"The directory {directory} does not exist.")
        else:
            raise ValueError(f"Please provide a path to read files.")

        self.directory = directory

        print(f"Design class is not implemented yet...")


class analyze(object):
    def __init__(self, name=None, directory=None):
        if name is None:
            raise ValueError(f"Please provide a name for the analysis.")
        self.name = name
        self.formatted_name = self.name.lower().replace(" ", "_")

        if directory is not None:
            if not os.path.exists(directory):
                raise ValueError(f"The directory {directory} does not exist.")
        else:
            raise ValueError(f"Please provide a path to read files.")

        self.directory = directory

    def initialize_ops(self, **kwargs) -> None:
        ops.wipe()
        ops.model("basic", "-ndm", 3, "-ndf", 6)
        print("OpenSeesPy initialized.")
        print("BE AWARE! Only following units (m, kN, C, etc.) are used!\n")
        return None

    def assign_node(self, verbose=False, show_plot=False, **kwargs) -> None:
        with open(f"{self.directory}/{self.formatted_name}_global_nodes.py", "r") as f:
            exec(f.read())

        if verbose:
            node_tags = ops.getNodeTags()
            print(f"{len(node_tags)} global nodes are assigned.")

        if show_plot:
            opsv.plot_model()
            plt.show()

        return None

    def declare_global_var(self, verbose=False, **kwargs) -> None:
        sys.path.append(self.directory)
        if "global_vars" in sys.modules:
            del sys.modules["global_vars"]
        self.global_vars = importlib.import_module(f"{self.formatted_name}_global_vars")

        if verbose:
            print("Global variables are declared.")
        return None

    def assign_geo_transf(self, verbose=False, **kwargs) -> None:
        with open(f"{self.directory}/{self.formatted_name}_geo_transfs.py", "r") as f:
            exec(f.read())

        if verbose:
            print("Geometric transformation is assigned.")
        return None

    def assign_section_material(self, verbose=False, **kwargs) -> None:
        with open(
            f"{self.directory}/{self.formatted_name}_sections_materials.py", "r"
        ) as f:
            exec(f.read())

        if verbose:
            print("Sections and materials are assigned.")
        return None

    def wipe_analysis(self, **kwargs) -> None:
        ops.wipeAnalysis()
        print("Analysis is wiped.")
        return None

    def wipe_model(self, **kwargs) -> None:
        ops.wipe()
        print("Model is wiped.")
        return None

    def start_timer(self, **kwargs) -> None:
        ops.start()
        return None

    def stop_timer(self, **kwargs) -> None:
        ops.stop()
        return None


class generate(object):
    def __init__(self, name=None, directory=None):
        if name is None:
            raise ValueError(f"Please provide a name for the analysis.")

        self.name = name
        self.formatted_name = self.name.lower().replace(" ", "_")

        if directory is not None:
            if not os.path.exists(directory):
                os.makedirs(directory)
        else:
            raise ValueError(f"Please provide a path to save files.")

        self.directory = directory

        self.df_steel_W = pd.read_excel(
            f"./data/SteelSections_W_HSS.xlsx",
            sheet_name="W",
        ).set_index("Dsg")

        self.df_steel_HSS = pd.read_excel(
            f"./data/SteelSections_W_HSS.xlsx",
            sheet_name="HSS-G40",
        ).set_index("Dsg")

    def layout(self, modules: dict, show_plot: bool = False, **kwargs):
        positions = {}
        corners = {}
        brace_positions = {}
        x, y = 0.0, 0.0  # Starting position

        for module_number, module in modules.items():
            if module["location"] == "south-west":
                x += module["west-spacing"]
                y += module["south-spacing"]
            else:
                # Get the module number from the location
                relative_module_number = int(module["location"].split("-")[1])
                relative_module = modules[relative_module_number]
                if "north" in module["location"]:
                    x = positions[relative_module_number][0]
                    y = (
                        positions[relative_module_number][1]
                        + relative_module["y-dir"]
                        + module["south-spacing"]
                    )
                elif "east" in module["location"]:
                    x = (
                        positions[relative_module_number][0]
                        + relative_module["x-dir"]
                        + module["west-spacing"]
                    )
                    y = positions[relative_module_number][1]

            positions[module_number] = (x, y)

            if module.get("brace"):
                brace_positions[module_number] = []
                for brace in module["brace"]:
                    side, range_, type_brace = brace

                    if range_ == "entire":
                        if side in ["south-side"]:
                            start_x, end_x = 0.0, module["x-dir"]
                            start_y, end_y = 0.0, 0.0
                        elif side in ["north-side"]:
                            start_x, end_x = 0.0, module["x-dir"]
                            start_y, end_y = module["y-dir"], module["y-dir"]
                        elif side in ["east-side"]:
                            start_y, end_y = 0.0, module["y-dir"]
                            start_x, end_x = module["x-dir"], module["x-dir"]
                        elif side in ["west-side"]:
                            start_y, end_y = 0.0, module["y-dir"]
                            start_x, end_x = 0.0, 0.0
                    else:
                        start, end = map(float, range_.split("-"))
                        if side in ["south-side"]:
                            start_x, end_x = start, end
                            start_y, end_y = 0.0, 0.0
                        elif side in ["north-side"]:
                            start_x, end_x = start, end
                            start_y, end_y = module["y-dir"], module["y-dir"]
                        elif side in ["east-side"]:
                            start_y, end_y = start, end
                            start_x, end_x = module["x-dir"], module["x-dir"]
                        elif side in ["west-side"]:
                            start_y, end_y = start, end
                            start_x, end_x = 0.0, 0.0

                    # Calculate the global start and end points
                    global_start_x = start_x + x
                    global_end_x = end_x + x
                    global_start_y = start_y + y
                    global_end_y = end_y + y

                    # Calculate the middle point if the type is "Chevron"
                    if type_brace == "Chevron":
                        middle_x = (start_x + end_x) / 2
                        middle_y = (start_y + end_y) / 2
                        global_middle_x = (global_start_x + global_end_x) / 2
                        global_middle_y = (global_start_y + global_end_y) / 2
                        brace_positions[module_number].append(
                            (
                                (side, type_brace),
                                (
                                    "relative",
                                    (start_x, start_y),
                                    (middle_x, middle_y),
                                    (end_x, end_y),
                                ),
                                (
                                    "global",
                                    (global_start_x, global_start_y),
                                    (global_middle_x, global_middle_y),
                                    (global_end_x, global_end_y),
                                ),
                            )
                        )
                    else:
                        brace_positions[module_number].append(
                            (
                                (side, type_brace),
                                ("relative", (start_x, start_y), (end_x, end_y)),
                                (
                                    "global",
                                    (global_start_x, global_start_y),
                                    (global_end_x, global_end_y),
                                ),
                            )
                        )

            else:
                brace_positions[module_number] = None

            if module.get("brace"):
                # Calculate the four corners of the module
                corner = [
                    (x, y),
                    (x + module["x-dir"], y),
                    (x + module["x-dir"], y + module["y-dir"]),
                    (x, y + module["y-dir"]),
                    (global_start_x, global_start_y),
                    (global_end_x, global_end_y),
                ]
            else:
                # Calculate the four corners of the module
                corner = [
                    (x, y),
                    (x + module["x-dir"], y),
                    (x + module["x-dir"], y + module["y-dir"]),
                    (x, y + module["y-dir"]),
                ]

            corners[module_number] = {"corners": corner}

        self.df_module_coords = pd.concat(
            [
                pd.DataFrame(value["corners"], columns=["X", "Y"])
                .assign(ID=key)
                .drop_duplicates()
                for key, value in corners.items()
            ]
        )

        # Round 'X' and 'Y' values to 6 significant figures
        self.df_module_coords["X"] = self.df_module_coords["X"].round(6)
        self.df_module_coords["Y"] = self.df_module_coords["Y"].round(6)

        self.df_module_coords = (
            self.df_module_coords.groupby("ID")
            .agg({"X": list, "Y": list})
            .reset_index()
        )

        data = []

        for module_number, brace in brace_positions.items():
            if brace:
                for (side, type_brace), relative_coords, global_coords in brace:
                    data.append(
                        {
                            "ID": module_number,
                            "X": global_coords[2][0],
                            "Y": global_coords[2][1],
                        }
                    )

        self.df_module_mid_nodes = pd.DataFrame(data)
        self.df_module_mid_nodes["X"] = self.df_module_mid_nodes["X"].round(6)
        self.df_module_mid_nodes["Y"] = self.df_module_mid_nodes["Y"].round(6)

        unique_x_no_mid = np.unique(self.df_module_coords["X"].explode().astype(float))
        unique_y_no_mid = np.unique(self.df_module_coords["Y"].explode().astype(float))

        unique_x = np.unique(
            pd.concat(
                [
                    self.df_module_coords["X"].explode().astype(float),
                    self.df_module_mid_nodes["X"],
                ]
            )
        )

        unique_y = np.unique(
            pd.concat(
                [
                    self.df_module_coords["Y"].explode().astype(float),
                    self.df_module_mid_nodes["Y"],
                ]
            )
        )

        self.df_grid_x = pd.DataFrame(
            unique_x, columns=["X"], index=np.arange(11, len(unique_x) + 11)
        )
        self.df_grid_y = pd.DataFrame(
            unique_y, columns=["Y"], index=np.arange(11, len(unique_y) + 11)
        )

        self.df_nodes = pd.DataFrame(
            np.column_stack(
                (
                    np.hstack(
                        (self.df_module_coords.X.explode(), self.df_module_mid_nodes.X)
                    ),
                    np.hstack(
                        (self.df_module_coords.Y.explode(), self.df_module_mid_nodes.Y)
                    ),
                )
            ),
            columns=["X", "Y"],
        ).drop_duplicates(subset=["X", "Y"])

        self.df_nodes["X_ID"] = self.df_nodes["X"].map(
            self.df_grid_x.reset_index().set_index("X")["index"]
        )
        self.df_nodes["Y_ID"] = self.df_nodes["Y"].map(
            self.df_grid_y.reset_index().set_index("Y")["index"]
        )

        self.df_module_mid_nodes["X_ID"] = self.df_module_mid_nodes["X"].map(
            self.df_grid_x.reset_index().set_index("X")["index"]
        )
        self.df_module_mid_nodes["Y_ID"] = self.df_module_mid_nodes["Y"].map(
            self.df_grid_y.reset_index().set_index("Y")["index"]
        )

        if show_plot:
            fig, ax = self.__plot_module_2D(
                positions,
                modules,
                brace_positions,
                corners,
                unique_x_no_mid,
                unique_y_no_mid,
            )
            fig.show()

        return None

    def height(
        self,
        height_array=None,
        unit_typ=None,
        unit_first=None,
        vert_con_typ=None,
        vert_con_first=0.0,
        show_plot=False,
        **kwargs,
    ) -> None:
        num_of_story = kwargs["num_of_story"]

        if isinstance(height_array, np.ndarray):
            if len(height_array) != 2 * num_of_story + 1:
                raise ValueError(
                    f"Please provide a height array having length of 2 * {num_of_story} + 1  = {2*num_of_story+1}."
                )
        elif isinstance(height_array, list):
            height_array = np.array(height_array)
            if len(height_array) != 2 * num_of_story + 1:
                raise ValueError(
                    f"Please provide a height array having length of 2 * {num_of_story} + 1  = {2*num_of_story+1}."
                )
        else:
            if (
                unit_typ is None
                or unit_first is None
                or vert_con_typ is None
                or vert_con_first is None
            ):
                raise ValueError(
                    f"Please provide the following kwargs -> unit_typ, unit_first, vert_con_typ, and vert_con_first."
                )
            arr_story = np.arange(1, num_of_story + 1, 1)
            sh_1, sh_typ = vert_con_first + unit_typ, vert_con_typ + unit_first

            story_height = np.empty(num_of_story + 1)
            for i in range(num_of_story + 1):
                if i == 0:
                    story_height[i] = 0
                elif i == 1:
                    story_height[i] = sh_1
                else:
                    story_height[i] = story_height[i - 1] + sh_typ

            height_array = np.empty(2 * len(story_height) - 1)
            for i in range(len(arr_story) * 2 + 1):
                if i == 0:
                    height_array[i] = 0.0
                if i == 1:
                    height_array[i] = vert_con_first
                if i % 2 == 0 and i != 0:
                    height_array[i] = story_height[int(i / 2)]
                if i % 2 == 1 and i != 1:
                    height_array[i] = height_array[i - 1] + vert_con_typ

            if vert_con_first == 0.0:
                height_array = np.delete(height_array, 0)

        height_array_id = [str(item + 10) for item in range(1, len(height_array) + 1)]

        self.df_height = pd.DataFrame(
            np.column_stack((height_array - vert_con_first, height_array_id)),
            columns=["Z", "ID"],
        ).astype({"Z": float, "ID": int})

        self.height_building = self.df_height.Z.max()
        print(f"Height of the building is {self.height_building:.4f} m.")

        if show_plot:
            raise NotImplementedError("Plotting is not implemented yet.")
        return None

    def node(self, verbose=False, show_plot=False, **kwargs) -> None:
        self.df_nodes_height = pd.DataFrame()

        for row in self.df_height.iterrows():
            temp_df = self.df_nodes.copy()
            temp_df["Z"] = row[1]["Z"]
            temp_df["Z_ID"] = row[1]["ID"].astype(int)
            self.df_nodes_height = pd.concat([self.df_nodes_height, temp_df])

        self.df_nodes_height = self.df_nodes_height.reset_index(drop=True)
        nodes_command = [
            f"ops.node({row['Z_ID']}{row['X_ID']}{row['Y_ID']}, {row['X']}, {row['Y']}, {row['Z']})"
            for _, row in self.df_nodes_height.iterrows()
        ]

        helper.save_list_to_file(
            self.directory, f"{self.formatted_name}_global_nodes.py", nodes_command
        )

        if verbose:
            print(f"In total, {len(self.df_nodes_height)} nodes are created and saved.")

        if show_plot:
            self.__plot_nodes_3D()
            plt.show()

        return None

    def section_material(self, verbose=False, **kwargs) -> None:
        sections_materials = [
            "mat_tag_pinned = 1",
            "mat_tag_rigid = 2",
            "mat_tag_brace_steel_no_fatigue = 3",
            "mat_tag_brace_steel = 4",
            "mat_tag_torsion = 5",
            "mat_tag_VC_steel = 6",
            " ",
            "ops.uniaxialMaterial('Elastic', mat_tag_pinned, 1e-9)",
            "ops.uniaxialMaterial('Elastic', mat_tag_rigid, 1e20)",
            " ",
            "if self.global_vars.include_fatigue:",
            "\tprint('Fatigue is included in the model.')",
            "\tops.uniaxialMaterial('Steel02', mat_tag_brace_steel_no_fatigue, steel_brace.Fy, steel_brace.YoungModulus, steel_brace.b, *[steel_brace.R0, steel_brace.cR1, steel_brace.cR2], steel_brace.a1, steel_brace.a2, steel_brace.a3, steel_brace.a4)",
            "\tops.uniaxialMaterial('Fatigue', mat_tag_brace_steel, mat_tag_brace_steel_no_fatigue, '-E0', steel_brace.fatigue_E0, '-m', -0.458, '-min', -1e16, '-max', 1e16)",
            "else:",
            "\tprint('WARNING: Fatigue is not included in the model.')",
            "\tops.uniaxialMaterial('Steel02', mat_tag_brace_steel, steel_brace.Fy, steel_brace.YoungModulus, steel_brace.b, *[steel_brace.R0, steel_brace.cR1, steel_brace.cR2], steel_brace.a1, steel_brace.a2, steel_brace.a3, steel_brace.a4)",
            " ",
            "ops.uniaxialMaterial('Elastic', mat_tag_torsion, 1.0)",
            "ops.uniaxialMaterial('Steel02', mat_tag_VC_steel, steel_column.Fy, steel_column.YoungModulus, steel_column.b, *[steel_column.R0, steel_column.cR1, steel_column.cR2], steel_column.a1, steel_column.a2, steel_column.a3, steel_column.a4)",
        ]

        helper.save_list_to_file(
            self.directory,
            f"{self.formatted_name}_sections_materials.py",
            sections_materials,
        )

        if verbose:
            print("Sections and materials are created and saved.")
        return None

    def geo_transf(self, verbose=False, **kwargs) -> None:
        geo_transfs = [
            "geo_tag_column_x = 1 # columns in X",
            "geo_tag_beam_x = 2 # beams in X",
            "geo_tag_brace_x = 3 # braces in X",
            "geo_tag_column_y = 4 # columns in Y",
            "geo_tag_beam_y = 5 # beams in Y",
            "geo_tag_brace_y = 6 # braces in Y",
            " ",
            "ops.geomTransf('PDelta', geo_tag_column_x, 1.0, 0.0, 0.0)",
            "ops.geomTransf('PDelta', geo_tag_beam_x, -1.0, 0.0, 0.0)",
            "ops.geomTransf('Corotational', geo_tag_brace_x, -1.0, 0.0, 0.0)",
            "ops.geomTransf('PDelta', geo_tag_column_y, 0.0, -1.0, 0.0)",
            "ops.geomTransf('PDelta', geo_tag_beam_y, 0.0, 1.0, 0.0)",
            "ops.geomTransf('Corotational', geo_tag_brace_y, 0.0, -1.0, 0.0)",
        ]

        helper.save_list_to_file(
            self.directory,
            f"{self.formatted_name}_geo_transfs.py",
            geo_transfs,
        )

        if verbose:
            print("GeoTransfer file has been created.")
            print("\tPDelta and Corotational transformations are used.")

        return None

    def global_var(
        self,
        elastic_ceiling_beam=False,
        elastic_floor_beam=False,
        elastic_column=False,
        elastic_brace=False,
        elastic_VC=False,
        elastic_HC=False,
        include_fatigue=False,
        include_element_mass=False,
        verbose=False,
        **kwargs,
    ) -> None:
        global_vars_list = [
            "list_recorder = []",
            "list_mass = []",
            "list_bilin_params = []",
            " ",
            "count_elastic_ceiling_beam = 0",
            "count_elastic_floor_beam = 0",
            "count_elastic_column = 0",
            "count_elastic_brace = 0",
            "count_elastic_VC = 0",
            " ",
        ]
        if elastic_ceiling_beam:
            global_vars_list.append("elastic_ceiling_beam = True")
        else:
            global_vars_list.append("elastic_ceiling_beam = False")

        if elastic_floor_beam:
            global_vars_list.append("elastic_floor_beam = True")
        else:
            global_vars_list.append("elastic_floor_beam = False")

        if elastic_column:
            global_vars_list.append("elastic_column = True")
        else:
            global_vars_list.append("elastic_column = False")

        if elastic_brace:
            global_vars_list.append("elastic_brace = True")
        else:
            global_vars_list.append("elastic_brace = False")

        if elastic_VC:
            global_vars_list.append("elastic_VC = True")
        else:
            global_vars_list.append("elastic_VC = False")

        if elastic_HC:
            global_vars_list.append("elastic_HC = True")
        else:
            global_vars_list.append("elastic_HC = False")

        if include_fatigue:
            global_vars_list.append("\ninclude_fatigue = True")
        else:
            global_vars_list.append("\ninclude_fatigue = False")

        if include_element_mass:
            global_vars_list.append("include_element_mass = True")
        else:
            global_vars_list.append("include_element_mass = False")

        helper.save_list_to_file(
            self.directory,
            f"{self.formatted_name}_global_vars.py",
            global_vars_list,
        )

        if verbose:
            print("Global variables has been created.")

        return None

    def __plot_module_2D(
        self,
        positions,
        modules,
        brace_positions,
        corners,
        unique_x,
        unique_y,
    ) -> tuple:
        fig, ax = plt.subplots()

        for i, (module_number, position) in enumerate(positions.items()):
            module = modules[module_number]
            x, y = position
            ax.plot(
                [x, x + module["x-dir"], x + module["x-dir"], x, x],
                [y, y, y + module["y-dir"], y + module["y-dir"], y],
                color="green",
                linestyle="-",
                linewidth=1,
                label=f"Module Perimeter" if i == 0 else None,
            )

            # Add module number at the middle of the module
            mid_x = x + module["x-dir"] / 2
            mid_y = y + module["y-dir"] / 2
            ax.text(mid_x, mid_y, f"M{module_number}", ha="center", va="center")

        chevron_counter = 0
        other_counter = 0

        for module_number, brace in brace_positions.items():
            if brace:
                for (side, type_brace), relative_coords, global_coords in brace:
                    if type_brace == "Chevron":
                        (
                            _,
                            (global_start_x, global_start_y),
                            (global_middle_x, global_middle_y),
                            (global_end_x, global_end_y),
                        ) = global_coords
                        ax.plot(
                            [global_start_x, global_middle_x, global_end_x],
                            [global_start_y, global_middle_y, global_end_y],
                            color="red",
                            linestyle="-",
                            linewidth=2,
                            label=f"{type_brace} Braces"
                            if chevron_counter == 0
                            else None,
                        )
                        chevron_counter += 1
                    elif type_brace == "X":
                        (
                            _,
                            (global_start_x, global_start_y),
                            (global_end_x, global_end_y),
                        ) = global_coords
                        ax.plot(
                            [global_start_x, global_end_x],
                            [global_start_y, global_end_y],
                            color="blue",
                            linestyle="-",
                            linewidth=2,
                            label=f"{type_brace} Braces"
                            if other_counter == 0
                            else None,
                        )
                        other_counter += 1
                    else:
                        raise ValueError(
                            f"Please provide a valid brace type. {type_brace} is not valid."
                        )

        for i, (module_number, corner) in enumerate(corners.items()):
            for ii, (x, y) in enumerate(corner["corners"]):
                ax.plot(
                    x,
                    y,
                    "o",
                    color="purple",
                    markersize=3,
                    label=f"Columns" if i == 0 and ii == 0 else None,
                )

        plt.title("Layout")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.axis("equal")

        ax.set_xticks(np.r_[unique_x[::2], unique_x[-1]])
        ax.set_yticks(np.r_[unique_y[::2], unique_y[-1]])

        ax.grid(True, alpha=0.5)
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

        return (fig, ax)

    def __plot_nodes_3D(self) -> None:
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection="3d")

        ax.scatter(
            self.df_nodes_height["X"],
            self.df_nodes_height["Y"],
            self.df_nodes_height["Z"],
            s=10,
            c="coral",
        )

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        ax.azim = 30
        ax.elev = 30

        plt.title("Global Nodes (3D)")

        return None
