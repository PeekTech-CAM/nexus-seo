"""
NEXUS SEO INTELLIGENCE - SEO Scanning Engine
Production-grade web scraping and SEO analysis
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
from typing import Dict, List, Optional, Tuple
import re
import logging
from datetime import datetime
from supabase import Client

# Configure logging
logger = logging.getLogger(__name__)

# Request configuration
HEADERS = {
    'User-Agent': 'NexusSEO-Bot/1.0 (SEO Analysis Tool; +https://nexusseo.com/bot)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

TIMEOUT = 15  # seconds
MAX_PAGE_SIZE = 10 * 1024 * 1024  # 10MB


class SEOScanner:
    """
    Comprehensive SEO scanning and analysis engine.
    Performs technical, on-page, and content analysis.
    """
    
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    
    def scan_url(self, user_id: str, url: str) -> Optional[str]:
        """
        Execute full SEO scan of a URL.
        
        Args:
            user_id: User performing the scan
            url: Target URL to analyze
        
        Returns:
            Scan ID if successful, None if failed
        """
        # Validate and normalize URL
        url = self._normalize_url(url)
        if not url:
            logger.error(f"Invalid URL provided: {url}")
            return None
        
        domain = urlparse(url).netloc
        
        # Check scan limits
        if not self._check_scan_limits(user_id):
            logger.warning(f"User {user_id} exceeded scan limits")
            return None
        
        # Create scan record
        scan_id = self._create_scan_record(user_id, url, domain)
        
        try:
            # Update status to processing
            self._update_scan_status(scan_id, 'processing')
            
            start_time = time.time()
            
            # Fetch page content
            html_content, http_status, load_time = self._fetch_page(url)
            
            if not html_content:
                self._mark_scan_failed(scan_id, f"Failed to fetch page: HTTP {http_status}")
                return None
            
            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Run all analysis modules
            metadata = self._extract_metadata(soup, url)
            technical = self._analyze_technical(url, http_status, html_content, load_time)
            content = self._analyze_content(soup)
            images = self._analyze_images(soup, url)
            links = self._analyze_links(soup, url)
            structured_data = self._extract_structured_data(soup)
            issues = self._identify_issues(metadata, technical, content, images)
            
            # Calculate scores
            scores = self._calculate_scores(metadata, technical, content, images, issues)
            
            # Prepare scan data
            scan_data = {
                **metadata,
                **technical,
                **content,
                **scores,
                **issues,
                'structured_data': structured_data,
                'issues_detail': self._format_issues_detail(issues),
                'completed_at': datetime.utcnow().isoformat(),
                'duration_seconds': int(time.time() - start_time),
                'status': 'completed'
            }
            
            # Update scan record
            self.supabase.table('scans').update(scan_data).eq('id', scan_id).execute()
            
            # Increment user scan counter
            self._increment_scan_counter(user_id)
            
            logger.info(f"Scan completed successfully: {scan_id}")
            return scan_id
            
        except Exception as e:
            logger.error(f"Error during scan {scan_id}: {e}")
            self._mark_scan_failed(scan_id, str(e))
            return None
    
    def _normalize_url(self, url: str) -> Optional[str]:
        """
        Validate and normalize URL.
        """
        try:
            # Add schema if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            parsed = urlparse(url)
            
            # Validate
            if not parsed.scheme or not parsed.netloc:
                return None
            
            # Ensure https
            if parsed.scheme == 'http':
                url = url.replace('http://', 'https://', 1)
            
            return url
            
        except Exception as e:
            logger.error(f"Error normalizing URL: {e}")
            return None
    
    def _check_scan_limits(self, user_id: str) -> bool:
        """
        Check if user can perform another scan.
        """
        try:
            profile = self.supabase.table('profiles').select(
                'tier, monthly_scan_limit, monthly_scans_used'
            ).eq('id', user_id).single().execute()
            
            if not profile.data:
                return False
            
            used = profile.data['monthly_scans_used']
            limit = profile.data['monthly_scan_limit']
            
            return used < limit
            
        except Exception as e:
            logger.error(f"Error checking scan limits: {e}")
            return False
    
    def _create_scan_record(self, user_id: str, url: str, domain: str) -> str:
        """
        Create initial scan record in database.
        """
        try:
            result = self.supabase.table('scans').insert({
                'user_id': user_id,
                'url': url,
                'domain': domain,
                'status': 'pending',
                'started_at': datetime.utcnow().isoformat()
            }).execute()
            
            return result.data[0]['id']
            
        except Exception as e:
            logger.error(f"Error creating scan record: {e}")
            raise
    
    def _update_scan_status(self, scan_id: str, status: str):
        """
        Update scan status.
        """
        self.supabase.table('scans').update({
            'status': status
        }).eq('id', scan_id).execute()
    
    def _mark_scan_failed(self, scan_id: str, error_message: str):
        """
        Mark scan as failed with error message.
        """
        self.supabase.table('scans').update({
            'status': 'failed',
            'error_message': error_message,
            'completed_at': datetime.utcnow().isoformat()
        }).eq('id', scan_id).execute()
    
    def _fetch_page(self, url: str) -> Tuple[Optional[str], int, int]:
        """
        Fetch page content with error handling.
        
        Returns:
            Tuple of (html_content, http_status, load_time_ms)
        """
        try:
            start = time.time()
            response = self.session.get(
                url,
                timeout=TIMEOUT,
                allow_redirects=True,
                stream=True
            )
            load_time = int((time.time() - start) * 1000)
            
            # Check content length
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > MAX_PAGE_SIZE:
                logger.warning(f"Page too large: {content_length} bytes")
                return None, response.status_code, load_time
            
            # Get content
            content = response.text
            
            return content, response.status_code, load_time
            
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None, 0, 0
    
    def _extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict:
        """
        Extract page metadata (title, description, etc.)
        """
        # Title
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else None
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '').strip() if meta_desc else None
        
        # H1 tags
        h1_tags = [h1.get_text().strip() for h1 in soup.find_all('h1')]
        
        # Canonical
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        canonical_url = canonical.get('href') if canonical else None
        
        # Robots meta
        robots_meta = soup.find('meta', attrs={'name': 'robots'})
        robots = robots_meta.get('content', '').strip() if robots_meta else None
        
        return {
            'title': title,
            'meta_description': description,
            'h1_tags': h1_tags,
            'canonical_url': canonical_url,
            'robots_meta': robots
        }
    
    def _analyze_technical(self, url: str, http_status: int, html: str, load_time: int) -> Dict:
        """
        Analyze technical SEO factors.
        """
        parsed = urlparse(url)
        
        # SSL check
        has_ssl = parsed.scheme == 'https'
        
        # Page size
        page_size_kb = len(html.encode('utf-8')) / 1024
        
        # Simple mobile-friendly check (viewport meta tag)
        has_viewport = 'viewport' in html.lower()
        
        return {
            'http_status': http_status,
            'has_ssl': has_ssl,
            'page_size_kb': int(page_size_kb),
            'load_time_ms': load_time,
            'is_mobile_friendly': has_viewport
        }
    
    def _analyze_content(self, soup: BeautifulSoup) -> Dict:
        """
        Analyze content quality and structure.
        """
        # Remove script and style elements
        for script in soup(['script', 'style', 'noscript']):
            script.decompose()
        
        # Get text content
        text = soup.get_text(separator=' ', strip=True)
        
        # Word count
        words = text.split()
        word_count = len(words)
        
        # Heading structure
        headings = {
            'h1': len(soup.find_all('h1')),
            'h2': len(soup.find_all('h2')),
            'h3': len(soup.find_all('h3')),
            'h4': len(soup.find_all('h4')),
            'h5': len(soup.find_all('h5')),
            'h6': len(soup.find_all('h6'))
        }
        
        return {
            'word_count': word_count,
            'heading_counts': headings
        }
    
    def _analyze_images(self, soup: BeautifulSoup, base_url: str) -> Dict:
        """
        Analyze image optimization.
        """
        images = soup.find_all('img')
        image_count = len(images)
        
        images_without_alt = 0
        large_images = 0
        
        for img in images:
            # Check alt tag
            if not img.get('alt'):
                images_without_alt += 1
            
            # Check if image has dimension attributes
            width = img.get('width')
            height = img.get('height')
            
            # Simple check for potentially large images
            if width and height:
                try:
                    if int(width) > 2000 or int(height) > 2000:
                        large_images += 1
                except (ValueError, TypeError):
                    pass
        
        return {
            'image_count': image_count,
            'images_without_alt': images_without_alt,
            'potentially_large_images': large_images
        }
    
    def _analyze_links(self, soup: BeautifulSoup, base_url: str) -> Dict:
        """
        Analyze internal and external links.
        """
        links = soup.find_all('a', href=True)
        
        internal_links = 0
        external_links = 0
        broken_links = 0
        
        base_domain = urlparse(base_url).netloc
        
        for link in links:
            href = link.get('href', '')
            
            # Skip anchors and javascript
            if href.startswith('#') or href.startswith('javascript:'):
                continue
            
            # Normalize URL
            full_url = urljoin(base_url, href)
            link_domain = urlparse(full_url).netloc
            
            if link_domain == base_domain:
                internal_links += 1
            else:
                external_links += 1
        
        return {
            'link_count': len(links),
            'internal_links': internal_links,
            'external_links': external_links
        }
    
    def _extract_structured_data(self, soup: BeautifulSoup) -> Dict:
        """
        Extract structured data (JSON-LD, microdata).
        """
        structured = {
            'json_ld': [],
            'has_schema': False
        }
        
        # JSON-LD
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            try:
                import json
                data = json.loads(script.string)
                structured['json_ld'].append(data)
                structured['has_schema'] = True
            except (json.JSONDecodeError, AttributeError):
                pass
        
        return structured
    
    def _identify_issues(self, metadata: Dict, technical: Dict, content: Dict, images: Dict) -> Dict:
        """
        Identify SEO issues and categorize by severity.
        """
        critical = []
        high = []
        medium = []
        low = []
        
        # Critical issues
        if not metadata.get('title'):
            critical.append('Missing page title')
        
        if not technical.get('has_ssl'):
            critical.append('No HTTPS encryption')
        
        if technical.get('http_status') != 200:
            critical.append(f"HTTP status: {technical.get('http_status')}")
        
        # High priority issues
        if not metadata.get('meta_description'):
            high.append('Missing meta description')
        
        if not metadata.get('h1_tags'):
            high.append('No H1 heading found')
        elif len(metadata['h1_tags']) > 1:
            high.append(f"Multiple H1 tags ({len(metadata['h1_tags'])})")
        
        if content.get('word_count', 0) < 300:
            high.append('Thin content (< 300 words)')
        
        # Medium priority issues
        if metadata.get('title') and len(metadata['title']) > 60:
            medium.append('Title tag too long (> 60 chars)')
        
        if metadata.get('meta_description') and len(metadata['meta_description']) > 160:
            medium.append('Meta description too long (> 160 chars)')
        
        if technical.get('load_time_ms', 0) > 3000:
            medium.append(f"Slow page load ({technical['load_time_ms']}ms)")
        
        if technical.get('page_size_kb', 0) > 2000:
            medium.append(f"Large page size ({technical['page_size_kb']}KB)")
        
        # Low priority issues
        if images.get('images_without_alt', 0) > 0:
            low.append(f"{images['images_without_alt']} images missing alt text")
        
        if not technical.get('is_mobile_friendly'):
            low.append('No viewport meta tag')
        
        return {
            'critical_issues': len(critical),
            'high_issues': len(high),
            'medium_issues': len(medium),
            'low_issues': len(low),
            '_critical_list': critical,
            '_high_list': high,
            '_medium_list': medium,
            '_low_list': low
        }
    
    def _format_issues_detail(self, issues: Dict) -> Dict:
        """
        Format detailed issues list for storage.
        """
        return {
            'critical': issues.get('_critical_list', []),
            'high': issues.get('_high_list', []),
            'medium': issues.get('_medium_list', []),
            'low': issues.get('_low_list', [])
        }
    
    def _calculate_scores(self, metadata: Dict, technical: Dict, content: Dict, images: Dict, issues: Dict) -> Dict:
        """
        Calculate SEO scores (0-100) for different aspects.
        """
        # Technical score
        technical_points = 100
        if not technical.get('has_ssl'):
            technical_points -= 30
        if technical.get('http_status') != 200:
            technical_points -= 25
        if technical.get('load_time_ms', 0) > 3000:
            technical_points -= 15
        if not technical.get('is_mobile_friendly'):
            technical_points -= 10
        technical_score = max(0, technical_points)
        
        # Content score
        content_points = 100
        if not metadata.get('title'):
            content_points -= 25
        if not metadata.get('meta_description'):
            content_points -= 20
        if not metadata.get('h1_tags'):
            content_points -= 20
        elif len(metadata['h1_tags']) > 1:
            content_points -= 10
        if content.get('word_count', 0) < 300:
            content_points -= 25
        content_score = max(0, content_points)
        
        # Performance score
        perf_points = 100
        load_time = technical.get('load_time_ms', 0)
        if load_time > 5000:
            perf_points -= 50
        elif load_time > 3000:
            perf_points -= 30
        elif load_time > 1000:
            perf_points -= 15
        
        page_size = technical.get('page_size_kb', 0)
        if page_size > 3000:
            perf_points -= 30
        elif page_size > 2000:
            perf_points -= 20
        elif page_size > 1000:
            perf_points -= 10
        performance_score = max(0, perf_points)
        
        # Accessibility score
        access_points = 100
        if images.get('images_without_alt', 0) > 0:
            access_points -= min(40, images['images_without_alt'] * 5)
        if not metadata.get('h1_tags'):
            access_points -= 20
        accessibility_score = max(0, access_points)
        
        # Overall score (weighted average)
        overall_score = int(
            technical_score * 0.35 +
            content_score * 0.35 +
            performance_score * 0.20 +
            accessibility_score * 0.10
        )
        
        return {
            'overall_score': overall_score,
            'technical_score': technical_score,
            'content_score': content_score,
            'performance_score': performance_score,
            'accessibility_score': accessibility_score
        }
    
    def _increment_scan_counter(self, user_id: str):
        """
        Increment user's monthly scan counter.
        """
        try:
            profile = self.supabase.table('profiles').select('monthly_scans_used').eq('id', user_id).single().execute()
            
            current = profile.data['monthly_scans_used']
            
            self.supabase.table('profiles').update({
                'monthly_scans_used': current + 1
            }).eq('id', user_id).execute()
            
        except Exception as e:
            logger.error(f"Error incrementing scan counter: {e}")