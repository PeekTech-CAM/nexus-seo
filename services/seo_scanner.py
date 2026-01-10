"""
SEO Scanner Service
Simple, working version for scanning websites
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
from typing import Tuple, Optional, Dict

class SEOScanner:
    """Simple SEO scanner for website analysis"""
    
    def __init__(self, supabase_client):
        """Initialize with Supabase client"""
        self.supabase = supabase_client
    
    def scan_url(self, user_id: str, url: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Scan a URL and store results
        
        Returns:
            Tuple of (scan_id, error_message)
        """
        try:
            # Validate URL
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Parse domain
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path
            
            # Fetch page
            start_time = time.time()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            load_time = int((time.time() - start_time) * 1000)
            
            if response.status_code != 200:
                return None, f"HTTP {response.status_code}"
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract data
            title = soup.find('title')
            title_text = title.get_text().strip() if title else ''
            
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content', '') if meta_desc else ''
            
            # Count elements
            h1_tags = soup.find_all('h1')
            images = soup.find_all('img')
            links = soup.find_all('a')
            
            # Get text content
            text = soup.get_text()
            words = len(text.split())
            
            # Calculate scores
            scores = self._calculate_scores({
                'title': title_text,
                'description': description,
                'h1_count': len(h1_tags),
                'images': len(images),
                'links': len(links),
                'words': words,
                'has_ssl': url.startswith('https://'),
                'load_time': load_time
            })
            
            # Identify issues
            issues = self._identify_issues({
                'title': title_text,
                'description': description,
                'h1_count': len(h1_tags),
                'images': images,
                'has_ssl': url.startswith('https://'),
            })
            
            # Store in database
            scan_data = {
                'user_id': user_id,
                'url': url,
                'domain': domain,
                'title': title_text[:500],
                'meta_description': description[:500],
                'overall_score': scores['overall'],
                'technical_score': scores['technical'],
                'content_score': scores['content'],
                'performance_score': scores['performance'],
                'http_status': response.status_code,
                'load_time_ms': load_time,
                'page_size_kb': len(response.content) // 1024,
                'word_count': words,
                'image_count': len(images),
                'link_count': len(links),
                'h1_count': len(h1_tags),
                'has_ssl': url.startswith('https://'),
                'is_mobile_friendly': True,  # Simplified
                'issues_detail': issues,
                'status': 'completed'
            }
            
            result = self.supabase.table('scans').insert(scan_data).execute()
            
            if result.data:
                scan_id = result.data[0]['id']
                
                # Update user stats
                try:
                    self.supabase.rpc('increment_monthly_scans', {'user_id_param': user_id}).execute()
                except:
                    pass
                
                return scan_id, None
            else:
                return None, "Failed to save scan"
                
        except requests.exceptions.Timeout:
            return None, "Request timeout"
        except requests.exceptions.RequestException as e:
            return None, f"Network error: {str(e)}"
        except Exception as e:
            return None, f"Scan error: {str(e)}"
    
    def _calculate_scores(self, data: Dict) -> Dict[str, int]:
        """Calculate SEO scores"""
        scores = {
            'technical': 100,
            'content': 100,
            'performance': 100
        }
        
        # Technical score
        if not data.get('has_ssl'):
            scores['technical'] -= 20
        if data.get('h1_count', 0) == 0:
            scores['technical'] -= 10
        elif data.get('h1_count', 0) > 1:
            scores['technical'] -= 5
        
        # Content score
        if not data.get('title') or len(data.get('title', '')) < 30:
            scores['content'] -= 15
        if not data.get('description') or len(data.get('description', '')) < 100:
            scores['content'] -= 15
        if data.get('words', 0) < 300:
            scores['content'] -= 10
        
        # Performance score
        load_time = data.get('load_time', 0)
        if load_time > 3000:
            scores['performance'] -= 30
        elif load_time > 2000:
            scores['performance'] -= 20
        elif load_time > 1000:
            scores['performance'] -= 10
        
        # Overall
        scores['overall'] = (scores['technical'] + scores['content'] + scores['performance']) // 3
        
        return scores
    
    def _identify_issues(self, data: Dict) -> Dict[str, list]:
        """Identify SEO issues"""
        issues = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }
        
        # Critical issues
        if not data.get('has_ssl'):
            issues['critical'].append('Website not using HTTPS')
        
        if not data.get('title'):
            issues['critical'].append('Missing title tag')
        
        # High priority
        if data.get('h1_count', 0) == 0:
            issues['high'].append('No H1 tag found')
        elif data.get('h1_count', 0) > 1:
            issues['high'].append(f"Multiple H1 tags ({data['h1_count']})")
        
        if not data.get('description'):
            issues['high'].append('Missing meta description')
        
        # Medium priority
        if data.get('title') and len(data.get('title', '')) < 30:
            issues['medium'].append('Title tag too short (< 30 chars)')
        
        if data.get('description') and len(data.get('description', '')) < 100:
            issues['medium'].append('Meta description too short (< 100 chars)')
        
        # Low priority
        missing_alt = sum(1 for img in data.get('images', []) if not img.get('alt'))
        if missing_alt > 0:
            issues['low'].append(f'{missing_alt} images missing alt text')
        
        return issues