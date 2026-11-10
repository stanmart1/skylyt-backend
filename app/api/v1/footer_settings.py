from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.core.dependencies import get_current_user
from app.core.database import get_db
from app.models.footer_settings import FooterSettings
from app.models.contact_settings import ContactSettings

router = APIRouter()

CONTACT_FIELDS = ("contact_address", "contact_phone", "contact_email")


def _model_default(model, field: str):
    default = model.__table__.columns[field].default
    return default.arg if default is not None else None


DEFAULT_COMPANY_NAME = _model_default(FooterSettings, "company_name")
DEFAULT_COMPANY_DESCRIPTION = _model_default(FooterSettings, "company_description")
DEFAULT_CONTACT_VALUES = {
    field: _model_default(ContactSettings, field) for field in CONTACT_FIELDS
}


class FooterSettingsUpdate(BaseModel):
    company_name: Optional[str] = None
    company_description: Optional[str] = None
    twitter_url: Optional[str] = None
    instagram_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    contact_address: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None


def _get_contact_settings(db: Session) -> Optional[ContactSettings]:
    return db.query(ContactSettings).first()


def _is_customized(value: Optional[str], field: str) -> bool:
    return bool(value) and value != DEFAULT_CONTACT_VALUES[field]


def _resolve_contact_value(
    contact_settings: Optional[ContactSettings],
    footer_settings: Optional[FooterSettings],
    field: str,
) -> str:
    """Resolve a contact detail from the shared settings.

    ContactSettings is the canonical source. FooterSettings values are only
    used when ContactSettings has not been customized (legacy installations
    that configured contact details from the Footer page).
    """
    contact_value = getattr(contact_settings, field, None) if contact_settings else None
    footer_value = getattr(footer_settings, field, None) if footer_settings else None

    if _is_customized(contact_value, field):
        return contact_value
    if _is_customized(footer_value, field):
        return footer_value
    if contact_value:
        return contact_value
    if footer_value:
        return footer_value
    return DEFAULT_CONTACT_VALUES[field]


def _serialize_footer_settings(
    footer_settings: Optional[FooterSettings],
    contact_settings: Optional[ContactSettings],
) -> dict:
    response = {
        "company_name": (
            getattr(footer_settings, "company_name", None) or DEFAULT_COMPANY_NAME
        ),
        "company_description": (
            getattr(footer_settings, "company_description", None)
            or DEFAULT_COMPANY_DESCRIPTION
        ),
        "twitter_url": getattr(footer_settings, "twitter_url", None),
        "instagram_url": getattr(footer_settings, "instagram_url", None),
        "linkedin_url": getattr(footer_settings, "linkedin_url", None),
    }
    for field in CONTACT_FIELDS:
        response[field] = _resolve_contact_value(
            contact_settings, footer_settings, field
        )
    return response


@router.get("/admin/footer-settings")
async def get_footer_settings(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get footer settings (admin only)"""
    if not (current_user.is_admin() or current_user.is_superadmin()):
        raise HTTPException(status_code=403, detail="Admin access required")

    settings = db.query(FooterSettings).first()
    if not settings:
        # Create default settings if none exist
        settings = FooterSettings()
        db.add(settings)
        db.commit()
        db.refresh(settings)

    contact_settings = _get_contact_settings(db)
    return {
        "id": settings.id,
        **_serialize_footer_settings(settings, contact_settings),
    }


@router.put("/admin/footer-settings")
async def update_footer_settings(
    settings_data: FooterSettingsUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update footer settings (admin only)"""
    if not (current_user.is_admin() or current_user.is_superadmin()):
        raise HTTPException(status_code=403, detail="Admin access required")

    settings = db.query(FooterSettings).first()
    if not settings:
        settings = FooterSettings()
        db.add(settings)

    contact_settings = _get_contact_settings(db)
    if not contact_settings:
        contact_settings = ContactSettings()
        db.add(contact_settings)

    update_data = settings_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field in CONTACT_FIELDS:
            setattr(contact_settings, field, value)
        elif hasattr(settings, field):
            setattr(settings, field, value)

    db.commit()
    db.refresh(settings)
    db.refresh(contact_settings)

    return {"message": "Footer settings updated successfully"}


@router.get("/footer-settings")
async def get_public_footer_settings(db: Session = Depends(get_db)):
    """Get footer settings for public use"""
    settings = db.query(FooterSettings).first()
    contact_settings = _get_contact_settings(db)
    return _serialize_footer_settings(settings, contact_settings)
