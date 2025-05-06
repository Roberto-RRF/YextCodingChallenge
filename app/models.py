from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
import re

from dataclasses import dataclass
from datetime import datetime, date
from typing import Dict
import re

@dataclass
class Contact:
    first_name: str
    last_name: str
    zip_code: str
    phone_number: str
    last_contacted: date  # Now a date object

    @classmethod
    def from_dict(cls, data: Dict) -> 'Contact':
        """Create a Contact instance from a dictionary."""
        required_fields = ['first_name', 'last_name', 'zip_code', 'phone_number', 'last_contacted']

        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        if not isinstance(data['first_name'], str) or not data['first_name']:
            raise ValueError("first_name must be a non-empty string")
        if not isinstance(data['last_name'], str) or not data['last_name']:
            raise ValueError("last_name must be a non-empty string")
        if not isinstance(data['zip_code'], str) or not data['zip_code']:
            raise ValueError("zip_code must be a non-empty string")
        if not isinstance(data['phone_number'], str) or not data['phone_number']:
            raise ValueError("phone_number must be a non-empty string")
        if not re.match(r'\d{3}-\d{4}', data['phone_number']):
            raise ValueError("phone_number must be in format '###-####'")

        # Parse and validate last_contacted as a date
        try:
            parsed_datetime = datetime.fromisoformat(data['last_contacted'].replace('Z', '+00:00'))
            last_contacted_date = parsed_datetime.date()
        except ValueError:
            raise ValueError("last_contacted must be a valid ISO 8601 date-time format")

        return cls(
            first_name=data['first_name'],
            last_name=data['last_name'],
            zip_code=data['zip_code'],
            phone_number=data['phone_number'],
            last_contacted=last_contacted_date
        )

    def to_dict(self) -> Dict:
        """Return the contact data as a dictionary (ISO 8601 string for the date)."""
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "zip_code": self.zip_code,
            "phone_number": self.phone_number,
            "last_contacted": self.last_contacted.isoformat()  # Converts date to string
        }

@dataclass
class SortOrder:
    last_contacted: Optional[str] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SortOrder':
        """Create a SortOrder instance from a dictionary."""
        # Validate order directions
        valid_directions = ["asc", "desc"]
        
        for field in data:
            if field not in ['last_contacted', 'last_name', 'first_name']:
                raise ValueError(f"Invalid sort field: {field}")
                
            if data[field] not in valid_directions:
                raise ValueError(f"Sort direction for {field} must be 'asc' or 'desc'")
        
        return cls(
            last_contacted=data.get('last_contacted'),
            last_name=data.get('last_name'),
            first_name=data.get('first_name')
        )


@dataclass
class RequestData:
    sort_order: SortOrder
    contacts: List[Contact]
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'RequestData':
        """Create a RequestData instance from a dictionary."""
        if not isinstance(data, dict):
            raise ValueError("Request body must be a JSON object")
            
        if 'sort_order' not in data:
            raise ValueError("Missing required field: sort_order")
            
        if 'contacts' not in data:
            raise ValueError("Missing required field: contacts")
            
        if not isinstance(data['sort_order'], dict):
            raise ValueError("sort_order must be an object")
            
        if not isinstance(data['contacts'], list):
            raise ValueError("contacts must be an array")
            
        sort_order = SortOrder.from_dict(data['sort_order'])
        contacts = [Contact.from_dict(contact) for contact in data['contacts']]
        
        return cls(
            sort_order=sort_order,
            contacts=contacts
        )
    
    def sort_contacts(self) -> List[Dict]:
        """
        Sort contacts based on the sort_order configuration.
        Returns a list of contacts as dictionaries, sorted according to the sort order.
        """
        # Convert contacts to dictionaries
        contact_dicts = [contact.to_dict() for contact in self.contacts]
        
        # Define sort order - from highest to lowest priority
        sort_priority = ["first_name", "last_name", "last_contacted"]
        
        # Sort in reverse priority order (least important first)
        for field in reversed(sort_priority):
            direction = getattr(self.sort_order, field)
            if direction is not None:
                reverse = (direction == "desc")
                key_func = lambda x: x[field]
                contact_dicts = sorted(contact_dicts, key=key_func, reverse=reverse)

        return contact_dicts