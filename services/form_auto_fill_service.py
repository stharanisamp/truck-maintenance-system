import re
from typing import Dict, Any, List, Optional
from models import Vehicle, Customer

class FormAutoFillService:
    """
    Form Auto-Fill Service:
    - Normalizes extracted AI/OCR data into form-ready structures
    - Performs database entity matching (active fleet vehicles & customer accounts)
    - Links detected text bounding boxes to individual form fields for visual UI highlighting
    """

    @classmethod
    def match_fleet_vehicle(cls, vehicle_text: Optional[str], active_vehicles: List[Vehicle]) -> Optional[Vehicle]:
        """Matches extracted vehicle number with existing fleet vehicles."""
        if not vehicle_text or not active_vehicles:
            return None

        # Clean spaces and hyphens e.g. "TN 52 AB 1234" -> "TN52AB1234"
        clean_extracted = re.sub(r'[\s\-]', '', vehicle_text).upper()

        for v in active_vehicles:
            clean_db = re.sub(r'[\s\-]', '', v.vehicle_number).upper()
            if clean_extracted == clean_db or clean_extracted in clean_db or clean_db in clean_extracted:
                return v

        return None

    @classmethod
    def match_customer(cls, raw_text: str, customers: List[Customer]) -> Optional[Customer]:
        """Matches customer name or location mentioned in raw OCR text against driver's portfolio."""
        if not raw_text or not customers:
            return None

        low = raw_text.lower()
        for c in customers:
            c_name = c.company_name.lower()
            if c_name in low:
                return c
            if c.contact_person and len(c.contact_person) > 3 and c.contact_person.lower() in low:
                return c

        return None

    @classmethod
    def find_field_bounding_boxes(cls, ocr_items: List[Dict[str, Any]], extracted_data: Dict[str, Any]) -> Dict[str, List[float]]:
        """
        Maps each form field to its approximate bounding box [ymin, xmin, ymax, xmax] on the memo.
        Enables interactive click/focus-to-highlight on the document image.
        """
        field_boxes = {}
        if not ocr_items:
            return field_boxes

        targets = {
            "vehicle_number": extracted_data.get("vehicle_number"),
            "memo_number": extracted_data.get("memo_number"),
            "driver_name": extracted_data.get("driver_name"),
            "from_place": extracted_data.get("from_place"),
            "to_place": extracted_data.get("to_place"),
            "freight_amount": str(int(extracted_data.get("freight_amount") or 0)) if extracted_data.get("freight_amount") else None,
            "diesel_expense": str(int(extracted_data.get("fuel_expense") or 0)) if extracted_data.get("fuel_expense") else None,
            "toll_expense": str(int(extracted_data.get("toll_expense") or 0)) if extracted_data.get("toll_expense") else None,
            "loading_charges": str(int(extracted_data.get("loading_charge") or 0)) if extracted_data.get("loading_charge") else None,
            "unloading_charges": str(int(extracted_data.get("unloading_charge") or 0)) if extracted_data.get("unloading_charge") else None,
            "commission_expense": str(int(extracted_data.get("commission_expense") or 0)) if extracted_data.get("commission_expense") else None,
            "food_expense": str(int(extracted_data.get("food_expense") or 0)) if extracted_data.get("food_expense") else None,
            "advance_amount": str(int(extracted_data.get("driver_advance") or 0)) if extracted_data.get("driver_advance") else None,
            "total_expense": str(int(extracted_data.get("total_expense") or 0)) if extracted_data.get("total_expense") else None
        }

        for field_name, val_str in targets.items():
            if not val_str:
                continue
            val_clean = str(val_str).replace(" ", "").lower()
            for item in ocr_items:
                item_txt = str(item.get("text", "")).replace(" ", "").lower()
                if val_clean in item_txt or (len(val_clean) > 4 and item_txt in val_clean):
                    field_boxes[field_name] = item.get("box", [0, 0, 0, 0])
                    break

        return field_boxes

    @classmethod
    def prepare_form_payload(
        cls,
        extracted_data: Dict[str, Any],
        validation_report: Dict[str, Any],
        ocr_result: Any,
        vehicles: List[Vehicle],
        customers: List[Customer],
        memo_file_path: str,
        enhanced_file_path: str,
        driver: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Creates the complete unified payload required by the verification form and API.
        """
        ocr_items = ocr_result.items if hasattr(ocr_result, 'items') else ocr_result.get('items', [])
        raw_text = ocr_result.full_text if hasattr(ocr_result, 'full_text') else ocr_result.get('full_text', "")

        # Entity matching
        matched_vehicle = cls.match_fleet_vehicle(extracted_data.get("vehicle_number"), vehicles)
        matched_customer = cls.match_customer(raw_text, customers)

        # Map bounding boxes for UI interactive highlights
        boxes = cls.find_field_bounding_boxes(ocr_items, extracted_data)

        # Other expenses calculation (parking + repair + misc)
        extra_other = (extracted_data.get("parking_expense") or 0.0) + (extracted_data.get("repair_expense") or 0.0)
        base_other = extracted_data.get("other_expense") or 0.0
        combined_other = round(base_other + extra_other, 2)

        notes_parts = []
        if extracted_data.get("commission_expense"):
            notes_parts.append(f"Commission: ₹{extracted_data['commission_expense']}")
        if extracted_data.get("parking_expense"):
            notes_parts.append(f"Parking: ₹{extracted_data['parking_expense']}")
        if extracted_data.get("repair_expense"):
            notes_parts.append(f"Repair: ₹{extracted_data['repair_expense']}")
        if extracted_data.get("remarks"):
            notes_parts.append(str(extracted_data["remarks"]))
        other_notes = ", ".join(notes_parts)

        d_name = extracted_data.get("driver_name") or (driver.full_name if driver else "")
        d_phone = extracted_data.get("driver_phone") or (driver.phone if driver else "")

        payload = {
            # Document metadata
            "memo_file_path": memo_file_path,
            "enhanced_image_path": enhanced_file_path,
            "raw_text": raw_text,
            
            # Header fields
            "memo_number": extracted_data.get("memo_number") or "",
            "memo_date": extracted_data.get("date") or "",
            "vehicle_number": extracted_data.get("vehicle_number") or "",
            "vehicle_id": matched_vehicle.id if matched_vehicle else None,
            "customer_id": matched_customer.id if matched_customer else None,
            "driver_id": driver.id if driver else None,
            "driver_name": d_name,
            "driver_phone": d_phone,
            "source": extracted_data.get("from_place") or "",
            "destination": extracted_data.get("to_place") or "",
            "material": extracted_data.get("material") or "",
            "load_quantity": extracted_data.get("load_quantity") or "",
            "start_km": extracted_data.get("starting_km") or 0.0,
            "end_km": extracted_data.get("ending_km") or 0.0,
            "total_km": float(extracted_data.get("total_km") or 0.0),
            "fuel_quantity": float(extracted_data.get("fuel_quantity") or 0.0),
            "mileage": float(extracted_data.get("mileage") or 0.0),

            # Financial particulars
            "freight_amount": float(extracted_data.get("freight_amount") or extracted_data.get("trip_amount") or 0.0),
            "advance_amount": float(extracted_data.get("driver_advance") or 0.0),
            "diesel_expense": float(extracted_data.get("fuel_expense") or 0.0),
            "toll_expense": float(extracted_data.get("toll_expense") or 0.0),
            "food_expense": float(extracted_data.get("food_expense") or 0.0),
            "commission_expense": float(extracted_data.get("commission_expense") or 0.0),
            "loading_charges": float(extracted_data.get("loading_charge") or 0.0),
            "unloading_charges": float(extracted_data.get("unloading_charge") or 0.0),
            "other_expenses": combined_other,
            "other_notes": other_notes,
            "balance_amount": float(extracted_data.get("balance_amount") or 0.0),
            "handwritten_total": float(extracted_data.get("total_expense") or 0.0),
            "total_expense": float(extracted_data.get("total_expense") or (
                float(extracted_data.get("fuel_expense") or 0.0) +
                float(extracted_data.get("toll_expense") or 0.0) +
                float(extracted_data.get("food_expense") or 0.0) +
                float(extracted_data.get("commission_expense") or 0.0) +
                float(extracted_data.get("loading_charge") or 0.0) +
                float(extracted_data.get("unloading_charge") or 0.0) +
                combined_other
            )),
            "profit": float(extracted_data.get("net_profit") or (
                float(extracted_data.get("freight_amount") or extracted_data.get("trip_amount") or 0.0) -
                float(extracted_data.get("total_expense") or 0.0)
            )),
            "net_amount": float(extracted_data.get("balance_amount") or (
                float(extracted_data.get("freight_amount") or extracted_data.get("trip_amount") or 0.0) -
                float(extracted_data.get("total_expense") or 0.0)
            )),

            # Tabular Column & Row Model (Excel Grid)
            "table_rows": extracted_data.get("table_rows", []),
            "table_columns": extracted_data.get("table_columns", []),
            "memo_model": extracted_data.get("memo_model", "TRIP_MEMO"),
            "financial_summary": extracted_data.get("financial_summary", {}),

            # Validation & Confidence
            "validation": validation_report,
            "confidence": extracted_data.get("confidence", {}),
            "field_boxes": boxes,
            "ocr_engine": getattr(ocr_result, 'engine', 'EasyOCR')
        }

        return payload
