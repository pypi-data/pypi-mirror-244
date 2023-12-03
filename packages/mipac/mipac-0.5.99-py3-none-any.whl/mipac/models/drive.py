from __future__ import annotations

from typing import TYPE_CHECKING

from mipac.abstract.model import AbstractModel
from mipac.models.lite.user import PartialUser
from mipac.types.drive import IDriveStatus

if TYPE_CHECKING:
    from mipac.manager.client import ClientManager
    from mipac.manager.drive.files import ClientFileManager
    from mipac.types import IFolder, IFile, IFileProperties
    from mipac.manager.drive.folders import ClientFolderManager


__all__ = ["FileProperties", "File", "Folder"]


class DriveStatus:
    def __init__(self, raw_drive_status: IDriveStatus, *, client: ClientManager) -> None:
        self.__raw_drive_status: IDriveStatus = raw_drive_status
        self.__client: ClientManager = client

    @property
    def capacity(self) -> int:
        """Total capacity of the drive in bytes

        Returns
        -------
        int
            Total capacity of the drive in bytes
        """
        return self.__raw_drive_status["capacity"]

    @property
    def usage(self) -> int:
        """Total usage of the drive in bytes

        Returns
        -------
        int
            Total usage of the drive in bytes
        """
        return self.__raw_drive_status["usage"]


class FileProperties(AbstractModel):
    def __init__(self, raw_properties: IFileProperties) -> None:
        self.__raw_properties: IFileProperties = raw_properties

    @property
    def width(self) -> int | None:
        return self.__raw_properties.get("width")

    @property
    def height(self) -> int | None:
        return self.__raw_properties.get("height")

    @property
    def orientation(self) -> int | None:
        return self.__raw_properties.get("orientation")

    @property
    def avg_color(self) -> str | None:
        return self.__raw_properties.get("avg_color")


class Folder(AbstractModel):
    def __init__(self, raw_folder: IFolder, client: ClientManager):
        self.__raw_folder: IFolder = raw_folder
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        return self.__raw_folder["id"]

    @property
    def created_at(self) -> str:  # TODO: 型
        return self.__raw_folder["created_at"]

    @property
    def name(self) -> str:
        return self.__raw_folder["name"]

    @property
    def parent_id(self) -> str | None:
        return self.__raw_folder["parent_id"]

    @property
    def folders_count(self) -> int | None:
        return self.__raw_folder.get("folders_count")

    @property
    def files_count(self) -> int | None:
        return self.__raw_folder.get("files_count")

    @property
    def parent(self) -> Folder | None:
        return (
            Folder(self.__raw_folder["parent"], client=self.__client)
            if "parent" in self.__raw_folder and self.__raw_folder["parent"]
            else None
        )

    @property
    def api(self) -> ClientFolderManager:
        return self.__client.drive._create_client_folder_manager(folder_id=self.id)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Folder) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)


class File(AbstractModel):
    def __init__(self, raw_file: IFile, *, client: ClientManager):
        self.__raw_file: IFile = raw_file
        self.__client: ClientManager = client

    @property
    def id(self) -> str:
        return self.__raw_file["id"]

    @property
    def created_at(self):
        return self.__raw_file["created_at"]

    @property
    def name(self) -> str:
        return self.__raw_file["name"]

    @property
    def type(self) -> str:
        return self.__raw_file["type"]

    @property
    def md5(self) -> str:
        return self.__raw_file["md5"]

    @property
    def size(self) -> int:
        return self.__raw_file["size"]

    @property
    def is_sensitive(self) -> bool:
        return self.__raw_file["is_sensitive"]

    @property
    def blurhash(self) -> str | None:
        return self.__raw_file["blurhash"]

    @property
    def properties(self) -> FileProperties:
        return FileProperties(self.__raw_file["properties"])

    @property
    def url(self) -> str:
        return self.__raw_file["url"]

    @property
    def thumbnail_url(self) -> str | None:
        return self.__raw_file["thumbnail_url"]

    @property
    def comment(self) -> str | None:
        return self.__raw_file["comment"]

    @property
    def folder_id(self) -> str | None:
        return self.__raw_file["folder_id"]

    @property
    def folder(self) -> Folder | None:
        return (
            Folder(self.__raw_file["folder"], client=self.__client)
            if "folder" in self.__raw_file and self.__raw_file["folder"]
            else None
        )

    @property
    def user_id(self) -> str | None:
        return self.__raw_file["user_id"]

    @property
    def user(self) -> PartialUser | None:
        return (
            PartialUser(self.__raw_file["user"], client=self.__client)
            if "user" in self.__raw_file and self.__raw_file["user"]
            else None
        )

    @property
    def api(self) -> ClientFileManager:
        return self.__client.drive._create_client_file_manager(file_id=self.id)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, File) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
