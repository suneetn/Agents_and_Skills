#!/usr/bin/env python3
"""
SEC EDGAR Guidance Extractor
Extracts management guidance from SEC filings (20-F, 6-K for foreign issuers; 10-K, 10-Q for US companies)
"""

import requests
import re
from typing import Dict, List, Optional
from datetime import datetime
import json


class SECGuidanceExtractor:
    """Extract management guidance from SEC EDGAR filings"""
    
    BASE_URL = "https://data.sec.gov"
    SEC_URL = "https://www.sec.gov"
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
    
    def get_company_cik(self, symbol: str) -> Optional[str]:
        """Get CIK (Central Index Key) from ticker symbol"""
        try:
            url = f'{self.SEC_URL}/files/company_tickers.json'
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for company in data.values():
                    if company.get('ticker', '').upper() == symbol.upper():
                        cik = str(company.get('cik_str', '')).zfill(10)
                        return cik
            return None
        except Exception as e:
            print(f"Error getting CIK for {symbol}: {e}")
            return None
    
    def get_recent_filings(self, cik: str, form_types: List[str] = None, limit: int = 10) -> List[Dict]:
        """Get recent filings of specified types"""
        if form_types is None:
            # Default: 20-F and 6-K for foreign issuers, 10-K and 10-Q for US companies
            form_types = ['20-F', '6-K', '10-K', '10-Q']
        
        try:
            url = f'{self.BASE_URL}/submissions/CIK{cik}.json'
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                filings = data.get('filings', {}).get('recent', {})
                
                forms = filings.get('form', [])
                descriptions = filings.get('description', [])
                dates = filings.get('filingDate', [])
                accession_numbers = filings.get('accessionNumber', [])
                
                relevant_filings = []
                for i, form in enumerate(forms[:50]):  # Check last 50 filings
                    if form in form_types:
                        relevant_filings.append({
                            'form': form,
                            'date': dates[i] if i < len(dates) else None,
                            'description': descriptions[i] if i < len(descriptions) else '',
                            'accession': accession_numbers[i] if i < len(accession_numbers) else None
                        })
                        if len(relevant_filings) >= limit:
                            break
                
                return relevant_filings
            return []
        except Exception as e:
            print(f"Error getting filings for CIK {cik}: {e}")
            return []
    
    def extract_guidance_ai(self, text: str, symbol: str) -> Dict:
        """
        Extract management guidance from SEC filing text using AI
        
        NOTE: This function checks for agent-generated extraction first.
        The agent (Claude) generates structured extraction during workflow execution.
        
        Returns:
            Dict with structured guidance data
        """
        # Check for agent-generated extraction first
        try:
            from agent_interpretation_injector import get_agent_interpretation
            import json
            
            # Generate key for this extraction
            guidance_key = f"sec_guidance_{symbol}_{hash(text[:500])}"
            agent_extraction = get_agent_interpretation(guidance_key)
            
            if agent_extraction:
                # Agent has generated extraction - parse and return
                try:
                    guidance = json.loads(agent_extraction)
                    if isinstance(guidance, dict):
                        return guidance
                except json.JSONDecodeError:
                    # If not JSON, try to parse as dict string
                    pass
        
        except ImportError:
            # agent_interpretation_injector not available
            pass
        except Exception:
            # Any other error - fall through to empty return
            pass
        
        # No agent extraction available - return empty structure
        # Agent will populate this during workflow execution
        return {
            'revenue_targets': [],
            'profitability_timeline': None,
            'ebitda_targets': [],
            'gmv_targets': [],
            'operational_milestones': [],
            'forward_statements': [],
            'self_funded_growth': False,
            'no_capital_raises': False,
            'operational_metrics': {}
        }
    
    def extract_guidance_from_text(self, text: str) -> Dict:
        """Extract guidance from text using regex patterns (FALLBACK - use extract_guidance_ai instead)"""
        guidance = {
            'revenue_targets': [],
            'profitability_timeline': None,
            'ebitda_targets': [],
            'gmv_targets': [],
            'operational_milestones': [],
            'forward_statements': [],
            'self_funded_growth': False,  # NEW: Self-funded growth flag
            'no_capital_raises': False  # NEW: No capital raises flag
        }
        
        if not text:
            return guidance
        
        text_lower = text.lower()
        
        # Revenue/GMV targets (e.g., "$2.5-$3B GMV by 2030")
        # Focus on future years (2026-2035) to avoid false positives from filing dates
        revenue_patterns = [
            r'\$[\d.]+[BMK]?\s*(?:to|-)?\s*\$?[\d.]+[BMK]?\s*(?:GMV|revenue|sales|turnover).*?(?:by|in|target|reach|achieve).*?(20[2-3][6-9]|203[0-5])',
            r'(?:GMV|revenue|sales|turnover).*?\$[\d.]+[BMK]?\s*(?:to|-)?\s*\$?[\d.]+[BMK]?.*?(?:by|in|target|reach|achieve).*?(20[2-3][6-9]|203[0-5])',
            r'(?:target|expect|project|plan|forecast).*?\$[\d.]+[BMK]?\s*(?:GMV|revenue|sales|turnover).*?(?:by|in).*?(20[2-3][6-9]|203[0-5])',
            r'reach.*?\$[\d.]+[BMK]?\s*(?:to|-)?\s*\$?[\d.]+[BMK]?\s*(?:GMV|revenue|sales).*?(?:by|in).*?(20[2-3][6-9]|203[0-5])',
            r'(20[2-3][6-9]|203[0-5]).*?\$[\d.]+[BMK]?\s*(?:to|-)?\s*\$?[\d.]+[BMK]?\s*(?:GMV|revenue|sales)'  # Year first (future years)
        ]
        
        for pattern in revenue_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if match not in guidance['revenue_targets']:
                    guidance['revenue_targets'].append(match)
        
        # GMV-specific targets (future years only) - ENHANCED PATTERNS
        gmv_patterns = [
            # Standard format: "$2.5-$3B GMV by 2030"
            r'\$[\d.]+[BMK]?\s*(?:to|-)?\s*\$?[\d.]+[BMK]?\s*GMV.*?(?:by|in|target|reach|achieve).*?(20[2-3][6-9]|203[0-5])',
            # GMV first: "GMV $2.5-$3B by 2030"
            r'GMV.*?\$[\d.]+[BMK]?\s*(?:to|-)?\s*\$?[\d.]+[BMK]?.*?(?:by|in|target|reach|achieve).*?(20[2-3][6-9]|203[0-5])',
            # With target/expect/plan: "target $2.5-$3B GMV by 2030"
            r'(?:target|expect|plan|reach|achieve).*?(?:GMV|gmv).*?\$[\d.]+[BMK]?\s*(?:to|-)?\s*\$?[\d.]+[BMK]?.*?(?:by|in).*?(20[2-3][6-9]|203[0-5])',
            # Billion spelled out: "2.5 to 3 billion GMV by 2030"
            r'[\d.]+[BMK]?\s*(?:to|-)?\s*[\d.]+[BMK]?\s*(?:billion|B)\s*GMV.*?(?:by|in|target|reach|achieve).*?(20[2-3][6-9]|203[0-5])',
            # Year first: "2030 GMV target $2.5-$3B"
            r'(20[2-3][6-9]|203[0-5]).*?(?:GMV|gmv).*?\$[\d.]+[BMK]?\s*(?:to|-)?\s*\$?[\d.]+[BMK]?',
            # Range format: "$2.5 billion to $3 billion GMV by 2030"
            r'\$[\d.]+[BMK]?\s*(?:billion|B)?\s*(?:to|-)?\s*\$?[\d.]+[BMK]?\s*(?:billion|B)?\s*GMV.*?(?:by|in|target|reach).*?(20[2-3][6-9]|203[0-5])'
        ]
        
        for pattern in gmv_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Handle tuple matches (year + amount) - extract full match from text
                if isinstance(match, tuple):
                    # Find the full match in text to get context
                    full_match = re.search(pattern, text, re.IGNORECASE)
                    if full_match:
                        match_str = full_match.group(0)
                        # Extract year from tuple
                        year = match[-1] if len(match) > 1 else None
                        if year and match_str:
                            # Check for duplicates
                            existing_years = [t.get('year', '') if isinstance(t, dict) else '' for t in guidance['gmv_targets']]
                            if year not in existing_years:
                                guidance['gmv_targets'].append({'amount': match_str, 'year': year})
                else:
                    # String match - check for duplicates
                    if match not in guidance['gmv_targets']:
                        guidance['gmv_targets'].append(match)
        
        # Profitability timeline (e.g., "profitability by 2027")
        # Avoid dates like "2025" in filing dates - look for future years (2026-2035)
        profitability_patterns = [
            r'profitability.*?(?:by|in|target|reach|achieve|expect).*?(20[2-3][6-9]|203[0-5])',
            r'profitable.*?(?:by|in|target|reach|achieve|expect).*?(20[2-3][6-9]|203[0-5])',
            r'reach.*?profitability.*?(?:by|in|expect).*?(20[2-3][6-9]|203[0-5])',
            r'achieve.*?profitability.*?(?:by|in|expect).*?(20[2-3][6-9]|203[0-5])',
            r'become.*?profitable.*?(?:by|in|expect).*?(20[2-3][6-9]|203[0-5])',
            r'path.*?profitability.*?(?:by|in|expect).*?(20[2-3][6-9]|203[0-5])',
            r'(20[2-3][6-9]|203[0-5]).*?profitability',  # Year first (future years only)
            r'(20[2-3][6-9]|203[0-5]).*?profitable'  # Year first (future years only)
        ]
        
        for pattern in profitability_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                guidance['profitability_timeline'] = match.group(1)
                break
        
        # EBITDA margin targets (e.g., "20% EBITDA margin by 2030") - ENHANCED PATTERNS
        ebitda_patterns = [
            # Standard: "20% EBITDA margin by 2030"
            r'(\d+)%?\s*EBITDA.*?margin.*?(?:by|in|target|reach|achieve).*?(20[2-3][6-9]|203[0-5])',
            # Margin after: "EBITDA margin 20% by 2030"
            r'EBITDA.*?margin.*?(\d+)%?.*?(?:by|in|target|reach|achieve).*?(20[2-3][6-9]|203[0-5])',
            # With target/expect: "target 20% EBITDA margin by 2030"
            r'(?:target|expect|plan|reach|achieve).*?(\d+)%?\s*EBITDA.*?margin.*?(?:by|in).*?(20[2-3][6-9]|203[0-5])',
            # Year first: "2030 EBITDA margin target 20%"
            r'(20[2-3][6-9]|203[0-5]).*?EBITDA.*?margin.*?(\d+)%?',
            # EBITDA margin of X%: "EBITDA margin of 20% by 2030"
            r'EBITDA.*?margin.*?of\s*(\d+)%?.*?(?:by|in|target|reach).*?(20[2-3][6-9]|203[0-5])'
        ]
        
        for pattern in ebitda_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple) and len(match) == 2:
                    margin = match[0]
                    year = match[1]
                    # Avoid duplicates
                    if not any(t.get('year') == year and t.get('margin') == margin for t in guidance['ebitda_targets']):
                        guidance['ebitda_targets'].append({
                            'margin': margin,
                            'year': year
                        })
                elif isinstance(match, tuple) and len(match) == 2:
                    # Handle reversed order (year first)
                    year = match[0]
                    margin = match[1]
                    if not any(t.get('year') == year and t.get('margin') == margin for t in guidance['ebitda_targets']):
                        guidance['ebitda_targets'].append({
                            'margin': margin,
                            'year': year
                        })
        
        # Self-funded growth / No capital raises (NEW)
        self_funded_patterns = [
            r'self[-\s]?funded.*?growth',
            r'no.*?(?:further|additional).*?capital.*?(?:raise|raising)',
            r'growth.*?self[-\s]?funded',
            r'not.*?expect.*?capital.*?raise',
            r'no.*?need.*?raise.*?capital',
            r'growth.*?without.*?capital.*?raise'
        ]
        
        for pattern in self_funded_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                guidance['self_funded_growth'] = True
                guidance['no_capital_raises'] = True
                break
        
        # Forward-looking statements (context for guidance)
        forward_keywords = [
            'expect', 'anticipate', 'believe', 'plan', 'target', 'project',
            'forecast', 'guidance', 'outlook', 'strategy', 'goal'
        ]
        
        sentences = re.split(r'[.!?]\s+', text)
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in forward_keywords):
                if len(sentence.strip()) > 20 and len(sentence.strip()) < 300:
                    guidance['forward_statements'].append(sentence.strip())
                    if len(guidance['forward_statements']) >= 5:
                        break
        
        return guidance
    
    def get_filing_text(self, cik: str, accession_number: str, form_type: str = None) -> Optional[str]:
        """Get full text of a filing from SEC EDGAR by accessing actual document files"""
        try:
            # Clean accession number (remove dashes)
            acc_clean = accession_number.replace('-', '')
            
            # Get filing index to find document files
            index_url = f'{self.SEC_URL}/Archives/edgar/data/{cik}/{acc_clean}/index.json'
            
            index_response = requests.get(index_url, headers=self.headers, timeout=10)
            
            if index_response.status_code == 200:
                index_data = index_response.json()
                files = index_data.get('directory', {}).get('item', [])
                
                # Find main filing document (usually .htm or .txt, not -index.htm)
                main_files = [
                    f for f in files 
                    if isinstance(f, dict) 
                    and (f.get('name', '').endswith('.htm') or f.get('name', '').endswith('.txt'))
                    and '-index' not in f.get('name', '').lower()
                ]
                
                if main_files:
                    # Prefer .htm over .txt, or take first
                    main_file = None
                    for f in main_files:
                        if f.get('name', '').endswith('.htm'):
                            main_file = f
                            break
                    if not main_file:
                        main_file = main_files[0]
                    
                    file_name = main_file.get('name', '')
                    doc_url = f'{self.SEC_URL}/Archives/edgar/data/{cik}/{acc_clean}/{file_name}'
                    
                    doc_response = requests.get(doc_url, headers=self.headers, timeout=15)
                    
                    if doc_response.status_code == 200:
                        doc_text = doc_response.text
                        
                        # Clean HTML
                        import re
                        text = re.sub(r'<script[^>]*>.*?</script>', '', doc_text, flags=re.DOTALL | re.IGNORECASE)
                        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
                        text = re.sub(r'<[^>]+>', ' ', text)
                        text = re.sub(r'\s+', ' ', text)
                        text = re.sub(r'&[a-z]+;', ' ', text)  # Remove HTML entities
                        
                        return text[:100000]  # Limit to first 100k chars
            
            return None
        except Exception as e:
            print(f"Error fetching filing text: {e}")
            return None
    
    def extract_mda_section(self, filing_text: str) -> Optional[str]:
        """Extract MD&A (Management Discussion & Analysis) section from filing text"""
        if not filing_text:
            return None
        
        # Look for MD&A section markers (various formats)
        mda_patterns = [
            # Standard 20-F/10-K format
            r'ITEM\s+7[\.\s]*MANAGEMENT[^\n]*DISCUSSION[^\n]*ANALYSIS[^\n]*?(?=ITEM\s+(?:7A|8|10|11)|$)',
            r'ITEM\s+5[\.\s]*MANAGEMENT[^\n]*DISCUSSION[^\n]*ANALYSIS[^\n]*?(?=ITEM\s+(?:6|7|8)|$)',
            # Alternative formats
            r'MANAGEMENT[^\n]*DISCUSSION[^\n]*ANALYSIS[^\n]*?(?=ITEM\s+(?:7A|8|10|11)|$)',
            r'MD&A[^\n]*?(?=ITEM\s+(?:7A|8|10|11)|$)',
            # Look for "Operating and Financial Review" (common in 20-F)
            r'OPERATING[^\n]*FINANCIAL[^\n]*REVIEW[^\n]*?(?=ITEM\s+(?:6|7|8)|$)',
        ]
        
        for pattern in mda_patterns:
            match = re.search(pattern, filing_text, re.IGNORECASE | re.DOTALL)
            if match:
                mda_text = match.group(0)
                # Clean up
                mda_text = re.sub(r'\s+', ' ', mda_text)
                # Remove HTML entities
                mda_text = re.sub(r'&#\d+;', ' ', mda_text)
                mda_text = re.sub(r'&[a-z]+;', ' ', mda_text)
                return mda_text[:50000]  # Increased limit
        
        # If no MD&A section found, look for forward-looking sections
        # Try to find sections with guidance keywords
        guidance_sections = []
        sentences = re.split(r'[.!?]\s+', filing_text)
        
        for i, sentence in enumerate(sentences):
            sentence_lower = sentence.lower()
            if any(kw in sentence_lower for kw in ['target', 'expect', 'plan', 'guidance', '2030', '2027', 'profitability', 'gmv']):
                # Get context (surrounding sentences)
                start = max(0, i - 2)
                end = min(len(sentences), i + 3)
                context = ' '.join(sentences[start:end])
                guidance_sections.append(context)
        
        if guidance_sections:
            return ' '.join(guidance_sections[:10])[:50000]  # Combine up to 10 sections
        
        # Fallback: return portion with most guidance keywords
        return filing_text[:50000]
    
    def extract_operational_metrics(self, text: str) -> Dict:
        """Extract operational improvement metrics from MD&A text"""
        metrics = {
            'payroll_reduction': None,
            'pickup_station_percentage': None,
            'fulfillment_cost_reduction': None,
            'nps_improvement': None,
            'repurchase_rate': None,
            'geographic_expansion': None
        }
        
        if not text:
            return metrics
        
        # Payroll reduction (e.g., "4500 to 2000 employees" or "4,500 to 2,000 employees")
        payroll_patterns = [
            r'(\d{1,3}(?:,\d{3})*)\s*(?:to|-|from)\s*(\d{1,3}(?:,\d{3})*)\s*(?:employees|staff|workforce|people)',
            r'payroll.*?(\d{1,3}(?:,\d{3})*)\s*(?:to|-|from)\s*(\d{1,3}(?:,\d{3})*)\s*(?:employees|staff)',
            r'reduced.*?(\d{1,3}(?:,\d{3})*)\s*(?:to|-|from)\s*(\d{1,3}(?:,\d{3})*)\s*(?:employees|staff)'
        ]
        
        for pattern in payroll_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                from_count = int(match.group(1).replace(',', ''))
                to_count = int(match.group(2).replace(',', ''))
                if from_count > to_count:  # Valid reduction
                    metrics['payroll_reduction'] = {
                        'from': from_count,
                        'to': to_count,
                        'reduction_pct': round((1 - to_count/from_count) * 100, 1)
                    }
                    break
        
        # Pickup station percentage (e.g., "72% of deliveries at pickup stations")
        pickup_patterns = [
            r'(\d+)%?\s*(?:of|deliveries).*?pickup.*?station',
            r'pickup.*?station.*?(\d+)%?\s*(?:of|deliveries)',
            r'(\d+)%?\s*deliveries.*?pickup',
            r'deliveries.*?(\d+)%?\s*(?:at|via).*?pickup'
        ]
        
        for pattern in pickup_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                percentage = int(match.group(1))
                if 0 <= percentage <= 100:
                    metrics['pickup_station_percentage'] = percentage
                    break
        
        # Fulfillment cost reduction (e.g., "9.2% to 5.3% of GMV")
        fulfillment_patterns = [
            r'fulfillment.*?(\d+\.?\d*)%?\s*(?:to|-|from)\s*(\d+\.?\d*)%?\s*(?:of|GMV|gmv)',
            r'fulfillment.*?expenses.*?(\d+\.?\d*)%?\s*(?:to|-|from)\s*(\d+\.?\d*)%?\s*(?:of|GMV)',
            r'(\d+\.?\d*)%?\s*(?:to|-|from)\s*(\d+\.?\d*)%?\s*(?:of|GMV).*?fulfillment'
        ]
        
        for pattern in fulfillment_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                from_pct = float(match.group(1))
                to_pct = float(match.group(2))
                if from_pct > to_pct:  # Valid reduction
                    metrics['fulfillment_cost_reduction'] = {
                        'from': from_pct,
                        'to': to_pct,
                        'reduction_pct': round((1 - to_pct/from_pct) * 100, 1)
                    }
                    break
        
        # NPS improvement (e.g., "NPS increased from 46 to 64" or "Net Promoter Score 46 to 64")
        nps_patterns = [
            r'(?:NPS|Net Promoter Score).*?(\d+)\s*(?:to|-|from)\s*(\d+)',
            r'(\d+)\s*(?:to|-|from)\s*(\d+).*?(?:NPS|Net Promoter Score)',
            r'Net Promoter Score.*?(?:increased|improved).*?(\d+)\s*(?:to|-|from)\s*(\d+)'
        ]
        
        for pattern in nps_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                from_nps = int(match.group(1))
                to_nps = int(match.group(2))
                if to_nps > from_nps:  # Valid improvement
                    metrics['nps_improvement'] = {
                        'from': from_nps,
                        'to': to_nps,
                        'improvement': to_nps - from_nps
                    }
                    break
        
        # Repurchase rate (e.g., "repurchase rate increased from 39% to 43%")
        repurchase_patterns = [
            r'(?:repurchase|repeat).*?rate.*?(\d+)%?\s*(?:to|-|from)\s*(\d+)%?',
            r'(\d+)%?\s*(?:to|-|from)\s*(\d+)%?.*?(?:repurchase|repeat).*?rate',
            r'(?:90[-\s]?day|90[-\s]?day).*?repurchase.*?(\d+)%?\s*(?:to|-|from)\s*(\d+)%?'
        ]
        
        for pattern in repurchase_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                from_rate = int(match.group(1))
                to_rate = int(match.group(2))
                if to_rate > from_rate:  # Valid improvement
                    metrics['repurchase_rate'] = {
                        'from': from_rate,
                        'to': to_rate,
                        'improvement': to_rate - from_rate
                    }
                    break
        
        # Geographic expansion (e.g., "60% of orders outside capital cities")
        geo_patterns = [
            r'(\d+)%?\s*(?:of|orders).*?(?:outside|outside of).*?(?:capital|cities)',
            r'orders.*?(\d+)%?\s*(?:outside|outside of).*?(?:capital|cities)',
            r'(\d+)%?\s*(?:deliveries|orders).*?(?:outside|outside of).*?(?:capital|urban)'
        ]
        
        for pattern in geo_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                percentage = int(match.group(1))
                if 0 <= percentage <= 100:
                    metrics['geographic_expansion'] = percentage
                    break
        
        return metrics
    
    def extract_guidance(self, symbol: str) -> Dict:
        """Main method to extract guidance for a symbol"""
        result = {
            'available': False,
            'symbol': symbol,
            'cik': None,
            'guidance': {},
            'filings': [],
            'error': None
        }
        
        try:
            # Get CIK
            cik = self.get_company_cik(symbol)
            if not cik:
                result['error'] = f'CIK not found for {symbol}'
                return result
            
            result['cik'] = cik
            
            # Determine form types based on company type
            # Check if foreign issuer (files 20-F) or US company (files 10-K)
            filings = self.get_recent_filings(cik, limit=20)
            
            if not filings:
                result['error'] = 'No relevant filings found'
                return result
            
            result['filings'] = filings
            
            # Phase 2: Fetch and parse actual filing text
            # Focus on most recent 20-F (annual) and recent 6-K filings
            annual_filings = [f for f in filings if f['form'] == '20-F']
            quarterly_filings = [f for f in filings if f['form'] == '6-K'][:3]  # Last 3 quarterly
            
            combined_text = ''
            
            # Try to get text from most recent annual filing
            if annual_filings:
                latest_annual = annual_filings[0]
                filing_text = self.get_filing_text(cik, latest_annual['accession'], latest_annual['form'])
                if filing_text:
                    mda_text = self.extract_mda_section(filing_text)
                    if mda_text:
                        combined_text += mda_text + ' '
            
            # Try to get text from recent quarterly filings
            for q_filing in quarterly_filings:
                filing_text = self.get_filing_text(cik, q_filing['accession'], q_filing['form'])
                if filing_text:
                    # For 6-K, look for earnings release or guidance sections
                    combined_text += filing_text[:5000] + ' '  # First 5k chars
            
            # Extract guidance from combined text using AI (agent generates directly)
            if combined_text:
                # AI-driven extraction (agent generates during workflow execution)
                guidance = self.extract_guidance_ai(combined_text, symbol)
                # Store text for agent generation (agent will generate extraction)
                result['_sec_text_for_ai'] = combined_text[:10000]  # Store first 10k chars for agent
                # If agent didn't populate, fall back to pattern matching
                if not guidance.get('gmv_targets') and not guidance.get('revenue_targets') and not guidance.get('profitability_timeline'):
                    # Fallback to pattern matching if AI extraction didn't work
                    guidance = self.extract_guidance_from_text(combined_text)
                    operational_metrics = self.extract_operational_metrics(combined_text)
                    guidance['operational_metrics'] = operational_metrics
            else:
                # Fallback to filing descriptions
                combined_text = ' '.join([f.get('description', '') for f in filings])
                guidance = self.extract_guidance_ai(combined_text, symbol)
                result['_sec_text_for_ai'] = combined_text[:10000]  # Store for agent
                # Fallback to pattern matching if needed
                if not guidance.get('gmv_targets') and not guidance.get('revenue_targets') and not guidance.get('profitability_timeline'):
                    guidance = self.extract_guidance_from_text(combined_text)
                    operational_metrics = self.extract_operational_metrics(combined_text)
                    guidance['operational_metrics'] = operational_metrics
            
            result['guidance'] = guidance
            result['available'] = True
            result['text_parsed'] = len(combined_text) > 100  # Indicate if we got actual text
            
            return result
            
        except Exception as e:
            result['error'] = str(e)
            return result
    
    def get_guidance_summary(self, guidance_data: Dict) -> str:
        """Generate human-readable guidance summary"""
        if not guidance_data.get('available'):
            return "Management guidance not available from SEC filings."
        
        guidance = guidance_data.get('guidance', {})
        summary_parts = []
        
        # Revenue/GMV targets
        revenue_targets = guidance.get('revenue_targets', [])
        gmv_targets = guidance.get('gmv_targets', [])
        
        if gmv_targets:
            # Handle both string and dict formats
            gmv_strs = []
            for target in gmv_targets:
                if isinstance(target, dict):
                    gmv_strs.append(f"${target.get('amount', 'N/A')} by {target.get('year', 'N/A')}")
                else:
                    gmv_strs.append(str(target))
            if gmv_strs:
                summary_parts.append(f"GMV targets: {', '.join(gmv_strs)}")
        elif revenue_targets:
            summary_parts.append(f"Revenue targets: {', '.join([str(t) for t in revenue_targets])}")
        
        # Profitability timeline
        profitability = guidance.get('profitability_timeline')
        if profitability:
            summary_parts.append(f"Profitability target: {profitability}")
        
        # EBITDA targets
        ebitda_targets = guidance.get('ebitda_targets', [])
        if ebitda_targets:
            ebitda_str = ', '.join([f"{t['margin']}% by {t['year']}" for t in ebitda_targets])
            summary_parts.append(f"EBITDA margin targets: {ebitda_str}")
        
        # Self-funded growth
        if guidance.get('self_funded_growth') or guidance.get('no_capital_raises'):
            summary_parts.append("Self-funded growth commitment (no further capital raises expected)")
        
        # Operational metrics
        operational_metrics = guidance.get('operational_metrics', {})
        if operational_metrics:
            op_parts = []
            if operational_metrics.get('payroll_reduction'):
                pr = operational_metrics['payroll_reduction']
                op_parts.append(f"Payroll reduction: {pr['from']:,} to {pr['to']:,} employees ({pr['reduction_pct']:.1f}% reduction)")
            
            if operational_metrics.get('pickup_station_percentage'):
                op_parts.append(f"Pickup stations: {operational_metrics['pickup_station_percentage']}% of deliveries")
            
            if operational_metrics.get('fulfillment_cost_reduction'):
                fcr = operational_metrics['fulfillment_cost_reduction']
                op_parts.append(f"Fulfillment costs: {fcr['from']:.1f}% to {fcr['to']:.1f}% of GMV ({fcr['reduction_pct']:.1f}% reduction)")
            
            if operational_metrics.get('nps_improvement'):
                nps = operational_metrics['nps_improvement']
                op_parts.append(f"Net Promoter Score: {nps['from']} to {nps['to']} (+{nps['improvement']} points)")
            
            if operational_metrics.get('repurchase_rate'):
                rr = operational_metrics['repurchase_rate']
                op_parts.append(f"Repurchase rate: {rr['from']}% to {rr['to']}% (+{rr['improvement']} points)")
            
            if operational_metrics.get('geographic_expansion'):
                op_parts.append(f"Geographic expansion: {operational_metrics['geographic_expansion']}% of orders outside capital cities")
            
            if op_parts:
                summary_parts.append("Operational improvements: " + "; ".join(op_parts))
        
        if summary_parts:
            return "Management guidance from SEC filings: " + ". ".join(summary_parts) + "."
        else:
            return "Management guidance found in SEC filings but specific targets require full filing text parsing."

