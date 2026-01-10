"""
SEO Scanner Service
Enhanced version with better error handling and scoring
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
from typing import Tuple, Optional, Dict, List
import re

class SEOScanner:
    """Comprehensive SEO scanner for website analysis"""
    
    def __init__(self, supabase_client):
        """Initialize with Supabase client"""
        self.supabase = supabase_client
        self.timeout = 15  # seconds
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def scan_url(self, user_id: str, url: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Scan a URL and store comprehensive results
        
        Returns:
            Tuple of (scan_id, error_message)
        """
        try:
            # Normalize URL
            url = self._normalize_url(url)
            
            # Parse domain
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path
            
            print(f"🔍 Scanning: {url}")
            
            # Fetch page with timing
            start_time = time.time()
            response = requests.get(
                url, 
                headers=self.headers, 
                timeout=self.timeout,
                allow_redirects=True,
                verify=True
            )
            load_time = int((time.time() - start_time) * 1000)
            
            if response.status_code != 200:
                return None, f"HTTP {response.status_code} - Page not accessible"
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract comprehensive data
            seo_data = self._extract_seo_data(soup, url, response)
            seo_data['load_time_ms'] = load_time
            seo_data['http_status'] = response.status_code
            seo_data['page_size_kb'] = len(response.content) // 1024
            seo_data['has_ssl'] = url.startswith('https://')
            
            # Calculate scores
            scores = self._calculate_scores(seo_data)
            
            # Identify issues
            issues = self._identify_issues(seo_data)
            
            # Prepare database entry
            scan_data = {
                'user_id': user_id,
                'url': url,
                'domain': domain,
                'title': seo_data['title'][:500],
                'meta_description': seo_data['description'][:500],
                'overall_score': scores['overall'],
                'technical_score': scores['technical'],
                'content_score': scores['content'],
                'performance_score': scores['performance'],
                'http_status': response.status_code,
                'load_time_ms': load_time,
                'page_size_kb': len(response.content) // 1024,
                'word_count': seo_data['word_count'],
                'image_count': seo_data['image_count'],
                'link_count': seo_data['link_count'],
                'h1_count': seo_data['h1_count'],
                'h2_count': seo_data.get('h2_count', 0),
                'has_ssl': seo_data['has_ssl'],
                'is_mobile_friendly': seo_data.get('is_mobile_friendly', True),
                'has_robots_txt': seo_data.get('has_robots_txt', False),
                'has_sitemap': seo_data.get('has_sitemap', False),
                'issues_detail': issues,
                'meta_keywords': seo_data.get('keywords', ''),
                'canonical_url': seo_data.get('canonical', ''),
                'og_title': seo_data.get('og_title', ''),
                'og_description': seo_data.get('og_description', ''),
                'status': 'completed'
            }
            
            # Store in database
            result = self.supabase.table('seo_scans').insert(scan_data).execute()
            
            if result.data and len(result.data) > 0:
                scan_id = result.data[0]['id']
                
                # Update user stats
                try:
                    self.supabase.rpc('increment_monthly_scans', {'user_id_param': user_id}).execute()
                except Exception as e:
                    print(f"⚠️ Failed to update scan count: {e}")
                
                print(f"✅ Scan completed successfully - ID: {scan_id}")
                return scan_id, None
            else:
                return None, "Failed to save scan results"
                
        except requests.exceptions.Timeout:
            return None, f"Request timeout after {self.timeout} seconds"
        except requests.exceptions.SSLError:
            return None, "SSL certificate error"
        except requests.exceptions.ConnectionError:
            return None, "Failed to connect to website"
        except requests.exceptions.RequestException as e:
            return None, f"Network error: {str(e)}"
        except Exception as e:
            print(f"❌ Scan error: {str(e)}")
            return None, f"Scan error: {str(e)}"
    
    def _normalize_url(self, url: str) -> str:
        """Normalize URL format"""
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url
    
    def _extract_seo_data(self, soup: BeautifulSoup, url: str, response) -> Dict:
        """Extract comprehensive SEO data from page"""
        data = {}
        
        # Title
        title_tag = soup.find('title')
        data['title'] = title_tag.get_text().strip() if title_tag else ''
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            meta_desc = soup.find('meta', attrs={'property': 'og:description'})
        data['description'] = meta_desc.get('content', '').strip() if meta_desc else ''
        
        # Meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        data['keywords'] = meta_keywords.get('content', '').strip() if meta_keywords else ''
        
        # Canonical URL
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        data['canonical'] = canonical.get('href', '') if canonical else ''
        
        # Open Graph tags
        og_title = soup.find('meta', attrs={'property': 'og:title'})
        data['og_title'] = og_title.get('content', '') if og_title else ''
        
        og_desc = soup.find('meta', attrs={'property': 'og:description'})
        data['og_description'] = og_desc.get('content', '') if og_desc else ''
        
        # Heading tags
        data['h1_count'] = len(soup.find_all('h1'))
        data['h2_count'] = len(soup.find_all('h2'))
        data['h1_tags'] = [h1.get_text().strip() for h1 in soup.find_all('h1')]
        
        # Images
        images = soup.find_all('img')
        data['image_count'] = len(images)
        data['images_without_alt'] = sum(1 for img in images if not img.get('alt'))
        
        # Links
        links = soup.find_all('a', href=True)
        data['link_count'] = len(links)
        data['internal_links'] = sum(1 for link in links if self._is_internal_link(link.get('href'), url))
        data['external_links'] = data['link_count'] - data['internal_links']
        
        # Content analysis
        # Remove script and style elements
        for script in soup(['script', 'style', 'nav', 'footer', 'header']):
            script.decompose()
        
        text = soup.get_text()
        words = text.split()
        data['word_count'] = len(words)
        data['text_content'] = ' '.join(words[:100])  # First 100 words for preview
        
        # Mobile viewport
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        data['is_mobile_friendly'] = viewport is not None
        
        # Check for common resources
        data['has_robots_txt'] = self._check_robots_txt(url)
        data['has_sitemap'] = self._check_sitemap(url)
        
        return data
    
    def _is_internal_link(self, href: str, base_url: str) -> bool:
        """Check if link is internal"""
        if not href:
            return False
        if href.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
            return False
        
        parsed_base = urlparse(base_url)
        parsed_href = urlparse(urljoin(base_url, href))
        
        return parsed_base.netloc == parsed_href.netloc
    
    def _check_robots_txt(self, url: str) -> bool:
        """Check if robots.txt exists"""
        try:
            parsed = urlparse(url)
            robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
            response = requests.get(robots_url, headers=self.headers, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _check_sitemap(self, url: str) -> bool:
        """Check if sitemap.xml exists"""
        try:
            parsed = urlparse(url)
            sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"
            response = requests.get(sitemap_url, headers=self.headers, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _calculate_scores(self, data: Dict) -> Dict[str, int]:
        """Calculate comprehensive SEO scores"""
        scores = {
            'technical': 100,
            'content': 100,
            'performance': 100
        }
        
        # ═══════════════════════════════════════════════════════
        # TECHNICAL SCORE
        # ═══════════════════════════════════════════════════════
        
        # SSL/HTTPS (20 points)
        if not data.get('has_ssl'):
            scores['technical'] -= 20
        
        # H1 tags (15 points)
        h1_count = data.get('h1_count', 0)
        if h1_count == 0:
            scores['technical'] -= 15
        elif h1_count > 1:
            scores['technical'] -= 8
        
        # Mobile friendly (10 points)
        if not data.get('is_mobile_friendly'):
            scores['technical'] -= 10
        
        # Robots.txt (5 points)
        if not data.get('has_robots_txt'):
            scores['technical'] -= 5
        
        # Sitemap (5 points)
        if not data.get('has_sitemap'):
            scores['technical'] -= 5
        
        # Canonical URL (5 points)
        if not data.get('canonical'):
            scores['technical'] -= 5
        
        # ═══════════════════════════════════════════════════════
        # CONTENT SCORE
        # ═══════════════════════════════════════════════════════
        
        # Title tag (25 points)
        title = data.get('title', '')
        if not title:
            scores['content'] -= 25
        elif len(title) < 30:
            scores['content'] -= 15
        elif len(title) > 60:
            scores['content'] -= 10
        
        # Meta description (25 points)
        description = data.get('description', '')
        if not description:
            scores['content'] -= 25
        elif len(description) < 100:
            scores['content'] -= 15
        elif len(description) > 160:
            scores['content'] -= 10
        
        # Word count (20 points)
        word_count = data.get('word_count', 0)
        if word_count < 300:
            scores['content'] -= 20
        elif word_count < 600:
            scores['content'] -= 10
        
        # Images with alt text (15 points)
        images_without_alt = data.get('images_without_alt', 0)
        image_count = data.get('image_count', 0)
        if image_count > 0:
            alt_ratio = images_without_alt / image_count
            if alt_ratio > 0.5:
                scores['content'] -= 15
            elif alt_ratio > 0.3:
                scores['content'] -= 8
        
        # Open Graph tags (10 points)
        if not data.get('og_title'):
            scores['content'] -= 5
        if not data.get('og_description'):
            scores['content'] -= 5
        
        # ═══════════════════════════════════════════════════════
        # PERFORMANCE SCORE
        # ═══════════════════════════════════════════════════════
        
        # Load time (50 points)
        load_time = data.get('load_time_ms', 0)
        if load_time > 5000:
            scores['performance'] -= 50
        elif load_time > 3000:
            scores['performance'] -= 35
        elif load_time > 2000:
            scores['performance'] -= 20
        elif load_time > 1000:
            scores['performance'] -= 10
        
        # Page size (30 points)
        page_size = data.get('page_size_kb', 0)
        if page_size > 5000:  # 5MB
            scores['performance'] -= 30
        elif page_size > 3000:  # 3MB
            scores['performance'] -= 20
        elif page_size > 2000:  # 2MB
            scores['performance'] -= 10
        
        # Image count (20 points)
        if image_count > 50:
            scores['performance'] -= 20
        elif image_count > 30:
            scores['performance'] -= 10
        
        # Ensure scores don't go below 0
        for key in scores:
            scores[key] = max(0, scores[key])
        
        # Calculate overall score (weighted average)
        scores['overall'] = int(
            (scores['technical'] * 0.35 + 
             scores['content'] * 0.40 + 
             scores['performance'] * 0.25)
        )
        
        return scores
    
    def _identify_issues(self, data: Dict) -> Dict[str, List[str]]:
        """Identify and categorize SEO issues"""
        issues = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }
        
        # ═══════════════════════════════════════════════════════
        # CRITICAL ISSUES
        # ═══════════════════════════════════════════════════════
        
        if not data.get('has_ssl'):
            issues['critical'].append('🔒 Website not using HTTPS - Security risk')
        
        if not data.get('title'):
            issues['critical'].append('📄 Missing title tag - Critical for SEO')
        
        if data.get('http_status', 200) != 200:
            issues['critical'].append(f'⚠️ HTTP {data.get("http_status")} error')
        
        # ═══════════════════════════════════════════════════════
        # HIGH PRIORITY ISSUES
        # ═══════════════════════════════════════════════════════
        
        h1_count = data.get('h1_count', 0)
        if h1_count == 0:
            issues['high'].append('📑 No H1 tag found - Important for page structure')
        elif h1_count > 1:
            issues['high'].append(f'📑 Multiple H1 tags ({h1_count}) - Should have only one')
        
        if not data.get('description'):
            issues['high'].append('📝 Missing meta description - Impacts click-through rate')
        
        if not data.get('is_mobile_friendly'):
            issues['high'].append('📱 Not mobile-friendly - Missing viewport meta tag')
        
        load_time = data.get('load_time_ms', 0)
        if load_time > 3000:
            issues['high'].append(f'⏱️ Slow page load time ({load_time}ms) - Aim for under 2000ms')
        
        # ═══════════════════════════════════════════════════════
        # MEDIUM PRIORITY ISSUES
        # ═══════════════════════════════════════════════════════
        
        title = data.get('title', '')
        if title and len(title) < 30:
            issues['medium'].append(f'📏 Title too short ({len(title)} chars) - Aim for 30-60 characters')
        elif title and len(title) > 60:
            issues['medium'].append(f'📏 Title too long ({len(title)} chars) - May be truncated in search results')
        
        description = data.get('description', '')
        if description and len(description) < 100:
            issues['medium'].append(f'📏 Meta description too short ({len(description)} chars) - Aim for 120-160')
        elif description and len(description) > 160:
            issues['medium'].append(f'📏 Meta description too long ({len(description)} chars) - Will be truncated')
        
        word_count = data.get('word_count', 0)
        if word_count < 300:
            issues['medium'].append(f'📊 Low word count ({word_count}) - Consider adding more content')
        
        if not data.get('canonical'):
            issues['medium'].append('🔗 Missing canonical URL - Helps prevent duplicate content')
        
        if not data.get('og_title'):
            issues['medium'].append('📱 Missing Open Graph title - Important for social sharing')
        
        page_size = data.get('page_size_kb', 0)
        if page_size > 3000:
            issues['medium'].append(f'💾 Large page size ({page_size}KB) - Consider optimization')
        
        # ═══════════════════════════════════════════════════════
        # LOW PRIORITY ISSUES
        # ═══════════════════════════════════════════════════════
        
        images_without_alt = data.get('images_without_alt', 0)
        if images_without_alt > 0:
            issues['low'].append(f'🖼️ {images_without_alt} images missing alt text - Important for accessibility')
        
        if not data.get('has_robots_txt'):
            issues['low'].append('🤖 No robots.txt file found - Consider adding one')
        
        if not data.get('has_sitemap'):
            issues['low'].append('🗺️ No sitemap.xml found - Helps search engines crawl your site')
        
        if not data.get('keywords'):
            issues['low'].append('🏷️ No meta keywords defined (optional but can help)')
        
        external_links = data.get('external_links', 0)
        if external_links > 100:
            issues['low'].append(f'🔗 Many external links ({external_links}) - Review link quality')
        
        return issues