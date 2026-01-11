<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexus SEO - Pricing Plans</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 2rem;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            margin-bottom: 3rem;
        }

        .header h1 {
            font-size: 3rem;
            color: #1e293b;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
        }

        .header p {
            font-size: 1.2rem;
            color: #64748b;
        }

        .billing-toggle {
            display: flex;
            gap: 2rem;
            justify-content: center;
            margin-bottom: 3rem;
        }

        .billing-card {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            transition: all 0.3s;
            cursor: pointer;
            border: 3px solid transparent;
            min-width: 280px;
        }

        .billing-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 50px rgba(0,0,0,0.15);
        }

        .billing-card.annual {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .billing-card.monthly {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }

        .billing-card.selected {
            border: 3px solid #fbbf24;
            transform: scale(1.05);
        }

        .billing-header {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1.8rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }

        .badge {
            display: inline-block;
            padding: 0.4rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: bold;
            margin-top: 0.5rem;
        }

        .badge.save {
            background: #10b981;
            color: white;
        }

        .badge.flexible {
            background: #3b82f6;
            color: white;
        }

        .billing-tagline {
            font-size: 2rem;
            font-weight: bold;
            margin: 1.5rem 0;
        }

        .features {
            background: rgba(255,255,255,0.2);
            border-radius: 15px;
            padding: 1.5rem;
            margin-top: 1.5rem;
        }

        .feature-section {
            margin-bottom: 1.5rem;
        }

        .feature-title {
            font-weight: bold;
            font-size: 1.1rem;
            margin-bottom: 0.8rem;
            border-bottom: 2px solid rgba(255,255,255,0.3);
            padding-bottom: 0.5rem;
        }

        .feature-item {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            margin: 0.7rem 0;
            font-size: 1rem;
        }

        .feature-icon {
            font-size: 1.3rem;
        }

        .plans-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }

        .plan-card {
            background: white;
            border-radius: 20px;
            padding: 2.5rem;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }

        .plan-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        }

        .plan-card.featured {
            border: 3px solid #fbbf24;
            transform: scale(1.05);
        }

        .plan-card.featured::before {
            content: "⭐ MOST POPULAR";
            position: absolute;
            top: 20px;
            right: -35px;
            background: #fbbf24;
            color: #1e293b;
            padding: 0.5rem 3rem;
            transform: rotate(45deg);
            font-weight: bold;
            font-size: 0.8rem;
        }

        .plan-name {
            font-size: 2rem;
            font-weight: bold;
            color: #1e293b;
            margin-bottom: 1rem;
        }

        .plan-price {
            font-size: 3rem;
            font-weight: bold;
            color: #667eea;
            margin: 1rem 0;
        }

        .plan-price span {
            font-size: 1.2rem;
            color: #64748b;
        }

        .plan-description {
            color: #64748b;
            margin-bottom: 2rem;
            line-height: 1.6;
        }

        .plan-features {
            list-style: none;
            margin-bottom: 2rem;
        }

        .plan-features li {
            padding: 0.8rem 0;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }

        .plan-features li:last-child {
            border-bottom: none;
        }

        .btn {
            display: block;
            width: 100%;
            padding: 1rem 2rem;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
            text-decoration: none;
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }

        .btn-secondary {
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
        }

        .btn-secondary:hover {
            background: #667eea;
            color: white;
        }

        @media (max-width: 768px) {
            .billing-toggle {
                flex-direction: column;
                align-items: center;
            }

            .header h1 {
                font-size: 2rem;
            }

            .plans-grid {
                grid-template-columns: 1fr;
            }

            .plan-card.featured {
                transform: scale(1);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Select Your Billing Cycle</h1>
            <p>Choose the plan that fits your needs</p>
        </div>

        <div class="billing-toggle">
            <div class="billing-card annual selected" onclick="showAnnual()">
                <div class="billing-header">
                    💰 Annual Billing
                </div>
                <div class="badge save">💸 SAVE UP TO 20%</div>
                <div class="billing-tagline">Best Value!</div>
                
                <div class="features">
                    <div class="feature-section">
                        <div class="feature-title">What's included:</div>
                        <div class="feature-item">
                            <span class="feature-icon">✅</span>
                            <span>Pro Yearly - €2,457/year</span>
                        </div>
                        <div class="feature-item">
                            <span class="feature-icon">✅</span>
                            <span>Agency Yearly - €1,430/year</span>
                        </div>
                        <div class="feature-item">
                            <span class="feature-icon">✅</span>
                            <span>Elite Yearly - Premium features</span>
                        </div>
                    </div>

                    <div class="feature-section">
                        <div class="feature-title">All plans include:</div>
                        <div class="feature-item">
                            <span class="feature-icon">🎨</span>
                            <span>White label reports</span>
                        </div>
                        <div class="feature-item">
                            <span class="feature-icon">🚀</span>
                            <span>Priority support</span>
                        </div>
                        <div class="feature-item">
                            <span class="feature-icon">🔥</span>
                            <span>All features unlocked</span>
                        </div>
                        <div class="feature-item">
                            <span class="feature-icon">💳</span>
                            <span>One payment per year</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="billing-card monthly" onclick="showMonthly()">
                <div class="billing-header">
                    📅 Monthly Billing
                </div>
                <div class="badge flexible">✨ FLEXIBLE</div>
                <div class="billing-tagline">Pay as you go</div>
                
                <div class="features">
                    <div class="feature-section">
                        <div class="feature-title">What's included:</div>
                        <div class="feature-item">
                            <span class="feature-icon">✅</span>
                            <span>Pro Monthly - Flexible pricing</span>
                        </div>
                        <div class="feature-item">
                            <span class="feature-icon">✅</span>
                            <span>Agency Monthly - Scale easily</span>
                        </div>
                        <div class="feature-item">
                            <span class="feature-icon">✅</span>
                            <span>Elite Monthly - No commitment</span>
                        </div>
                    </div>

                    <div class="feature-section">
                        <div class="feature-title">All plans include:</div>
                        <div class="feature-item">
                            <span class="feature-icon">🎨</span>
                            <span>White label reports</span>
                        </div>
                        <div class="feature-item">
                            <span class="feature-icon">🚀</span>
                            <span>Priority support</span>
                        </div>
                        <div class="feature-item">
                            <span class="feature-icon">🔥</span>
                            <span>All features unlocked</span>
                        </div>
                        <div class="feature-item">
                            <span class="feature-icon">🔄</span>
                            <span>Cancel anytime</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div id="annual-plans" class="plans-grid">
            <div class="plan-card">
                <div class="plan-name">Pro</div>
                <div class="plan-price">€2,457<span>/year</span></div>
                <div class="plan-description">Perfect for freelancers and small businesses looking to boost their SEO</div>
                <ul class="plan-features">
                    <li>✅ 50 scans per month</li>
                    <li>✅ 100,000 AI credits</li>
                    <li>✅ Advanced AI analysis</li>
                    <li>✅ JSON export</li>
                    <li>✅ Priority support</li>
                    <li>✅ Save €131/year</li>
                </ul>
                <button class="btn btn-primary">🎯 View Yearly Plans</button>
            </div>

            <div class="plan-card featured">
                <div class="plan-name">Agency</div>
                <div class="plan-price">€1,430<span>/year</span></div>
                <div class="plan-description">For agencies managing multiple clients with advanced features</div>
                <ul class="plan-features">
                    <li>✅ 200 scans per month</li>
                    <li>✅ 500,000 AI credits</li>
                    <li>✅ PDF & JSON exports</li>
                    <li>✅ White label reports</li>
                    <li>✅ API access</li>
                    <li>✅ Team collaboration</li>
                    <li>✅ Save €358/year</li>
                </ul>
                <button class="btn btn-primary">🎯 View Yearly Plans</button>
            </div>

            <div class="plan-card">
                <div class="plan-name">Elite</div>
                <div class="plan-price">€43,000<span>/year</span></div>
                <div class="plan-description">Enterprise solution with unlimited everything and dedicated support</div>
                <ul class="plan-features">
                    <li>✅ Unlimited scans</li>
                    <li>✅ 10M AI credits</li>
                    <li>✅ Custom AI training</li>
                    <li>✅ Dedicated manager</li>
                    <li>✅ Custom integrations</li>
                    <li>✅ All features included</li>
                    <li>✅ Save €4,788/year</li>
                </ul>
                <button class="btn btn-primary">🎯 View Yearly Plans</button>
            </div>
        </div>

        <div id="monthly-plans" class="plans-grid" style="display: none;">
            <div class="plan-card">
                <div class="plan-name">Pro</div>
                <div class="plan-price">€49<span>/month</span></div>
                <div class="plan-description">Perfect for freelancers and small businesses looking to boost their SEO</div>
                <ul class="plan-features">
                    <li>✅ 50 scans per month</li>
                    <li>✅ 100,000 AI credits</li>
                    <li>✅ Advanced AI analysis</li>
                    <li>✅ JSON export</li>
                    <li>✅ Priority support</li>
                    <li>✅ Cancel anytime</li>
                </ul>
                <button class="btn btn-secondary">📅 View Monthly Plans</button>
            </div>

            <div class="plan-card featured">
                <div class="plan-name">Agency</div>
                <div class="plan-price">€149<span>/month</span></div>
                <div class="plan-description">For agencies managing multiple clients with advanced features</div>
                <ul class="plan-features">
                    <li>✅ 200 scans per month</li>
                    <li>✅ 500,000 AI credits</li>
                    <li>✅ PDF & JSON exports</li>
                    <li>✅ White label reports</li>
                    <li>✅ API access</li>
                    <li>✅ Team collaboration</li>
                    <li>✅ Cancel anytime</li>
                </ul>
                <button class="btn btn-secondary">📅 View Monthly Plans</button>
            </div>

            <div class="plan-card">
                <div class="plan-name">Elite</div>
                <div class="plan-price">€399<span>/month</span></div>
                <div class="plan-description">Enterprise solution with unlimited everything and dedicated support</div>
                <ul class="plan-features">
                    <li>✅ Unlimited scans</li>
                    <li>✅ 10M AI credits</li>
                    <li>✅ Custom AI training</li>
                    <li>✅ Dedicated manager</li>
                    <li>✅ Custom integrations</li>
                    <li>✅ All features included</li>
                    <li>✅ Cancel anytime</li>
                </ul>
                <button class="btn btn-secondary">📅 View Monthly Plans</button>
            </div>
        </div>
    </div>

    <script>
        function showAnnual() {
            document.getElementById('annual-plans').style.display = 'grid';
            document.getElementById('monthly-plans').style.display = 'none';
            
            document.querySelectorAll('.billing-card').forEach(card => {
                card.classList.remove('selected');
            });
            document.querySelector('.billing-card.annual').classList.add('selected');
        }

        function showMonthly() {
            document.getElementById('annual-plans').style.display = 'none';
            document.getElementById('monthly-plans').style.display = 'grid';
            
            document.querySelectorAll('.billing-card').forEach(card => {
                card.classList.remove('selected');
            });
            document.querySelector('.billing-card.monthly').classList.add('selected');
        }
    </script>
</body>
</html>