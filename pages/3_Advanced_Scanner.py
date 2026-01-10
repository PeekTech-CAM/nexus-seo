import React, { useState } from 'react';
import { Search, Brain, Zap, TrendingUp, AlertCircle, CheckCircle, XCircle, ArrowRight, Download, Loader, Globe, BarChart3, Target, Lightbulb } from 'lucide-react';

const AdvancedSEOScanner = () => {
  const [url, setUrl] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [currentPhase, setCurrentPhase] = useState('');
  const [progress, setProgress] = useState(0);

  const analyzeWebsite = async () => {
    if (!url) return;
    
    setAnalyzing(true);
    setProgress(0);
    setCurrentPhase('Initializing AI agents...');
    
    // Simulate comprehensive analysis
    const phases = [
      { text: 'Scanning website structure...', progress: 15 },
      { text: 'Technical SEO audit in progress...', progress: 30 },
      { text: 'AI analyzing content quality...', progress: 45 },
      { text: 'Competitive intelligence gathering...', progress: 60 },
      { text: 'Keyword research & semantic analysis...', progress: 75 },
      { text: 'Generating strategic recommendations...', progress: 90 },
      { text: 'Finalizing comprehensive report...', progress: 100 }
    ];
    
    for (const phase of phases) {
      setCurrentPhase(phase.text);
      setProgress(phase.progress);
      await new Promise(resolve => setTimeout(resolve, 1200));
    }
    
    // Generate comprehensive results
    const mockResults = {
      overall: {
        score: 73,
        technical: 85,
        content: 68,
        competitive: 66,
        mobile: 91,
        performance: 58
      },
      criticalIssues: [
        {
          severity: 'critical',
          title: 'Page Speed Issues Detected',
          description: 'Page load time is 4.2s, well above the recommended 2.5s threshold. This significantly impacts user experience and search rankings.',
          impact: 'High - affecting 75% of mobile users',
          fix: 'Implement lazy loading, optimize images (convert to WebP), minify CSS/JS, enable browser caching',
          effort: 7,
          timeline: '2-3 weeks'
        },
        {
          severity: 'critical',
          title: 'Missing Core Web Vitals Optimization',
          description: 'LCP: 5.2s (Poor), FID: 180ms (Needs Improvement), CLS: 0.18 (Good)',
          impact: 'Direct ranking factor affecting visibility',
          fix: 'Optimize server response time, reduce render-blocking resources, stabilize layout shifts',
          effort: 8,
          timeline: '3-4 weeks'
        },
        {
          severity: 'high',
          title: 'Mobile Usability Issues',
          description: 'Clickable elements too close together, viewport not properly configured on 12 pages',
          impact: 'Medium - affecting mobile rankings',
          fix: 'Increase touch target sizes to minimum 48x48px, fix viewport meta tags',
          effort: 4,
          timeline: '1 week'
        }
      ],
      contentAnalysis: {
        quality: 'Good but needs enhancement',
        wordCount: 847,
        readability: 'Grade 8 (Accessible)',
        keywordDensity: 'Optimal',
        primaryKeywords: ['AI SEO tools', 'website optimization', 'search rankings'],
        semanticOpportunities: ['voice search optimization', 'featured snippets', 'long-tail keywords'],
        contentGaps: [
          'Missing FAQ section for featured snippet opportunities',
          'No video content to increase engagement',
          'Limited use of schema markup for rich snippets',
          'Weak internal linking structure'
        ],
        recommendations: [
          'Add 500-800 words of in-depth content covering user intent',
          'Create comprehensive FAQ section targeting question keywords',
          'Implement schema markup for articles, products, and reviews',
          'Build content hub around primary topic clusters'
        ]
      },
      competitiveAnalysis: {
        position: 'Mid-tier with growth potential',
        competitors: [
          { name: 'competitor-a.com', score: 89, advantage: 'Strong backlink profile' },
          { name: 'competitor-b.com', score: 82, advantage: 'Superior content depth' },
          { name: 'competitor-c.com', score: 76, advantage: 'Better technical SEO' }
        ],
        advantages: [
          'Faster mobile load times than 2/3 competitors',
          'Better social media integration',
          'More frequent content updates'
        ],
        opportunities: [
          {
            title: 'Target Low-Competition Keywords',
            difficulty: 'Easy',
            roi: 'High - 20-35% traffic increase',
            description: 'Focus on 15 identified long-tail keywords with search volume 500-2000/mo and low competition'
          },
          {
            title: 'Build Topical Authority',
            difficulty: 'Medium',
            roi: 'Very High - 40-60% traffic increase',
            description: 'Create content clusters around 3 main topics to establish domain authority'
          },
          {
            title: 'Steal Competitor Backlinks',
            difficulty: 'Medium',
            roi: 'High - 15-25 high-quality links',
            description: 'Identify and replicate competitor link sources through better content'
          }
        ]
      },
      actionPlan: {
        quickWins: [
          {
            task: 'Fix Missing Meta Descriptions',
            impact: 'High',
            effort: 2,
            timeline: '2-3 days',
            instructions: 'Add unique, compelling 150-160 character meta descriptions to all 23 pages missing them. Focus on including primary keyword and clear value proposition.'
          },
          {
            task: 'Optimize Image Alt Text',
            impact: 'Medium',
            effort: 3,
            timeline: '1 week',
            instructions: 'Add descriptive alt text to 89 images. Include keywords naturally but focus on accurate descriptions for accessibility.'
          },
          {
            task: 'Fix Broken Internal Links',
            impact: 'Medium',
            effort: 2,
            timeline: '2 days',
            instructions: 'Update or remove 17 broken internal links affecting page authority flow.'
          }
        ],
        foundations: [
          {
            task: 'Implement Comprehensive Schema Markup',
            impact: 'High',
            effort: 6,
            timeline: '2-3 weeks',
            instructions: 'Add Organization, Article, Product, and FAQ schema to enhance rich snippet visibility'
          },
          {
            task: 'Optimize Core Web Vitals',
            impact: 'Very High',
            effort: 8,
            timeline: '3-4 weeks',
            instructions: 'Reduce LCP to <2.5s, improve FID to <100ms through code optimization and CDN implementation'
          },
          {
            task: 'Build Content Hub Strategy',
            impact: 'Very High',
            effort: 7,
            timeline: '4-6 weeks',
            instructions: 'Create 10-15 pillar pages with supporting cluster content for topical authority'
          }
        ],
        growth: [
          {
            task: 'Launch Link Building Campaign',
            impact: 'Very High',
            effort: 9,
            timeline: '8-12 weeks',
            instructions: 'Target 30-50 high-quality backlinks through guest posting, digital PR, and broken link building'
          },
          {
            task: 'Develop Video Content Strategy',
            impact: 'High',
            effort: 8,
            timeline: '6-10 weeks',
            instructions: 'Create 10-15 video tutorials optimized for YouTube and embedded on site for engagement'
          }
        ],
        metrics: [
          'Organic traffic increase: Target 40-60% in 90 days',
          'Keyword rankings: Move 20+ keywords to page 1',
          'Domain authority: Increase from 35 to 45+',
          'Core Web Vitals: All green scores',
          'Conversion rate: Improve by 15-25%'
        ]
      }
    };
    
    setResults(mockResults);
    setAnalyzing(false);
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-500';
    if (score >= 60) return 'text-blue-500';
    if (score >= 40) return 'text-yellow-500';
    return 'text-red-500';
  };

  const getSeverityStyle = (severity) => {
    const styles = {
      critical: 'border-red-500 bg-red-50',
      high: 'border-orange-500 bg-orange-50',
      medium: 'border-yellow-500 bg-yellow-50',
      low: 'border-green-500 bg-green-50'
    };
    return styles[severity] || styles.medium;
  };

  const getSeverityIcon = (severity) => {
    if (severity === 'critical' || severity === 'high') return <XCircle className="w-5 h-5 text-red-500" />;
    if (severity === 'medium') return <AlertCircle className="w-5 h-5 text-yellow-500" />;
    return <CheckCircle className="w-5 h-5 text-green-500" />;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-20 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse delay-1000"></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <Brain className="w-16 h-16 text-purple-400 mr-4" />
            <h1 className="text-6xl font-bold text-white">
              NEXUS SEO
              <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent"> Intelligence</span>
            </h1>
          </div>
          <p className="text-xl text-gray-300 mb-2">Advanced AI-Powered Multi-Agent Analysis System</p>
          <p className="text-gray-400">Professional-grade SEO scanning with deep competitive intelligence</p>
        </div>

        {/* Search Bar */}
        <div className="max-w-3xl mx-auto mb-12">
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 shadow-2xl">
            <div className="flex gap-4">
              <div className="flex-1 relative">
                <Globe className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="Enter website URL (e.g., https://example.com)"
                  className="w-full pl-12 pr-4 py-4 bg-white rounded-xl text-gray-800 placeholder-gray-400 text-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <button
                onClick={analyzeWebsite}
                disabled={analyzing || !url}
                className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl font-semibold text-lg hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 flex items-center gap-2"
              >
                {analyzing ? (
                  <>
                    <Loader className="w-5 h-5 animate-spin" />
                    Analyzing
                  </>
                ) : (
                  <>
                    <Search className="w-5 h-5" />
                    Analyze
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Analysis Progress */}
        {analyzing && (
          <div className="max-w-3xl mx-auto mb-12">
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <div className="flex items-center justify-between mb-4">
                <span className="text-white font-medium">{currentPhase}</span>
                <span className="text-purple-400 font-bold">{progress}%</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-500"
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
            </div>
          </div>
        )}

        {/* Results */}
        {results && !analyzing && (
          <div className="space-y-8">
            {/* Overall Scores */}
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
              {[
                { label: 'Overall', score: results.overall.score, icon: TrendingUp },
                { label: 'Technical', score: results.overall.technical, icon: Zap },
                { label: 'Content', score: results.overall.content, icon: Brain },
                { label: 'Competitive', score: results.overall.competitive, icon: Target },
                { label: 'Mobile', score: results.overall.mobile, icon: Globe },
                { label: 'Performance', score: results.overall.performance, icon: BarChart3 }
              ].map((item) => (
                <div key={item.label} className="bg-white rounded-xl p-6 text-center shadow-lg">
                  <item.icon className="w-8 h-8 mx-auto mb-2 text-purple-600" />
                  <div className="text-sm text-gray-600 mb-2">{item.label}</div>
                  <div className={`text-4xl font-bold ${getScoreColor(item.score)}`}>
                    {item.score}
                  </div>
                  <div className="text-sm text-gray-400">/100</div>
                </div>
              ))}
            </div>

            {/* Critical Issues */}
            <div className="bg-white rounded-xl p-8 shadow-lg">
              <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                <AlertCircle className="w-6 h-6 text-red-500" />
                Critical Issues & Fixes
              </h2>
              <div className="space-y-4">
                {results.criticalIssues.map((issue, idx) => (
                  <div key={idx} className={`border-l-4 rounded-lg p-6 ${getSeverityStyle(issue.severity)}`}>
                    <div className="flex items-start gap-3 mb-3">
                      {getSeverityIcon(issue.severity)}
                      <div className="flex-1">
                        <h3 className="font-bold text-lg mb-2">{issue.title}</h3>
                        <p className="text-gray-700 mb-3">{issue.description}</p>
                        <div className="grid md:grid-cols-2 gap-4 text-sm">
                          <div>
                            <strong>Impact:</strong> {issue.impact}
                          </div>
                          <div>
                            <strong>Timeline:</strong> {issue.timeline}
                          </div>
                        </div>
                        <div className="mt-3 p-3 bg-white rounded border border-gray-200">
                          <strong className="text-green-700">Fix:</strong>
                          <p className="text-gray-700 mt-1">{issue.fix}</p>
                        </div>
                        <div className="mt-2 flex items-center gap-2 text-sm text-gray-600">
                          <span>Effort: {issue.effort}/10</span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Content Analysis */}
            <div className="bg-white rounded-xl p-8 shadow-lg">
              <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                <Brain className="w-6 h-6 text-purple-600" />
                AI Content Analysis
              </h2>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-bold mb-3">Primary Keywords</h3>
                  <div className="space-y-2">
                    {results.contentAnalysis.primaryKeywords.map((kw, idx) => (
                      <div key={idx} className="bg-purple-50 px-3 py-2 rounded-lg text-purple-700 font-medium">
                        {kw}
                      </div>
                    ))}
                  </div>
                  <h3 className="font-bold mt-6 mb-3">Semantic Opportunities</h3>
                  <div className="space-y-2">
                    {results.contentAnalysis.semanticOpportunities.map((kw, idx) => (
                      <div key={idx} className="bg-green-50 px-3 py-2 rounded-lg text-green-700">
                        {kw}
                      </div>
                    ))}
                  </div>
                </div>
                <div>
                  <h3 className="font-bold mb-3">Content Gaps</h3>
                  <ul className="space-y-2">
                    {results.contentAnalysis.contentGaps.map((gap, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-gray-700">
                        <ArrowRight className="w-4 h-4 mt-1 text-orange-500 flex-shrink-0" />
                        <span>{gap}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            {/* Competitive Analysis */}
            <div className="bg-white rounded-xl p-8 shadow-lg">
              <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                <Target className="w-6 h-6 text-blue-600" />
                Competitive Intelligence
              </h2>
              <div className="mb-6">
                <h3 className="font-bold mb-3">Market Opportunities</h3>
                <div className="space-y-4">
                  {results.competitiveAnalysis.opportunities.map((opp, idx) => (
                    <div key={idx} className="border border-blue-200 rounded-lg p-4 bg-blue-50">
                      <div className="flex items-start justify-between mb-2">
                        <h4 className="font-bold text-lg">{opp.title}</h4>
                        <span className="px-3 py-1 bg-blue-600 text-white text-sm rounded-full">
                          {opp.difficulty}
                        </span>
                      </div>
                      <p className="text-gray-700 mb-2">{opp.description}</p>
                      <div className="text-green-700 font-semibold">{opp.roi}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* 90-Day Action Plan */}
            <div className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl p-8 shadow-lg text-white">
              <h2 className="text-3xl font-bold mb-6 flex items-center gap-2">
                <Lightbulb className="w-8 h-8" />
                90-Day Strategic Action Plan
              </h2>
              
              {/* Quick Wins */}
              <div className="mb-8">
                <h3 className="text-xl font-bold mb-4 bg-white/20 rounded-lg px-4 py-2">
                  Phase 1: Quick Wins (Week 1-2)
                </h3>
                <div className="space-y-3">
                  {results.actionPlan.quickWins.map((task, idx) => (
                    <div key={idx} className="bg-white/10 backdrop-blur rounded-lg p-4 border border-white/20">
                      <div className="flex items-start justify-between mb-2">
                        <h4 className="font-bold">{task.task}</h4>
                        <span className="px-3 py-1 bg-green-500 text-white text-sm rounded-full">
                          {task.impact} Impact
                        </span>
                      </div>
                      <p className="text-white/90 text-sm mb-2">{task.instructions}</p>
                      <div className="flex gap-4 text-sm text-white/70">
                        <span>Effort: {task.effort}/10</span>
                        <span>Timeline: {task.timeline}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Foundations */}
              <div className="mb-8">
                <h3 className="text-xl font-bold mb-4 bg-white/20 rounded-lg px-4 py-2">
                  Phase 2: Foundations (Week 3-6)
                </h3>
                <div className="space-y-3">
                  {results.actionPlan.foundations.slice(0, 3).map((task, idx) => (
                    <div key={idx} className="bg-white/10 backdrop-blur rounded-lg p-4 border border-white/20">
                      <div className="flex items-start justify-between mb-2">
                        <h4 className="font-bold">{task.task}</h4>
                        <span className="px-3 py-1 bg-yellow-500 text-white text-sm rounded-full">
                          {task.impact} Impact
                        </span>
                      </div>
                      <p className="text-white/90 text-sm">{task.instructions}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Success Metrics */}
              <div className="bg-white/20 rounded-lg p-6">
                <h3 className="text-xl font-bold mb-4">Success Metrics to Track</h3>
                <ul className="space-y-2">
                  {results.actionPlan.metrics.map((metric, idx) => (
                    <li key={idx} className="flex items-center gap-2">
                      <CheckCircle className="w-5 h-5 text-green-300" />
                      <span>{metric}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Export Button */}
            <div className="flex justify-center">
              <button className="px-8 py-4 bg-white text-purple-600 rounded-xl font-bold text-lg hover:bg-gray-100 transition-all transform hover:scale-105 flex items-center gap-2 shadow-lg">
                <Download className="w-5 h-5" />
                Download Full Report (PDF)
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdvancedSEOScanner;