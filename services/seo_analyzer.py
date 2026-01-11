import React, { useState } from 'react';
import { Brain, Zap, TrendingUp, Code, FileText, Image, Link, Search, CheckCircle, AlertTriangle, XCircle, Sparkles, Wand2, Copy, Download, ArrowRight, Target, Lightbulb, ChevronDown, ChevronUp } from 'lucide-react';

export default function SEOIntelligence() {
  const [activeTab, setActiveTab] = useState('scanner');
  const [url, setUrl] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [expandedIssue, setExpandedIssue] = useState(null);

  const analyzeWebsite = async () => {
    if (!url) return;
    
    setAnalyzing(true);
    
    // Simulate AI analysis
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    setResults({
      score: 68,
      previousScore: 52,
      issues: [
        {
          id: 1,
          severity: 'critical',
          category: 'Meta Tags',
          icon: FileText,
          title: 'Missing Meta Description',
          impact: 'High - Reduces click-through rates by up to 40%',
          currentState: 'No meta description detected on 12 pages',
          aiSolution: {
            explanation: 'Meta descriptions are crucial for search visibility and user engagement. They appear in search results and influence whether users click on your link.',
            automated: true,
            steps: [
              'AI will analyze your page content and generate optimized descriptions',
              'Each description will be unique, 150-160 characters, and include target keywords',
              'Descriptions will be compelling and include a call-to-action'
            ],
            code: `<!-- AI-Generated Meta Description -->
<meta name="description" content="Discover premium organic coffee beans sourced directly from sustainable farms. Free shipping on orders over $50. Shop now for the perfect brew!">

<!-- Implementation in React/Next.js -->
<Head>
  <meta name="description" content="Your AI-optimized description here" />
</Head>`,
            generatedSolutions: [
              'Discover premium organic coffee beans sourced directly from sustainable farms. Free shipping on orders over $50. Shop now!',
              'Award-winning specialty coffee roasted fresh daily. 100% organic beans from ethical farms. Order today and taste the difference.',
              'Transform your morning ritual with artisan coffee beans. Ethically sourced, expertly roasted. Join 10,000+ satisfied customers.'
            ]
          }
        },
        {
          id: 2,
          severity: 'critical',
          category: 'Performance',
          icon: Zap,
          title: 'Slow Page Load Speed (4.2s)',
          impact: 'Critical - 53% of users abandon sites loading over 3 seconds',
          currentState: 'First Contentful Paint: 4.2s (Target: <1.8s)',
          aiSolution: {
            explanation: 'Page speed directly impacts SEO rankings, conversion rates, and user experience. Google prioritizes fast-loading sites.',
            automated: true,
            steps: [
              'Automatically compress and convert images to WebP format',
              'Implement lazy loading for below-the-fold content',
              'Minify CSS, JavaScript, and HTML files',
              'Enable browser caching and CDN integration'
            ],
            code: `// Lazy Loading Images (React)
import { useState, useEffect } from 'react';

function OptimizedImage({ src, alt }) {
  const [imgSrc, setImgSrc] = useState('/placeholder.svg');
  
  useEffect(() => {
    const img = new Image();
    img.src = src;
    img.onload = () => setImgSrc(src);
  }, [src]);
  
  return <img src={imgSrc} alt={alt} loading="lazy" />;
}

// Modern Image Optimization with WebP
<picture>
  <source srcSet="/coffee.webp" type="image/webp" />
  <source srcSet="/coffee.jpg" type="image/jpeg" />
  <img 
    src="/coffee.jpg" 
    width="800" 
    height="600"
    loading="lazy"
    alt="Premium coffee beans"
  />
</picture>`,
            automatedFixes: [
              { action: 'Compress 47 images', savings: '2.3MB → 340KB', impact: '-1.8s load time' },
              { action: 'Enable Brotli compression', savings: '890KB → 156KB', impact: '-0.6s load time' },
              { action: 'Defer non-critical CSS', savings: 'Block time: 380ms → 45ms', impact: '-0.4s load time' },
              { action: 'Implement service worker', savings: 'Repeat visits: instant', impact: '100% cache hit' }
            ]
          }
        },
        {
          id: 3,
          severity: 'warning',
          category: 'Content',
          icon: FileText,
          title: 'Thin Content on Key Pages',
          impact: 'Medium - Reduces topical authority and keyword rankings',
          currentState: 'Average word count: 287 words (Recommended: 1,200+)',
          aiSolution: {
            explanation: 'Comprehensive content signals expertise and provides value to users. AI can expand your content while maintaining your brand voice.',
            automated: true,
            steps: [
              'AI analyzes top-ranking competitor content',
              'Identifies content gaps and missing topics',
              'Generates SEO-optimized content expansion',
              'Maintains your existing tone and style'
            ],
            contentSuggestions: [
              {
                section: 'Product Benefits',
                current: '2 paragraphs (112 words)',
                suggested: 'Expand to 400 words covering: health benefits, sustainability, taste profiles, brewing methods',
                aiGenerated: 'Our organic coffee beans offer more than exceptional taste...'
              },
              {
                section: 'FAQ Section',
                current: 'Not present',
                suggested: 'Add 8-10 frequently asked questions targeting long-tail keywords',
                keywords: ['how to brew organic coffee', 'best coffee beans for espresso', 'coffee bean storage tips']
              }
            ]
          }
        },
        {
          id: 4,
          severity: 'warning',
          category: 'Technical',
          icon: Code,
          title: 'Missing Schema Markup',
          impact: 'Medium - Missing rich snippets in search results',
          currentState: 'No structured data detected',
          aiSolution: {
            explanation: 'Schema markup helps search engines understand your content and enables rich results like star ratings, prices, and availability.',
            automated: true,
            steps: [
              'AI identifies page type (Product, Article, Local Business, etc.)',
              'Generates appropriate JSON-LD schema',
              'Validates against Google requirements',
              'Implements automatically across all pages'
            ],
            code: `<!-- AI-Generated Product Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "Ethiopian Yirgacheffe Coffee Beans",
  "image": "https://example.com/coffee.jpg",
  "description": "Single-origin Ethiopian coffee with floral notes",
  "brand": {
    "@type": "Brand",
    "name": "Your Coffee Co"
  },
  "offers": {
    "@type": "Offer",
    "price": "24.99",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "seller": {
      "@type": "Organization",
      "name": "Your Coffee Co"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "247"
  }
}
</script>`,
            schemaTypes: ['Product', 'Organization', 'BreadcrumbList', 'LocalBusiness']
          }
        },
        {
          id: 5,
          severity: 'info',
          category: 'Keywords',
          icon: Target,
          title: 'Keyword Optimization Opportunities',
          impact: 'High Potential - Untapped ranking opportunities detected',
          currentState: 'Ranking for 23 keywords, 147 opportunities identified',
          aiSolution: {
            explanation: 'AI has identified high-value keywords where you could rank with minimal optimization.',
            automated: true,
            opportunities: [
              { keyword: 'organic coffee beans online', volume: '14.8K/mo', difficulty: 'Medium', currentRank: null, potential: 3, action: 'Add to product pages' },
              { keyword: 'best coffee subscription service', volume: '8.1K/mo', difficulty: 'Low', currentRank: 47, potential: 8, action: 'Create dedicated page' },
              { keyword: 'fair trade coffee brands', volume: '6.2K/mo', difficulty: 'Low', currentRank: null, potential: 5, action: 'Add content section' },
              { keyword: 'coffee bean storage tips', volume: '4.5K/mo', difficulty: 'Very Low', currentRank: null, potential: 2, action: 'Create blog post' }
            ],
            implementation: 'AI will automatically integrate these keywords naturally into your existing content and generate new content briefs.'
          }
        }
      ]
    });
    
    setAnalyzing(false);
  };

  const copyCode = (code) => {
    navigator.clipboard.writeText(code);
  };

  const implementFix = async (issueId) => {
    alert('AI is implementing this fix automatically. You will receive a notification when complete.');
  };

  const getSeverityColor = (severity) => {
    switch(severity) {
      case 'critical': return 'text-red-500 bg-red-50';
      case 'warning': return 'text-orange-500 bg-orange-50';
      case 'info': return 'text-blue-500 bg-blue-50';
      default: return 'text-gray-500 bg-gray-50';
    }
  };

  const getSeverityIcon = (severity) => {
    switch(severity) {
      case 'critical': return XCircle;
      case 'warning': return AlertTriangle;
      case 'info': return Lightbulb;
      default: return CheckCircle;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl flex items-center justify-center">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Nexus SEO Intelligence</h1>
                <p className="text-sm text-gray-500">AI-Powered Solutions Platform</p>
              </div>
            </div>
            <div className="flex items-center space-x-2 text-sm">
              <Sparkles className="w-4 h-4 text-purple-600" />
              <span className="text-purple-600 font-semibold">AI-Powered</span>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Scanner Input */}
        {!results && (
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-3">
                AI-Powered Website Analysis
              </h2>
              <p className="text-gray-600 text-lg">
                Get actionable solutions, not just problems. Our AI automatically fixes issues.
              </p>
            </div>

            <div className="max-w-2xl mx-auto">
              <div className="relative">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="Enter your website URL (e.g., https://example.com)"
                  className="w-full pl-12 pr-4 py-4 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-purple-500 text-lg"
                  onKeyPress={(e) => e.key === 'Enter' && analyzeWebsite()}
                />
              </div>
              
              <button
                onClick={analyzeWebsite}
                disabled={!url || analyzing}
                className="w-full mt-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-4 rounded-xl font-semibold text-lg hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center space-x-2"
              >
                {analyzing ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    <span>AI is analyzing your website...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    <span>Start AI Analysis</span>
                  </>
                )}
              </button>

              <div className="mt-6 grid grid-cols-3 gap-4 text-center">
                <div className="p-4 bg-indigo-50 rounded-xl">
                  <Zap className="w-6 h-6 text-indigo-600 mx-auto mb-2" />
                  <p className="text-sm font-semibold text-gray-900">Instant Fixes</p>
                  <p className="text-xs text-gray-600 mt-1">AI implements solutions</p>
                </div>
                <div className="p-4 bg-purple-50 rounded-xl">
                  <Brain className="w-6 h-6 text-purple-600 mx-auto mb-2" />
                  <p className="text-sm font-semibold text-gray-900">Smart Analysis</p>
                  <p className="text-xs text-gray-600 mt-1">Deep learning insights</p>
                </div>
                <div className="p-4 bg-pink-50 rounded-xl">
                  <TrendingUp className="w-6 h-6 text-pink-600 mx-auto mb-2" />
                  <p className="text-sm font-semibold text-gray-900">Track Growth</p>
                  <p className="text-xs text-gray-600 mt-1">Monitor improvements</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Results */}
        {results && (
          <div className="space-y-6">
            {/* Score Card */}
            <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl shadow-xl p-8 text-white">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg opacity-90 mb-2">SEO Health Score</h3>
                  <div className="flex items-baseline space-x-4">
                    <span className="text-6xl font-bold">{results.score}</span>
                    <span className="text-2xl opacity-75">/100</span>
                    <div className="flex items-center space-x-2 text-green-300">
                      <TrendingUp className="w-5 h-5" />
                      <span className="text-lg font-semibold">+{results.score - results.previousScore}</span>
                    </div>
                  </div>
                  <p className="mt-3 opacity-90">
                    {results.issues.filter(i => i.severity === 'critical').length} critical issues detected with AI solutions ready
                  </p>
                </div>
                <div className="text-right">
                  <button
                    onClick={() => setResults(null)}
                    className="px-6 py-3 bg-white text-indigo-600 rounded-xl font-semibold hover:bg-indigo-50 transition-colors"
                  >
                    New Scan
                  </button>
                </div>
              </div>
            </div>

            {/* Issues with Solutions */}
            <div className="space-y-4">
              {results.issues.map((issue) => {
                const SeverityIcon = getSeverityIcon(issue.severity);
                const CategoryIcon = issue.icon;
                const isExpanded = expandedIssue === issue.id;
                
                return (
                  <div key={issue.id} className="bg-white rounded-xl shadow-lg overflow-hidden">
                    <div 
                      className="p-6 cursor-pointer hover:bg-gray-50 transition-colors"
                      onClick={() => setExpandedIssue(isExpanded ? null : issue.id)}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex items-start space-x-4 flex-1">
                          <div className={`w-12 h-12 rounded-xl ${getSeverityColor(issue.severity)} flex items-center justify-center flex-shrink-0`}>
                            <SeverityIcon className="w-6 h-6" />
                          </div>
                          
                          <div className="flex-1">
                            <div className="flex items-center space-x-3 mb-2">
                              <CategoryIcon className="w-4 h-4 text-gray-400" />
                              <span className="text-sm font-medium text-gray-500">{issue.category}</span>
                              {issue.aiSolution.automated && (
                                <span className="px-2 py-1 bg-gradient-to-r from-indigo-500 to-purple-500 text-white text-xs rounded-full flex items-center space-x-1">
                                  <Wand2 className="w-3 h-3" />
                                  <span>Auto-Fix Available</span>
                                </span>
                              )}
                            </div>
                            
                            <h3 className="text-xl font-bold text-gray-900 mb-2">{issue.title}</h3>
                            <p className="text-gray-600 mb-2">{issue.impact}</p>
                            <p className="text-sm text-gray-500">{issue.currentState}</p>
                          </div>
                        </div>
                        
                        <div className="flex items-center space-x-2 ml-4">
                          {isExpanded ? (
                            <ChevronUp className="w-5 h-5 text-gray-400" />
                          ) : (
                            <ChevronDown className="w-5 h-5 text-gray-400" />
                          )}
                        </div>
                      </div>
                    </div>

                    {isExpanded && (
                      <div className="border-t border-gray-100 bg-gray-50 p-6">
                        <div className="space-y-6">
                          {/* AI Explanation */}
                          <div className="bg-white rounded-lg p-5 border border-indigo-100">
                            <div className="flex items-center space-x-2 mb-3">
                              <Brain className="w-5 h-5 text-indigo-600" />
                              <h4 className="font-semibold text-gray-900">AI Analysis</h4>
                            </div>
                            <p className="text-gray-700">{issue.aiSolution.explanation}</p>
                          </div>

                          {/* Implementation Steps */}
                          <div>
                            <h4 className="font-semibold text-gray-900 mb-3 flex items-center space-x-2">
                              <Lightbulb className="w-5 h-5 text-yellow-500" />
                              <span>Implementation Steps</span>
                            </h4>
                            <div className="space-y-2">
                              {issue.aiSolution.steps.map((step, idx) => (
                                <div key={idx} className="flex items-start space-x-3 text-gray-700">
                                  <span className="w-6 h-6 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center text-sm font-semibold flex-shrink-0">
                                    {idx + 1}
                                  </span>
                                  <span>{step}</span>
                                </div>
                              ))}
                            </div>
                          </div>

                          {/* Code Solution */}
                          {issue.aiSolution.code && (
                            <div>
                              <div className="flex items-center justify-between mb-3">
                                <h4 className="font-semibold text-gray-900 flex items-center space-x-2">
                                  <Code className="w-5 h-5 text-gray-600" />
                                  <span>Implementation Code</span>
                                </h4>
                                <button
                                  onClick={() => copyCode(issue.aiSolution.code)}
                                  className="flex items-center space-x-2 px-3 py-1.5 bg-gray-200 hover:bg-gray-300 rounded-lg text-sm font-medium text-gray-700 transition-colors"
                                >
                                  <Copy className="w-4 h-4" />
                                  <span>Copy</span>
                                </button>
                              </div>
                              <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
                                <code>{issue.aiSolution.code}</code>
                              </pre>
                            </div>
                          )}

                          {/* Generated Solutions */}
                          {issue.aiSolution.generatedSolutions && (
                            <div>
                              <h4 className="font-semibold text-gray-900 mb-3 flex items-center space-x-2">
                                <Sparkles className="w-5 h-5 text-purple-600" />
                                <span>AI-Generated Options (Choose One)</span>
                              </h4>
                              <div className="space-y-3">
                                {issue.aiSolution.generatedSolutions.map((solution, idx) => (
                                  <div key={idx} className="bg-white border border-gray-200 rounded-lg p-4 hover:border-purple-300 transition-colors cursor-pointer">
                                    <div className="flex items-start justify-between">
                                      <p className="text-gray-700 flex-1">{solution}</p>
                                      <button className="ml-4 px-3 py-1 bg-purple-100 text-purple-700 rounded-lg text-sm font-medium hover:bg-purple-200 transition-colors">
                                        Use This
                                      </button>
                                    </div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}

                          {/* Automated Fixes */}
                          {issue.aiSolution.automatedFixes && (
                            <div>
                              <h4 className="font-semibold text-gray-900 mb-3 flex items-center space-x-2">
                                <Zap className="w-5 h-5 text-yellow-500" />
                                <span>Automated Optimizations</span>
                              </h4>
                              <div className="space-y-2">
                                {issue.aiSolution.automatedFixes.map((fix, idx) => (
                                  <div key={idx} className="bg-white border border-gray-200 rounded-lg p-4">
                                    <div className="flex items-center justify-between">
                                      <div className="flex-1">
                                        <p className="font-medium text-gray-900">{fix.action}</p>
                                        <p className="text-sm text-gray-600 mt-1">{fix.savings}</p>
                                      </div>
                                      <div className="text-right ml-4">
                                        <span className="text-green-600 font-semibold">{fix.impact}</span>
                                      </div>
                                    </div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}

                          {/* Keyword Opportunities */}
                          {issue.aiSolution.opportunities && (
                            <div>
                              <h4 className="font-semibold text-gray-900 mb-3 flex items-center space-x-2">
                                <Target className="w-5 h-5 text-green-600" />
                                <span>Keyword Opportunities</span>
                              </h4>
                              <div className="overflow-x-auto">
                                <table className="w-full bg-white rounded-lg overflow-hidden">
                                  <thead className="bg-gray-100">
                                    <tr>
                                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Keyword</th>
                                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Search Volume</th>
                                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Difficulty</th>
                                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Potential Rank</th>
                                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Action</th>
                                    </tr>
                                  </thead>
                                  <tbody>
                                    {issue.aiSolution.opportunities.map((opp, idx) => (
                                      <tr key={idx} className="border-t border-gray-100">
                                        <td className="px-4 py-3 text-sm text-gray-900">{opp.keyword}</td>
                                        <td className="px-4 py-3 text-sm text-gray-700">{opp.volume}</td>
                                        <td className="px-4 py-3">
                                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                            opp.difficulty === 'Low' ? 'bg-green-100 text-green-700' :
                                            opp.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                                            'bg-red-100 text-red-700'
                                          }`}>
                                            {opp.difficulty}
                                          </span>
                                        </td>
                                        <td className="px-4 py-3">
                                          <span className="text-sm font-semibold text-indigo-600">#{opp.potential}</span>
                                        </td>
                                        <td className="px-4 py-3 text-sm text-gray-700">{opp.action}</td>
                                      </tr>
                                    ))}
                                  </tbody>
                                </table>
                              </div>
                            </div>
                          )}

                          {/* Action Buttons */}
                          <div className="flex items-center space-x-4 pt-4">
                            <button
                              onClick={() => implementFix(issue.id)}
                              className="flex-1 bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-3 rounded-xl font-semibold hover:from-indigo-700 hover:to-purple-700 transition-all flex items-center justify-center space-x-2"
                            >
                              <Wand2 className="w-5 h-5" />
                              <span>Implement AI Fix Automatically</span>
                            </button>
                            <button className="px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-xl font-semibold hover:border-gray-400 transition-colors flex items-center space-x-2">
                              <Download className="w-5 h-5" />
                              <span>Export Report</span>
                            </button>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}