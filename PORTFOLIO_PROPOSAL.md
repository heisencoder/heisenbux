# Heisenbux Portfolio Management Enhancement Proposal

## Executive Summary

This proposal outlines enhancements to transform Heisenbux from a single-ticker visualization tool into a comprehensive portfolio management system with modern code quality practices, multi-account tracking, and sophisticated rebalancing recommendations based on efficient frontier analysis and analyst projections.

## 1. Code Quality & CI/CD Infrastructure

### 1.1 Type Annotations

- Add comprehensive type hints to all functions and classes
- Use `mypy` for static type checking with strict configuration
- Define custom types for domain objects (e.g., `Ticker`, `Portfolio`, `Allocation`)

### 1.2 Testing Suite

- **Framework**: pytest with pytest-cov for coverage reporting
- **Target Coverage**: 90%+ with branch coverage
- **Test Structure**:

  ```text
  tests/
  ├── unit/
  │   ├── test_finance.py
  │   ├── test_portfolio.py
  │   └── test_analysis.py
  ├── integration/
  │   └── test_data_sources.py
  └── fixtures/
      └── sample_portfolios.py
  ```

- Mock external API calls (yfinance, analyst data)
- Property-based testing with Hypothesis for numerical algorithms

### 1.3 Code Quality Tools

- **Formatter**: Ruff format (already configured)
- **Linter**: Ruff with extended ruleset
- **Type Checker**: mypy with strict mode
- **Security**: bandit for security vulnerabilities
- **Docstrings**: pydocstyle enforcement

### 1.4 GitHub Actions Workflow

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: poetry install
      - run: poetry run ruff check .
      - run: poetry run ruff format . --check
      - run: poetry run mypy .
      - run: poetry run pytest --cov=heisenbux --cov-report=xml
      - run: poetry run bandit -r heisenbux/
      - uses: codecov/codecov-action@v3
```

### 1.5 Pre-commit Hooks

Configure pre-commit to run all quality checks locally before commits.

## 2. Portfolio Data Management

### 2.1 Portfolio Configuration Format

Use YAML for human-readable portfolio definitions:

```yaml
# portfolio.yaml
portfolio:
  name: "My Investment Portfolio"
  currency: USD

accounts:
  - name: "Vanguard Roth IRA"
    type: roth_ira
    holdings:
      - ticker: VTI
        shares: 150.5
        cost_basis: 32000.00
        purchase_date: 2022-01-15
      - ticker: VXUS
        shares: 75.25
        cost_basis: 4500.00
        purchase_date: 2022-03-20

  - name: "Fidelity Traditional IRA"
    type: traditional_ira
    holdings:
      - ticker: BND
        shares: 200
        cost_basis: 16000.00
        purchase_date: 2021-06-01

  - name: "Schwab Taxable"
    type: taxable
    holdings:
      - ticker: AAPL
        shares: 50
        cost_basis: 7500.00
        purchase_date: 2023-01-10
      - ticker: MSFT
        shares: 30
        cost_basis: 9000.00
        purchase_date: 2023-02-15

rebalancing_preferences:
  target_allocation:
    US_stocks: 0.60
    international_stocks: 0.30
    bonds: 0.10
  risk_tolerance: moderate  # conservative, moderate, aggressive
  rebalance_threshold: 0.05  # 5% deviation triggers rebalancing
```

### 2.2 Asset Classification

Implement automatic asset classification:

```python
asset_classifications = {
    "VTI": {"class": "US_stocks", "category": "total_market"},
    "VXUS": {"class": "international_stocks", "category": "total_market"},
    "BND": {"class": "bonds", "category": "aggregate"},
    # ... more mappings
}
```

### 2.3 Transaction Tracking

Support transaction logs for tax optimization:

```yaml
transactions:
  - date: 2024-01-15
    account: "Schwab Taxable"
    type: buy
    ticker: AAPL
    shares: 10
    price: 185.50
    fees: 0.00
```

## 3. Portfolio Analysis & Rebalancing Engine

### 3.1 Data Sources

- **Market Data**: Continue using yfinance for price data
- **Analyst Projections**:
  - Integrate multiple sources: Yahoo Finance analyst estimates, Seeking Alpha API
  - Aggregate consensus price targets and earnings projections
  - Calculate confidence intervals based on analyst disagreement

### 3.2 Portfolio Analytics Module

```python
class PortfolioAnalyzer:
    def calculate_current_allocation(self) -> Dict[str, float]
    def calculate_performance_metrics(self) -> PerformanceMetrics
    def calculate_risk_metrics(self) -> RiskMetrics
    def generate_correlation_matrix(self) -> pd.DataFrame
    def calculate_sharpe_ratio(self) -> float
    def calculate_tax_efficiency(self) -> TaxMetrics
```

### 3.3 Efficient Frontier Analysis

- Use `PyPortfolioOpt` library for modern portfolio theory calculations
- Generate efficient frontier curves considering:
  - Historical returns and volatility
  - Analyst consensus projections
  - Correlation between assets
  - Account-type constraints (e.g., no individual stocks in IRA)

### 3.4 Rebalancing Recommendations

```python
class RebalancingEngine:
    def generate_recommendations(
        self,
        portfolio: Portfolio,
        target_allocation: Dict[str, float],
        constraints: RebalancingConstraints
    ) -> RebalancingPlan
```

Features:
- Tax-aware rebalancing (prioritize tax-advantaged accounts)
- Transaction cost minimization
- Tax-loss harvesting opportunities in taxable accounts
- Respect wash-sale rules
- Consider dividend timing

### 3.5 Visualization Enhancements

- **Current vs Target Allocation**: Pie/donut charts
- **Efficient Frontier**: Scatter plot with current position marked
- **Performance Attribution**: Waterfall charts
- **Risk Decomposition**: Heatmaps
- **Historical Performance**: Multi-asset line charts with benchmarks

## 4. New CLI Commands

```bash
# Portfolio management
heisenbux portfolio load portfolio.yaml
heisenbux portfolio show --format table
heisenbux portfolio performance --period 1Y

# Analysis
heisenbux analyze risk --var 95
heisenbux analyze correlation --heatmap
heisenbux analyze projections --sources all

# Rebalancing
heisenbux rebalance suggest --method efficient-frontier
heisenbux rebalance preview --tax-aware
heisenbux rebalance export --format csv

# Batch operations
heisenbux update-all  # Update all holdings data
```

## 5. Implementation Phases

### Phase 1: Foundation (Weeks 1-2)

- Set up testing framework and CI/CD pipeline
- Add type annotations to existing code
- Implement portfolio data models and YAML parsing

### Phase 2: Data Layer (Weeks 3-4)

- Extend finance module for multi-ticker support
- Implement analyst data aggregation
- Build transaction tracking system

### Phase 3: Analytics (Weeks 5-6)

- Implement portfolio metrics calculations
- Integrate PyPortfolioOpt for efficient frontier
- Build basic rebalancing engine

### Phase 4: Visualization & CLI (Weeks 7-8)

- Enhance plotting capabilities
- Implement new CLI commands
- Add comprehensive documentation

### Phase 5: Advanced Features (Weeks 9-10)

- Tax-aware rebalancing
- Monte Carlo simulations
- Backtesting framework

## 6. Dependencies to Add

```toml
[tool.poetry.dependencies]
pyyaml = "^6.0"
pyportfolioopt = "^1.5"
scipy = "^1.11"
numpy = "^1.25"
plotly = "^5.0"  # For interactive visualizations

[tool.poetry.group.dev.dependencies]
pytest = "^7.4"
pytest-cov = "^4.1"
mypy = "^1.7"
pre-commit = "^3.5"
bandit = "^1.7"
hypothesis = "^6.9"
pytest-mock = "^3.12"
```

## 7. Example Usage

```python
# Load portfolio
portfolio = Portfolio.from_yaml("portfolio.yaml")

# Analyze current state
analyzer = PortfolioAnalyzer(portfolio)
metrics = analyzer.calculate_performance_metrics()
print(f"Total Value: ${metrics.total_value:,.2f}")
print(f"YTD Return: {metrics.ytd_return:.2%}")

# Get rebalancing suggestions
engine = RebalancingEngine()
targets = TargetAllocation.from_risk_profile("moderate")
plan = engine.generate_recommendations(
    portfolio,
    targets,
    constraints=RebalancingConstraints(
        min_transaction_size=100,
        consider_taxes=True,
        avoid_wash_sales=True
    )
)

# Execute rebalancing
for action in plan.actions:
    print(f"{action.action}: {action.shares} shares of {action.ticker} "
          f"in {action.account} (${action.estimated_value:,.2f})")
```

## 8. Future Enhancements

- Real-time portfolio tracking with webhooks
- Mobile-friendly web dashboard
- Integration with broker APIs for automated execution
- Machine learning for return predictions
- Social features for strategy sharing
- Options strategy analysis
- Cryptocurrency support
