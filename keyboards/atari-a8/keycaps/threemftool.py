from datetime import datetime
from enum import Enum
from typing import cast
from bs4 import BeautifulSoup, Tag
from zipfile import ZipFile
from pathlib import Path

from key_info import COLOR_SCHEME, HAS_LEGEND, KeyInfo


class ThreeMfTool:
    def set_contents(self, xml_data: Tag, contents: Tag | str) -> None:
        """Method to clear and set the content of an XML tag."""
        xml_data.clear()
        xml_data.append(contents)

    def set_metadata(self, xml_data: Tag) -> None:
        """Method to set metadata in the XML, including application details and timestamps."""

        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

        metadata_items = {
            "Application": "Retro-Keys.com AutoGenerator",
            "CreationDate": dt_string,
            "ModificationDate": dt_string,
        }

        for name, value in metadata_items.items():
            el = cast(Tag, xml_data.find("metadata", {"name": name}))
            self.set_contents(el, value)

    def cura_create_object(self, id: str, name: str) -> Tag:
        """Method to create an XML object with given ID and name, of type "model." """

        new_element = Tag(
            name="object",
            attrs={
                "id": id,
                "name": name,
                "type": "model",
            },
        )

        return new_element

    def bambu_create_object(self, id: str, name: str) -> Tag:
        """Method to create an XML object with given ID and name, of type "model." """

        new_element = Tag(
            name="object",
            attrs={
                "id": id,
                #  "name": name,
                "type": "model",
            },
        )

        return new_element

    def cura_add_extruder(self, extruder: int, object: Tag) -> None:
        """Method to add an extruder metadata to an object. Extruder determines which material is used."""
        metadatagroup_element = Tag(name="metadatagroup", attrs={})
        metadata_element = Tag(name="metadata", attrs={"name": "cura:extruder_nr"})
        metadata_element.append(str(extruder))
        metadatagroup_element.append(metadata_element)

        object.append(metadatagroup_element)

    def cura_make_mesh_object(
        self,
        file_name: Path,  # file_name, gets embedded in the XML
        src_xml: Tag,  # The XML to take the mesh from
        object_id: str,  # The object_id for our current object
        extruder: int,  # Which extruder to use
    ) -> Tag:
        """
        Method to create a mesh object from a given file and XML source, with specified ID and extruder.
        """
        base_name = Path(file_name).name
        object1 = cast(Tag, self.cura_create_object(object_id, base_name))
        mesh = cast(Tag, src_xml.find("mesh"))
        self.cura_add_extruder(extruder, object1)
        object1.append(mesh)
        return object1

    def bambu_make_mesh_object(
        self,
        file_name: Path,  # file_name, gets embedded in the XML
        src_xml: Tag,  # The XML to take the mesh from
        object_id: str,  # The object_id for our current object
        extruder: int,  # Which extruder to use
    ) -> Tag:
        """
        Method to create a mesh object from a given file and XML source, with specified ID and extruder.
        """
        base_name = Path(file_name).name
        object1 = cast(Tag, self.bambu_create_object(object_id, base_name))
        mesh = cast(Tag, src_xml.find("mesh"))
        object1.append(mesh)
        return object1

    def create_component(self, id: str) -> Tag:
        """
        Method to create a component with a specified ID in XML.
        """

        component_element = Tag(name="component", attrs={"objectid": id})
        return component_element

    def read_xml_from_zip(self, file_name: Path, model_file_name: str) -> BeautifulSoup:
        """
        Read the XML file from a zip file
        """
        with ZipFile(file_name, "r") as zip:
            data = zip.read(model_file_name)
            return BeautifulSoup(data, "xml")

    def bambu_convert_to_two_color(
        self,
        idx: int,
        legend_file_name: Path,
        keycap_file_name: Path,
        twocolor_file_name: Path,
        template_file_name: Path,
        keyinfo: KeyInfo,
    ) -> None:
        legend_index = str((idx * 1) + 1)
        keycap_index = str((idx * 1) + 2)
        merged_index = str((idx * 1) + 3)

        legend_index = str(1)
        keycap_index = str(2)
        merged_index = str(3)

        model_file_name = "3D/3dmodel.model"

        Bs_legend_data = (
            self.read_xml_from_zip(legend_file_name, model_file_name)
            if keyinfo.has_legend
            else BeautifulSoup("")
        )
        Bs_keycap_data = self.read_xml_from_zip(keycap_file_name, model_file_name)
        Bs_twocolor_data = self.read_xml_from_zip(template_file_name, model_file_name)

        resources = cast(Tag, Bs_twocolor_data.find("resources"))
        build = cast(Tag, Bs_twocolor_data.find("build"))

        for child in resources.findChildren():
            child.extract()

        if keyinfo.has_legend:
            mesh_object1 = self.bambu_make_mesh_object(
                legend_file_name, Bs_legend_data, legend_index, 1
            )
            resources.append(mesh_object1)

        mesh_object2 = self.bambu_make_mesh_object(
            keycap_file_name, Bs_keycap_data, keycap_index, 0
        )
        resources.append(mesh_object2)

        mergedComponent = BeautifulSoup(
            f"""
                <object id="{merged_index}" type="model">
                    <components>
                        <component objectid="1" transform="1 0 0 0 1 0 0 0 1 0 0 0" />
                        <component objectid="2" transform="1 0 0 0 1 0 0 0 1 0 0 0" />
                  </components>
                </object>
                """,
            features="lxml",
        )
        resources.append(cast(Tag, mergedComponent.find("object")))

        extruder1: str = "1"
        extruder2: str = "2"

        if keyinfo.color_scheme == COLOR_SCHEME.REVERSED:
            extruder1 = "2"
            extruder2 = "1"

        model_setting_config = BeautifulSoup(
            f"""
<?xml version="1.0" encoding="UTF-8"?>
<config>
  <object id="3">
    <metadata key="name" value="key_1_legend"/>
    <metadata key="extruder" value="1"/>
    <part id="1" subtype="normal_part">
      <metadata key="name" value="key_1_legend.stl"/>
      <metadata key="matrix" value="1 0 0 -2.1554796099662781 0 1 0 1.796262264251709 0 0 1 3.2037577629089355 0 0 0 1"/>
      <metadata key="source_file" value="key_1_legend.stl"/>
      <metadata key="source_object_id" value="0"/>
      <metadata key="source_volume_id" value="0"/>
      <metadata key="source_offset_x" value="-2.1554796099662781"/>
      <metadata key="source_offset_y" value="1.796262264251709"/>
      <metadata key="source_offset_z" value="7.9809274673461914"/>
      <metadata key="extruder" value="{extruder1}"/>
      <mesh_stat edges_fixed="0" degenerate_facets="0" facets_removed="0" facets_reversed="0" backwards_edges="0"/>
    </part>
    <part id="2" subtype="normal_part">
      <metadata key="name" value="key_1_cap.stl"/>
      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>
      <metadata key="source_file" value="key_1_cap.stl"/>
      <metadata key="source_object_id" value="0"/>
      <metadata key="source_volume_id" value="0"/>
      <metadata key="source_offset_x" value="0"/>
      <metadata key="source_offset_y" value="0"/>
      <metadata key="source_offset_z" value="4.7771697044372559"/>
      <metadata key="extruder" value="{extruder2}"/>
      <mesh_stat edges_fixed="0" degenerate_facets="0" facets_removed="0" facets_reversed="0" backwards_edges="0"/>
    </part>
  </object>
  <plate>
    <metadata key="plater_id" value="1"/>
    <metadata key="plater_name" value=""/>
    <metadata key="locked" value="false"/>
    <metadata key="thumbnail_file" value="Metadata/plate_1.png"/>
    <metadata key="thumbnail_no_light_file" value="Metadata/plate_no_light_1.png"/>
    <metadata key="top_file" value="Metadata/top_1.png"/>
    <metadata key="pick_file" value="Metadata/pick_1.png"/>
    <model_instance>
      <metadata key="object_id" value="3"/>
      <metadata key="instance_id" value="0"/>
      <metadata key="identify_id" value="116"/>
    </model_instance>
  </plate>
  <assemble>
   <assemble_item object_id="3" instance_id="0" transform="1 0 0 0 1 0 0 0 1 21.659985351562501 0 9.5543394088745117" offset="0 0 0" />
  </assemble>
</config>

            """,
            features="lxml",
        )

        # Update the ZIP file
        with ZipFile(twocolor_file_name, "a") as zip_out:
            # Copy all files from the existing ZIP archive
            with ZipFile(template_file_name, "r") as zip_in:
                for item in zip_in.infolist():
                    if item.filename == "Metadata/model_settings.config":
                        continue

                    if item.filename == model_file_name:
                        continue

                    if item.filename != model_file_name:  # Skip the file being replaced
                        with zip_in.open(item) as source:
                            zip_out.writestr(item, source.read())

            # Write the updated 3D model file
            with zip_out.open(model_file_name, "w") as model_file:
                updated_content = bytes(Bs_twocolor_data.prettify(), "utf-8")
                model_file.write(updated_content)

            with zip_out.open(
                "Metadata/model_settings.config", "w"
            ) as model_config_file:
                updated_content = bytes(model_setting_config.prettify(), "utf-8")
                model_config_file.write(updated_content)

    def cura_convert_to_two_color(
        self,
        idx: int,
        legend_file_name: Path,
        keycap_file_name: Path,
        twocolor_file_name: Path,
        template_file_name: Path,
        keyinfo: KeyInfo,
    ) -> None:

        """
        Method to convert separate keycap and legend files into a two-color 3MF object.
        It accepts paths to files for the legend, keycap, and the template, along with their indices.
        """

        legend_index = str((idx * 100) + 1)
        keycap_index = str((idx * 100) + 2)
        merged_index = str((idx * 100) + 3)

        model_file_name = "3D/3dmodel.model"

        Bs_legend_data = (
            self.read_xml_from_zip(legend_file_name, model_file_name)
            if keyinfo.has_legend == HAS_LEGEND.LEGEND_TRUE
            else BeautifulSoup("")
        )
        Bs_keycap_data = self.read_xml_from_zip(keycap_file_name, model_file_name)
        Bs_twocolor_data = self.read_xml_from_zip(template_file_name, model_file_name)

        resources = cast(Tag, Bs_twocolor_data.find("resources"))
        build = cast(Tag, Bs_twocolor_data.find("build"))

        if keyinfo.has_legend:
            mesh_object1 = self.cura_make_mesh_object(
                legend_file_name, Bs_legend_data, legend_index, 1
            )
            resources.append(mesh_object1)

        mesh_object2 = self.cura_make_mesh_object(
            keycap_file_name, Bs_keycap_data, keycap_index, 0
        )
        resources.append(mesh_object2)

        merged_object = cast(Tag, self.cura_create_object(merged_index, "MergedMesh"))

        components_element = Tag(name="components", attrs={})

        if keyinfo.has_legend:
            components_element.append(self.create_component(legend_index))

        components_element.append(self.create_component(keycap_index))

        merged_object.append(components_element)
        resources.append(merged_object)

        item_element = Tag(name="item", attrs={"objectid": merged_index})
        build.append(item_element)

        with ZipFile(twocolor_file_name, "a") as zip:
            with zip.open(model_file_name, "w") as new_hello:
                arr = bytes(Bs_twocolor_data.prettify(), "utf-8")
                new_hello.write(arr)
