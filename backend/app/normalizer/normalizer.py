# backend/app/normalizer/normalizer.py
from typing import Dict, Any, Optional
from dateutil.parser import parse as parse_date
import validators

class DataNormalizer:
    def __init__(self, resume_data: Dict[str, Any]):
        self.resume_data = resume_data

    def _normalize_date(self, date_str: Optional[str]) -> Optional[str]:
        if not date_str:
            return None
        try:
            return parse_date(date_str).strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            return None

    def _normalize_url(self, url_str: Optional[str]) -> Optional[str]:
        if not url_str:
            return None
        if validators.url(url_str):
            return url_str
        return None

    def _clean_text(self, text: Optional[str]) -> Optional[str]:
        return text.strip() if text else None

    def normalize(self) -> Dict[str, Any]:
        data = self.resume_data.copy()

        # Normalize basics
        if 'basics' in data:
            basics = data['basics']
            if 'summary' in basics:
                basics['summary'] = self._clean_text(basics.get('summary'))
            if 'url' in basics:
                basics['url'] = self._normalize_url(basics.get('url'))
            if 'image' in basics:
                basics['image'] = self._normalize_url(basics.get('image'))
            
            if 'profiles' in basics:
                for profile in basics['profiles']:
                    if 'url' in profile:
                        profile['url'] = self._normalize_url(profile.get('url'))
                    if 'image' in profile:
                        profile['image'] = self._normalize_url(profile.get('image'))


        # Normalize work
        if 'work' in data:
            for item in data['work']:
                item['startDate'] = self._normalize_date(item.get('startDate'))
                item['endDate'] = self._normalize_date(item.get('endDate'))
                if 'summary' in item:
                    item['summary'] = self._clean_text(item.get('summary'))
                if 'url' in item:
                    item['url'] = self._normalize_url(item.get('url'))
                if 'image' in item:
                    item['image'] = self._normalize_url(item.get('image'))


        # Normalize education
        if 'education' in data:
            for item in data['education']:
                item['startDate'] = self._normalize_date(item.get('startDate'))
                item['endDate'] = self._normalize_date(item.get('endDate'))
                if 'url' in item:
                    item['url'] = self._normalize_url(item.get('url'))
                if 'image' in item:
                    item['image'] = self._normalize_url(item.get('image'))

        # Normalize projects
        if 'projects' in data:
            for item in data['projects']:
                item['startDate'] = self._normalize_date(item.get('startDate'))
                item['endDate'] = self._normalize_date(item.get('endDate'))
                if 'description' in item:
                    item['description'] = self._clean_text(item.get('description'))
                if 'url' in item:
                    item['url'] = self._normalize_url(item.get('url'))
                if 'image' in item:
                    item['image'] = self._normalize_url(item.get('image'))
        
        # Normalize skills
        if 'skills' in data:
            for item in data['skills']:
                if 'image' in item:
                    item['image'] = self._normalize_url(item.get('image'))

        return data