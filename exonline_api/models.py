from dataclasses import dataclass, field
from typing import List, Optional, Union, TypeVar, Type, Generic

# Generic type variable for APIResponse
T = TypeVar('T')

@dataclass
class APIResponse(Generic[T]):
    """
    Handles the standardized root repsonse from the Ex-Online API.
    Wraps the metadata (status, err, etc.) and the actual data payload.
    """
    status: str             # "success" | "warning" | "danger"
    message: Optional[str]
    err: int                # 0 = no error
    timestamp: int          # unix timestamp
    data: List[T] = field(default_factory=list)

    token: Optional[str] = None
    auto_close: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: dict, data_class: Type[T]) -> 'APIResponse[T]':
        """
        Parses the root JSON and converts the 'data' list into objects of type `data_class`.
        """
        # Safely handle if 'data' is None/Null
        raw_data_list = data.get("data")
        if raw_data_list is None:
            parsed_data = []
        else:
            # Recursively parse each item in the list using the provided class
            parsed_data = [data_class.from_dict(item) for item in raw_data_list]

        return cls(
            status=data.get("status", ""),
            message=data.get("message", ""),
            err=data.get("err", 0),
            timestamp=data.get("timestamp", 0),
            data=parsed_data,
            token=data.get("token", ""),
            auto_close=data.get("auto-close") # Handles key with hyphen
        )

@dataclass
class AssociatedEq:
    """
    Represents an associated equipment item tied to the specified dossier.
    """
    dossier_id: int
    project_id: int
    ae_item_no: Optional[Union[str, int]]  # Handles string|number|null
    linked_items: int
    description: str
    updated_by: str
    updated_dt: str  # Kept as str, can be parsed to datetime if needed
    dossier_state: str
    dossier_state_dt: str
    dossier_dossier_id: int
    dossier_dossier_id1: int
    
    # Nullable fields
    service: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    cert: Optional[str] = None
    
    # EX Ratings (exr_*)
    exr_epl: Optional[str] = None
    exr_group: Optional[str] = None
    exr_prot: Optional[str] = None
    exr_tclass: Optional[str] = None
    exr_amb_min: Optional[str] = None
    exr_amb_max: Optional[str] = None
    is_simple: Optional[str] = "N" # Defaulting to N if missing
    
    # Electrical Ratings (exr_*)
    exr_ip: Optional[str] = None
    exr_ui: Optional[str] = None
    exr_ii: Optional[str] = None
    exr_pi: Optional[str] = None
    exr_ci: Optional[str] = None
    exr_li: Optional[str] = None
    
    # Barrier Ratings (bar_*)
    bar_um: Optional[str] = None
    bar_uo: Optional[str] = None
    bar_io: Optional[str] = None
    bar_po: Optional[str] = None
    bar_co: Optional[str] = None
    bar_lo: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'AssociatedEq':
        """Safely creates an instance from a dictionary."""
        return cls(
            dossier_id=data.get("dossier_id"),
            project_id=data.get("project_id"),
            ae_item_no=data.get("ae_item_no"),
            linked_items=data.get("linked_items"),
            description=data.get("description", ""),
            service=data.get("service"),
            manufacturer=data.get("manufacturer"),
            model=data.get("model"),
            cert=data.get("cert"),
            exr_epl=data.get("exr_epl"),
            exr_group=data.get("exr_group"),
            exr_prot=data.get("exr_prot"),
            exr_tclass=data.get("exr_tclass"),
            exr_amb_min=data.get("exr_amb_min"),
            exr_amb_max=data.get("exr_amb_max"),
            is_simple=data.get("is_simple", "N"),
            exr_ip=data.get("exr_ip"),
            exr_ui=data.get("exr_ui"),
            exr_ii=data.get("exr_ii"),
            exr_pi=data.get("exr_pi"),
            exr_ci=data.get("exr_ci"),
            exr_li=data.get("exr_li"),
            bar_um=data.get("bar_um"),
            bar_uo=data.get("bar_uo"),
            bar_io=data.get("bar_io"),
            bar_po=data.get("bar_po"),
            bar_co=data.get("bar_co"),
            bar_lo=data.get("bar_lo"),
            updated_by=data.get("updated_by", ""),
            updated_dt=data.get("updated_dt", ""),
            dossier_state=data.get("dossier_state", ""),
            dossier_state_dt=data.get("dossier_state_dt", ""),
            dossier_dossier_id=data.get("dossier_dossier_id"),
            dossier_dossier_id1=data.get("dossier_dossier_id1"),
        )


@dataclass
class Document:
    """
    Represents a document attached to the equipment.
    """
    dossier_id: int
    document_id: int
    document_no_issued: str
    updated_by: str
    updated_dt: str
    doc_type: str
    file_name_stored: str
    link: str
    issue_no: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Document':
        return cls(
            dossier_id=data.get("dossier_id"),
            document_id=data.get("document_id"),
            document_no_issued=data.get("document_no_issued", ""),
            issue_no=data.get("issue_no"),
            updated_by=data.get("updated_by", ""),
            updated_dt=data.get("updated_dt", ""),
            doc_type=data.get("doc_type", ""),
            file_name_stored=data.get("file_name_stored", ""),
            link=data.get("link", "")
        )


@dataclass
class AttachmentData:
    """
    The root response object containing lists of associated equipment and documents.
    """
    dossier_id: int
    assoc_eq: List[AssociatedEq] = field(default_factory=list)
    doc: List[Document] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> 'AttachmentData':
        return cls(
            dossier_id=data.get("dossier_id"),
            # Recursively parse the lists of objects
            assoc_eq=[
                AssociatedEq.from_dict(item) 
                for item in (data.get("assoc_eq") or [])
            ],
            doc=[
                Document.from_dict(item) 
                for item in (data.get("doc") or [])
            ]
        )


@dataclass
class Project:
    """
    Represents a project in Ex-Online.
    """
    pgid: int # project ID
    name: str
    description: Optional[str] = None
    client: Optional[str] = None
    proj_job_no: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Project':
        return cls(
            pgid=data.get("pgid"),
            name=data.get("name", ""),
            description=data.get("description"),
            client=data.get("client"),
            proj_job_no=data.get("proj_job_no")
        )
    
@dataclass
class EqItem:
    """
    Represents a detailed equipment item returned by ListEq.
    """
    dossier_id: int
    project_id: int
    tag_no: str
    site: str
    area: str
    description: str
    service: str
    location: str
    manufacturer: str
    model: str
    install_date: str
    last_insp_date: str
    last_insp_grade: str
    insp_interval_month: int
    ac_zone: str
    ac_epl: str
    ac_group: str
    ac_tclass: str
    ac_amb_min: str
    ac_amb_max: str
    ac_ip: str
    cert: str
    cert_issue: str
    is_simple: str
    exr_epl: str
    exr_group: str
    exr_prot: str
    exr_tclass: str
    exr_amb_min: str
    exr_amb_max: str
    exr_ip: str
    updated_by: str
    updated_dt: str
    dossier_state: str
    dossier_state_dt: str

    # Defects, Actions, 
    D: int = 0
    C: int = 0
    A: int = 0

    # Nullable Fields (string|null)
    serial_no: Optional[str] = None
    actual_last_insp_date: Optional[str] = None
    last_system_insp_upload_dt: Optional[str] = None
    eq_group: Optional[str] = None
    ce_code: Optional[str] = None
    eex: Optional[str] = None
    certified_to: Optional[str] = None
    
    # Motor Details
    mot_kw: Optional[str] = None
    mot_voltage: Optional[str] = None
    mot_amps: Optional[str] = None
    mot_hz: Optional[str] = None
    mot_rpm: Optional[str] = None
    exe_mot_Ia_In: Optional[str] = None
    exe_mot_te: Optional[str] = None

    # Ratings
    exr_ui: Optional[str] = None
    exr_ii: Optional[str] = None
    exr_pi: Optional[str] = None
    exr_ci: Optional[str] = None
    exr_li: Optional[str] = None
    bar_um: Optional[str] = None
    bar_uo: Optional[str] = None
    bar_io: Optional[str] = None
    bar_po: Optional[str] = None
    bar_co: Optional[str] = None
    bar_lo: Optional[str] = None

    # Extras
    other_1: Optional[str] = None
    other_2: Optional[str] = None
    other_3: Optional[str] = None
    other_4: Optional[str] = None
    other_5: Optional[str] = None
    other_6: Optional[str] = None
    comment_1: Optional[str] = None
    comment_2: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'EqItem':
        return cls(
            dossier_id=data.get("dossier_id"),
            project_id=data.get("project_id"),
            tag_no=data.get("tag_no", ""),
            D=data.get("D", 0),
            C=data.get("C", 0),
            A=data.get("A", 0),
            site=data.get("site", ""),
            area=data.get("area", ""),
            description=data.get("description", ""),
            service=data.get("service", ""),
            location=data.get("location", ""),
            manufacturer=data.get("manufacturer", ""),
            model=data.get("model", ""),
            serial_no=data.get("serial_no"),
            install_date=data.get("install_date", ""),
            last_insp_date=data.get("last_insp_date", ""),
            last_insp_grade=data.get("last_insp_grade", ""),
            actual_last_insp_date=data.get("actual_last_insp_date"),
            last_system_insp_upload_dt=data.get("last_system_insp_upload_dt"),
            insp_interval_month=data.get("insp_interval_month", 0),
            ac_zone=data.get("ac_zone", ""),
            ac_epl=data.get("ac_epl", ""),
            ac_group=data.get("ac_group", ""),
            ac_tclass=data.get("ac_tclass", ""),
            ac_amb_min=data.get("ac_amb_min", ""),
            ac_amb_max=data.get("ac_amb_max", ""),
            ac_ip=data.get("ac_ip", ""),
            cert=data.get("cert", ""),
            cert_issue=data.get("cert_issue", ""),
            is_simple=data.get("is_simple", ""),
            eq_group=data.get("eq_group"),
            ce_code=data.get("ce_code"),
            eex=data.get("eex"),
            certified_to=data.get("certified_to"),
            exr_epl=data.get("exr_epl", ""),
            exr_group=data.get("exr_group", ""),
            exr_prot=data.get("exr_prot", ""),
            exr_tclass=data.get("exr_tclass", ""),
            exr_amb_min=data.get("exr_amb_min", ""),
            exr_amb_max=data.get("exr_amb_max", ""),
            exr_ip=data.get("exr_ip", ""),
            mot_kw=data.get("mot_kw"),
            mot_voltage=data.get("mot_voltage"),
            mot_amps=data.get("mot_amps"),
            mot_hz=data.get("mot_hz"),
            mot_rpm=data.get("mot_rpm"),
            exe_mot_Ia_In=data.get("exe_mot_Ia_In"),
            exe_mot_te=data.get("exe_mot_te"),
            exr_ui=data.get("exr_ui"),
            exr_ii=data.get("exr_ii"),
            exr_pi=data.get("exr_pi"),
            exr_ci=data.get("exr_ci"),
            exr_li=data.get("exr_li"),
            bar_um=data.get("bar_um"),
            bar_uo=data.get("bar_uo"),
            bar_io=data.get("bar_io"),
            bar_po=data.get("bar_po"),
            bar_co=data.get("bar_co"),
            bar_lo=data.get("bar_lo"),
            other_1=data.get("other_1"),
            other_2=data.get("other_2"),
            other_3=data.get("other_3"),
            other_4=data.get("other_4"),
            other_5=data.get("other_5"),
            other_6=data.get("other_6"),
            comment_1=data.get("comment_1"),
            comment_2=data.get("comment_2"),
            updated_by=data.get("updated_by", ""),
            updated_dt=data.get("updated_dt", ""),
            dossier_state=data.get("dossier_state", ""),
            dossier_state_dt=data.get("dossier_state_dt", "")
        )