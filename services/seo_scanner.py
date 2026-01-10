"""
SEO Scanner Service
Analyzes websites for SEO metrics and issues
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
import re
from typing import Dict, List, Optional

class SEOScanner:
    """Main SEO scanning engine"""
    
    def __init__(self, url: str, timeout: int = 30):
        self.url = url
        self.timeout = timeout
        self.soup = None
        self.response = None
        self.results = {}
        
    def scan(self) -> Dict:
        """
        Run complete SEO scan
        Returns: Dictionary with all SEO metrics
        """
        try:
            # Fetch the page
            self.response = self._fetch_page()
            if not self.response:
                return {'error': 'Failed to fetch page'}
            
            # Parse HTML
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
            
            # Run all analyses
            self.results = {
                'url': self.url,
                'status_code': self.response.status_code,
                'scan_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'meta_tags': self._analyze_meta_tags(),
                'headings': self._analyze_headings(),
                'images': self._analyze_images(),
                'links': self._analyze_links(),
                'content': self._analyze_content(),
                'technical': self._analyze_technical(),
                'mobile': self._check_mobile_friendly(),
                'performance': self._analyze_performance(),
                'issues': [],
                'warnings': [],
                'recommendations': []
            }
            
            # Calculate scores and issues
            self._calculate_issues()
            self._calculate_score()
            
            return self.results
            
        except Exception as e:
            return {'error': f'Scan failed: {str(e)}'}
    
    def _fetch_page(self) -> Optional[requests.Response]:
        """Fetch webpage with proper headers"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        try:
            response = requests.get(self.url, headers=headers, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()
            return response
        except Exception as e:
            print(f"Error fetching page: {e}")
            return None
    
    def _analyze_meta_tags(self) -> Dict:
        """Analyze meta tags (title, description, keywords, etc.)"""
        meta_data = {
            'title': '',
            'title_length': 0,
            'description': '',
            'description_length': 0,
            'keywords': '',
            'robots': '',
            'canonical': '',
            'og_tags': {},
            'twitter_tags': {}
        }
        
        # Title
        title_tag = self.soup.find('title')
        if title_tag:
            meta_data['title'] = title_tag.get_text().strip()
            meta_data['title_length'] = len(meta_data['title'])
        
        # Meta tags
        for meta in self.soup.find_all('meta'):
            name = meta.get('name', '').lower()
            property_name = meta.get('property', '').lower()
            content = meta.get('content', '')
            
            if name == 'description':
                meta_data['description'] = content
                meta_data['description_length'] = len(content)
            elif name == 'keywords':
                meta_data['keywords'] = content
            elif name == 'robots':
                meta_data['robots'] = content
            elif property_name.startswith('og:'):
                meta_data['og_tags'][property_name] = content
            elif name.startswith('twitter:'):
                meta_data['twitter_tags'][name] = content
        
        # Canonical
        canonical = self.soup.find('link', {'rel': 'canonical'})
        if canonical:
            meta_data['canonical'] = canonical.get('href', '')
        
        return meta_data
    
    def _analyze_headings(self) -> Dict:
        """Analyze heading structure (H1-H6)"""
        headings = {
            'h1': [],
            'h2': [],
            'h3': [],
            'h4': [],
            'h5': [],
            'h6': [],
            'h1_count': 0,
            'total_count': 0
        }
        
        for i in range(1, 7):
            tags = self.soup.find_all(f'h{i}')
            heading_texts = [tag.get_text().strip() for tag in tags]
            headings[f'h{i}'] = heading_texts
            headings[f'h{i}_count'] = len(heading_texts)
            headings['total_count'] += len(heading_texts)
        
        headings['h1_count'] = len(headings['h1'])
        
        return headings
    
    def _analyze_images(self) -> Dict:
        """Analyze images (alt tags, optimization)"""
        images = {
            'total': 0,
            'with_alt': 0,
            'without_alt': 0,
            'missing_alt': [],
            'alt_texts': []
        }
        
        img_tags = self.soup.find_all('img')
        images['total'] = len(img_tags)
        
        for img in img_tags:
            alt = img.get('alt', '').strip()
            src = img.get('src', '')
            
            if alt:
                images['with_alt'] += 1
                images['alt_texts'].append({'src': src, 'alt': alt})
            else:
                images['without_alt'] += 1
                images['missing_alt'].append(src)
        
        return images
    
    def _analyze_links(self) -> Dict:
        """Analyze internal and external links"""
        links = {
            'total': 0,
            'internal': 0,
            'external': 0,
            'broken': 0,
            'nofollow': 0,
            'internal_links': [],
            'external_links': []
        }
        
        domain = urlparse(self.url).netloc
        
        for link in self.soup.find_all('a', href=True):
            href = link.get('href', '')
            rel = link.get('rel', [])
            
            if not href or href.startswith('#'):
                continue
            
            links['total'] += 1
            
            # Check if nofollow
            if 'nofollow' in rel:
                links['nofollow'] += 1
            
            # Resolve relative URLs
            full_url = urljoin(self.url, href)
            link_domain = urlparse(full_url).netloc
            
            # Classify as internal or external
            if link_domain == domain:
                links['internal'] += 1
                links['internal_links'].append(full_url)
            else:
                links['external'] += 1
                links['external_links'].append(full_url)
        
        return links
    
    def _analyze_content(self) -> Dict:
        """Analyze page content (word count, readability, etc.)"""
        # Get text content
        text = self.soup.get_text()
        text_clean = ' '.join(text.split())
        
        # Word count
        words = text_clean.split()
        word_count = len(words)
        
        # Character count
        char_count = len(text_clean)
        
        # Paragraph count
        paragraphs = self.soup.find_all('p')
        paragraph_count = len(paragraphs)
        
        content = {
            'word_count': word_count,
            'char_count': char_count,
            'paragraph_count': paragraph_count,
            'avg_words_per_paragraph': round(word_count / paragraph_count, 2) if paragraph_count > 0 else 0,
            'text_preview': text_clean[:500] + '...' if len(text_clean) > 500 else text_clean
        }
        
        return content
    
    def _analyze_technical(self) -> Dict:
        """Analyze technical SEO factors"""
        technical = {
            'has_sitemap': False,
            'has_robots_txt': False,
            'has_favicon': False,
            'has_ssl': self.url.startswith('https://'),
            'load_time': 0,
            'page_size': 0,
            'charset': '',
            'doctype': ''
        }
        
        # Check charset
        charset_meta = self.soup.find('meta', {'charset': True})
        if charset_meta:
            technical['charset'] = charset_meta.get('charset', '')
        
        # Check doctype
        if self.soup.contents:
            doctype = str(self.soup.contents[0])
            if 'DOCTYPE' in doctype:
                technical['doctype'] = 'HTML5' if 'html' in doctype.lower() else 'Legacy'
        
        # Check favicon
        favicon = self.soup.find('link', {'rel': 'icon'}) or self.soup.find('link', {'rel': 'shortcut icon'})
        technical['has_favicon'] = favicon is not None
        
        # Page size
        if self.response:
            technical['page_size'] = len(self.response.content)
            technical['load_time'] = self.response.elapsed.total_seconds()
        
        return technical
    
    def _check_mobile_friendly(self) -> Dict:
        """Check mobile-friendliness indicators"""
        mobile = {
            'has_viewport': False,
            'viewport_content': '',
            'is_responsive': False
        }
        
        # Check viewport meta tag
        viewport = self.soup.find('meta', {'name': 'viewport'})
        if viewport:
            mobile['has_viewport'] = True
            mobile['viewport_content'] = viewport.get('content', '')
            if 'width=device-width' in mobile['viewport_content']:
                mobile['is_responsive'] = True
        
        return mobile
    
    def _analyze_performance(self) -> Dict:
        """Analyze performance metrics"""
        performance = {
            'load_time': 0,
            'size_kb': 0,
            'resource_count': 0
        }
        
        if self.response:
            performance['load_time'] = round(self.response.elapsed.total_seconds(), 2)
            performance['size_kb'] = round(len(self.response.content) / 1024, 2)
        
        # Count resources
        scripts = len(self.soup.find_all('script'))
        styles = len(self.soup.find_all('link', {'rel': 'stylesheet'}))
        images = len(self.soup.find_all('img'))
        
        performance['resource_count'] = scripts + styles + images
        performance['scripts'] = scripts
        performance['styles'] = styles
        performance['images'] = images
        
        return performance
    
    def _calculate_issues(self):
        """Identify SEO issues and generate recommendations"""
        issues = []
        warnings = []
        recommendations = []
        
        # Meta tags issues
        meta = self.results['meta_tags']
        if not meta['title']:
            issues.append({'type': 'critical', 'category': 'meta', 'title': 'Missing Title Tag', 'description': 'Page has no title tag'})
        elif meta['title_length'] < 30:
            warnings.append({'type': 'warning', 'category': 'meta', 'title': 'Title Too Short', 'description': f'Title is {meta["title_length"]} chars (recommended: 50-60)'})
        elif meta['title_length'] > 60:
            warnings.append({'type': 'warning', 'category': 'meta', 'title': 'Title Too Long', 'description': f'Title is {meta["title_length"]} chars (recommended: 50-60)'})
        
        if not meta['description']:
            issues.append({'type': 'critical', 'category': 'meta', 'title': 'Missing Meta Description', 'description': 'Page has no meta description'})
        elif meta['description_length'] < 120:
            warnings.append({'type': 'warning', 'category': 'meta', 'title': 'Description Too Short', 'description': f'Description is {meta["description_length"]} chars (recommended: 150-160)'})
        elif meta['description_length'] > 160:
            warnings.append({'type': 'warning', 'category': 'meta', 'title': 'Description Too Long', 'description': f'Description is {meta["description_length"]} chars (recommended: 150-160)'})
        
        # Heading issues
        headings = self.results['headings']
        if headings['h1_count'] == 0:
            issues.append({'type': 'critical', 'category': 'content', 'title': 'Missing H1 Tag', 'description': 'Page has no H1 heading'})
        elif headings['h1_count'] > 1:
            warnings.append({'type': 'warning', 'category': 'content', 'title': 'Multiple H1 Tags', 'description': f'Page has {headings["h1_count"]} H1 tags (recommended: 1)'})
        
        # Image issues
        images = self.results['images']
        if images['without_alt'] > 0:
            warnings.append({'type': 'warning', 'category': 'images', 'title': 'Images Missing Alt Text', 'description': f'{images["without_alt"]} of {images["total"]} images missing alt attributes'})
        
        # Content issues
        content = self.results['content']
        if content['word_count'] < 300:
            warnings.append({'type': 'warning', 'category': 'content', 'title': 'Low Word Count', 'description': f'Page has only {content["word_count"]} words (recommended: 300+)'})
        
        # Technical issues
        technical = self.results['technical']
        if not technical['has_ssl']:
            issues.append({'type': 'critical', 'category': 'technical', 'title': 'No HTTPS', 'description': 'Page is not using HTTPS encryption'})
        
        # Mobile issues
        mobile = self.results['mobile']
        if not mobile['has_viewport']:
            issues.append({'type': 'critical', 'category': 'mobile', 'title': 'No Viewport Meta Tag', 'description': 'Page is missing viewport meta tag for mobile'})
        
        # Generate recommendations
        if meta['title_length'] < 30:
            recommendations.append({'title': 'Optimize Title Tag', 'description': 'Expand your title to 50-60 characters to improve click-through rates'})
        
        if content['word_count'] < 300:
            recommendations.append({'title': 'Add More Content', 'description': 'Expand content to at least 300 words for better SEO performance'})
        
        if images['without_alt'] > 0:
            recommendations.append({'title': 'Add Alt Text to Images', 'description': 'Add descriptive alt text to all images for accessibility and SEO'})
        
        self.results['issues'] = issues
        self.results['warnings'] = warnings
        self.results['recommendations'] = recommendations
        self.results['issues_count'] = len(issues)
        self.results['warnings_count'] = len(warnings)
        self.results['opportunities_count'] = len(recommendations)
    
    def _calculate_score(self):
        """Calculate overall SEO score (0-100)"""
        score = 100
        
        # Deduct points for issues
        score -= len(self.results['issues']) * 10
        score -= len(self.results['warnings']) * 5
        
        # Bonus points for good practices
        if self.results['technical']['has_ssl']:
            score += 5
        if self.results['mobile']['is_responsive']:
            score += 5
        if self.results['meta_tags']['title_length'] >= 50:
            score += 5
        if self.results['content']['word_count'] >= 300:
            score += 5
        
        # Ensure score is between 0-100
        score = max(0, min(100, score))
        
        self.results['seo_score'] = score


# Helper function for easy use
def scan_website(url: str) -> Dict:
    """
    Convenience function to scan a website
    Usage: results = scan_website('https://example.com')
    """
    scanner = SEOScanner(url)
    return scanner.scan()