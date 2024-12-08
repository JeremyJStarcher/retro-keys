from datetime import datetime
from typing import cast
from bs4 import BeautifulSoup, Tag
from zipfile import ZipFile
from pathlib import Path


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

    def create_object(self, id: str, name: str) -> Tag:
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

    def add_extruder(self, extruder: int, object: Tag) -> None:
        """Method to add an extruder metadata to an object. Extruder determines which material is used."""
        metadatagroup_element = Tag(name="metadatagroup", attrs={})
        metadata_element = Tag(name="metadata", attrs={"name": "cura:extruder_nr"})
        metadata_element.append(str(extruder))
        metadatagroup_element.append(metadata_element)

        object.append(metadatagroup_element)

    def make_mesh_object(
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
        object1 = cast(Tag, self.create_object(object_id, base_name))
        mesh = cast(Tag, src_xml.find("mesh"))
        self.add_extruder(extruder, object1)
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

    def cura_convert_to_two_color(
        self,
        idx: int,
        legend_file_name: Path,
        keycap_file_name: Path,
        twocolor_file_name: Path,
        template_file_name: Path,
        has_legend: bool,
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
            if has_legend
            else BeautifulSoup("")
        )
        Bs_keycap_data = self.read_xml_from_zip(keycap_file_name, model_file_name)
        Bs_twocolor_data = self.read_xml_from_zip(template_file_name, model_file_name)

        resources = cast(Tag, Bs_twocolor_data.find("resources"))
        build = cast(Tag, Bs_twocolor_data.find("build"))

        if has_legend:
            mesh_object1 = self.make_mesh_object(
                legend_file_name, Bs_legend_data, legend_index, 1
            )
            resources.append(mesh_object1)

        mesh_object2 = self.make_mesh_object(
            keycap_file_name, Bs_keycap_data, keycap_index, 0
        )
        resources.append(mesh_object2)

        merged_object = cast(Tag, self.create_object(merged_index, "MergedMesh"))

        components_element = Tag(name="components", attrs={})

        if has_legend:
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
