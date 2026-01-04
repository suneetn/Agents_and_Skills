#!/usr/bin/env python3
"""
Earnings Transcript Extractor
Extracts earnings call transcripts from FMP API or SEC EDGAR and uses AI to extract insights
"""

import requests
import os
import re
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class EarningsTranscriptExtractor:
    """Extract and analyze earnings call transcripts"""
    
    FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"
    SEC_BASE_URL = "https://data.sec.gov"
    SEC_URL = "https://www.sec.gov"
    
    def __init__(self):
        self.fmp_api_key = os.getenv('FMP_API_KEY')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
    
    def get_transcript_from_fmp(self, symbol: str, date: Optional[str] = None) -> Dict:
        """Get earnings transcript from FMP API"""
        if not self.fmp_api_key:
            return {'available': False, 'reason': 'FMP_API_KEY not set'}
        
        try:
            # First, get available transcript dates
            dates_url = f"{self.FMP_BASE_URL}/transcripts-dates-by-symbol/{symbol}"
            dates_response = requests.get(dates_url, params={'apikey': self.fmp_api_key}, timeout=10)
            
            if dates_response.status_code == 200:
                dates_data = dates_response.json()
                if dates_data and isinstance(dates_data, list) and len(dates_data) > 0:
                    # Get most recent transcript date
                    latest_date = dates_data[0].get('date') if not date else date
                    
                    # Get transcript for that date
                    transcript_url = f"{self.FMP_BASE_URL}/earnings-transcript/{symbol}"
                    transcript_response = requests.get(
                        transcript_url,
                        params={'apikey': self.fmp_api_key, 'date': latest_date},
                        timeout=10
                    )
                    
                    if transcript_response.status_code == 200:
                        transcript_data = transcript_response.json()
                        if transcript_data and isinstance(transcript_data, dict):
                            content = transcript_data.get('content', '')
                            if content:
                                return {
                                    'available': True,
                                    'source': 'FMP',
                                    'date': transcript_data.get('date', latest_date),
                                    'quarter': transcript_data.get('quarter'),
                                    'year': transcript_data.get('year'),
                                    'content': content,
                                    'transcript': content
                                }
            
            return {'available': False, 'reason': 'No transcript found in FMP (may require premium)'}
        except Exception as e:
            return {'available': False, 'reason': f'FMP API error: {str(e)}'}
    
    def get_transcript_from_sec(self, symbol: str) -> Dict:
        """Try to get transcript from SEC EDGAR (8-K exhibits and filing text)"""
        try:
            # Get CIK
            cik = self._get_company_cik(symbol)
            if not cik:
                return {'available': False, 'reason': 'CIK not found'}
            
            # Get recent 8-K filings (earnings calls often filed here)
            url = f"{self.SEC_BASE_URL}/submissions/CIK{cik}.json"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                filings = data.get('filings', {}).get('recent', {})
                forms = filings.get('form', [])
                dates = filings.get('filingDate', [])
                accession_numbers = filings.get('accessionNumber', [])
                descriptions = filings.get('description', [])
                
                # Find recent 8-K filings
                for i, form in enumerate(forms[:30]):  # Check last 30 filings
                    if form == '8-K':
                        filing_date = dates[i] if i < len(dates) else None
                        accession = accession_numbers[i] if i < len(accession_numbers) else None
                        description = descriptions[i] if i < len(descriptions) else ''
                        
                        if filing_date and accession:
                            # Check description for earnings-related keywords
                            desc_lower = description.lower()
                            earnings_keywords = ['earnings', 'results', 'financial results', 'quarterly', 'q1', 'q2', 'q3', 'q4']
                            
                            if any(keyword in desc_lower for keyword in earnings_keywords):
                                # Try to get filing text first
                                filing_text = self._get_filing_text(cik, accession)
                                if filing_text:
                                    # Check if main filing contains transcript
                                    if self._is_transcript(filing_text):
                                        return {
                                            'available': True,
                                            'source': 'SEC',
                                            'date': filing_date,
                                            'content': filing_text,
                                            'transcript': filing_text
                                        }
                                    
                                    # Try to extract transcript from filing text (may be embedded)
                                    transcript_text = self._extract_transcript_from_filing(filing_text)
                                    if transcript_text:
                                        return {
                                            'available': True,
                                            'source': 'SEC',
                                            'date': filing_date,
                                            'content': transcript_text,
                                            'transcript': transcript_text
                                        }
                                
                                # Try to get exhibits (transcripts often filed as Exhibit 99.1, 99.2, etc.)
                                exhibits = self._get_filing_exhibits(cik, accession)
                                for exhibit_text in exhibits:
                                    if self._is_transcript(exhibit_text):
                                        return {
                                            'available': True,
                                            'source': 'SEC',
                                            'date': filing_date,
                                            'content': exhibit_text,
                                            'transcript': exhibit_text
                                        }
            
            return {'available': False, 'reason': 'No transcript found in SEC filings'}
        except Exception as e:
            return {'available': False, 'reason': f'SEC API error: {str(e)}'}
    
    def _extract_transcript_from_filing(self, filing_text: str) -> Optional[str]:
        """Extract transcript text from filing (may be embedded in HTML or structured text)"""
        if not filing_text:
            return None
        
        # Look for transcript sections in filing
        # Common patterns: <TRANSCRIPT>, <DOCUMENT>, or sections with transcript indicators
        import re
        
        # Try to find transcript section markers
        transcript_patterns = [
            r'<TRANSCRIPT[^>]*>(.*?)</TRANSCRIPT>',
            r'<DOCUMENT[^>]*TYPE="TRANSCRIPT"[^>]*>(.*?)</DOCUMENT>',
            r'(?:TRANSCRIPT|EARNINGS CALL|CONFERENCE CALL)(.*?)(?:END OF TRANSCRIPT|END OF CALL|</DOCUMENT>)',
        ]
        
        for pattern in transcript_patterns:
            match = re.search(pattern, filing_text, re.IGNORECASE | re.DOTALL)
            if match:
                transcript_text = match.group(1)
                if len(transcript_text) > 1000:  # Reasonable transcript length
                    return transcript_text
        
        # If no structured markers, check if entire filing looks like transcript
        if self._is_transcript(filing_text) and len(filing_text) > 5000:
            return filing_text
        
        return None
    
    def _get_filing_exhibits(self, cik: str, accession: str) -> List[str]:
        """Get exhibit files from SEC filing"""
        exhibits = []
        try:
            accession_no_dashes = accession.replace('-', '')
            base_url = f"{self.SEC_URL}/Archives/edgar/data/{cik}/{accession_no_dashes}"
            
            # Try common exhibit file names
            exhibit_names = [
                'ex99-1.txt', 'ex99-2.txt', 'ex99-3.txt',
                'ex991.txt', 'ex992.txt', 'ex993.txt',
                'exhibit99-1.txt', 'exhibit99-2.txt',
                'exhibit991.txt', 'exhibit992.txt'
            ]
            
            for exhibit_name in exhibit_names:
                exhibit_url = f"{base_url}/{exhibit_name}"
                try:
                    response = requests.get(exhibit_url, headers=self.headers, timeout=5)
                    if response.status_code == 200:
                        exhibit_text = response.text[:100000]  # First 100k chars
                        if exhibit_text and len(exhibit_text) > 1000:
                            exhibits.append(exhibit_text)
                except:
                    continue
            
            return exhibits
        except:
            return []
    
    def _get_company_cik(self, symbol: str) -> Optional[str]:
        """Get CIK from ticker symbol"""
        try:
            url = f'{self.SEC_URL}/files/company_tickers.json'
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for company in data.values():
                    if company.get('ticker', '').upper() == symbol.upper():
                        return str(company.get('cik_str', '')).zfill(10)
            return None
        except:
            return None
    
    def _get_filing_text(self, cik: str, accession: str) -> Optional[str]:
        """Get filing text from SEC"""
        try:
            # Convert accession to filing URL format
            accession_no_dashes = accession.replace('-', '')
            url = f"{self.SEC_URL}/Archives/edgar/data/{cik}/{accession_no_dashes}/{accession}.txt"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.text[:50000]  # First 50k chars
            return None
        except:
            return None
    
    def _is_transcript(self, text: str) -> bool:
        """Check if text looks like an earnings transcript"""
        if not text or len(text) < 500:
            return False
        
        transcript_indicators = [
            'operator', 'conference call', 'earnings call', 'q&a', 'question and answer',
            'prepared remarks', 'opening remarks', 'closing remarks', 'analyst',
            'good morning', 'good afternoon', 'thank you for joining',
            'earnings conference', 'quarterly earnings', 'fiscal year',
            'questions and answers', 'q and a', 'question-and-answer'
        ]
        text_lower = text.lower()
        matches = sum(1 for indicator in transcript_indicators if indicator in text_lower)
        
        # Also check for speaker patterns (common in transcripts)
        speaker_patterns = [
            r'\b[A-Z][a-z]+\s+[A-Z][a-z]+:',  # "John Smith:"
            r'\([A-Z][a-z]+\s+[A-Z][a-z]+\)',  # "(John Smith)"
        ]
        import re
        speaker_matches = sum(1 for pattern in speaker_patterns if re.search(pattern, text))
        
        # Transcript if: (3+ indicators) OR (2+ indicators AND speaker patterns)
        return matches >= 3 or (matches >= 2 and speaker_matches >= 5)
    
    def extract_transcript(self, symbol: str) -> Dict:
        """
        Main method to extract transcript from any available source
        
        NOTE: Full earnings call transcripts are rarely filed with SEC.
        Most companies provide transcripts on their investor relations pages.
        This method tries SEC first (for companies that do file transcripts),
        then falls back to FMP if available.
        
        For most companies, transcripts will not be available from SEC.
        The intelligence from transcripts can be partially extracted from:
        - SEC 8-K earnings releases (prepared remarks, key points)
        - SEC 10-K/10-Q MD&A sections (forward-looking statements)
        - SEC 6-K filings (for foreign issuers)
        """
        # Try SEC first (free, publicly available)
        # Note: Most companies don't file full transcripts, but some do
        result = self.get_transcript_from_sec(symbol)
        
        if not result.get('available'):
            # Fallback to FMP (may require premium)
            result = self.get_transcript_from_fmp(symbol)
        
        return result
    
    def extract_insights_ai(self, transcript_text: str, symbol: str) -> Dict:
        """
        Extract insights from transcript using AI
        
        NOTE: This function is called by the agent (Claude) during workflow execution.
        The agent generates structured insights directly based on the transcript content.
        
        Returns:
            Dict with structured insights:
            {
                'management_guidance': {},
                'key_metrics_discussed': [],
                'strategic_initiatives': [],
                'sentiment': {},
                'forward_statements': [],
                'q_and_a_highlights': []
            }
        """
        # Agent generates insights directly from transcript
        # This is where the agent (me!) creates structured insights
        # The agent understands context, extracts key points, and synthesizes insights
        
        if not transcript_text:
            return None
        
        # Agent will generate insights when orchestrating workflow
        # For now, return None - agent will populate during workflow execution
        return None

