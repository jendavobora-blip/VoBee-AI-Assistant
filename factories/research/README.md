# Research Factory

The Research Factory provides modular, extensible interfaces for market research, competitive analysis, and autonomous research agents.

## Overview

The Research Factory is designed to:
- Enable systematic market and competitive analysis
- Support autonomous research agents for information discovery
- Provide structured data collection and analysis workflows
- Integrate with existing services (spy-orchestration, data sources)
- Allow role-specific research tasks and agent deployments

## Architecture

```
research/
├── __init__.py              # Factory registry and exports
├── base.py                  # Abstract base classes and interfaces
├── market_analysis.py       # Market and competitive analysis workflow
└── research_agent.py        # Autonomous research agent workflow
```

## Usage Examples

### Market Analysis

```python
from factories.research import ResearchFactoryRegistry, ResearchType

# Get a market analysis workflow instance
market_workflow = ResearchFactoryRegistry.get_workflow(ResearchType.MARKET_ANALYSIS)

# Conduct competitive analysis
task = market_workflow.analyze_competitors(
    market_sector="technology",
    competitors=["CompanyA", "CompanyB", "CompanyC"],
    metrics=["market_share", "innovation", "customer_satisfaction"]
)

# Identify market trends
task = market_workflow.identify_trends(
    market_sector="finance",
    timeframe="1Y"
)

# Assess opportunities
task = market_workflow.assess_opportunities(
    market_sector="healthcare",
    criteria={"growth_potential": "high", "barriers": "low"}
)

# Check task status
print(f"Task ID: {task.task_id}")
print(f"Status: {task.status}")
print(f"Progress: {task.progress * 100}%")
```

### Research Agents

```python
from factories.research import ResearchFactoryRegistry, ResearchType

# Get a research agent workflow instance
agent_workflow = ResearchFactoryRegistry.get_workflow(ResearchType.RESEARCH_AGENT)

# Discover new technologies
task = agent_workflow.discover_technology(
    query="machine learning frameworks 2024",
    filters={"language": "python", "min_stars": 1000}
)

# Analyze research papers
task = agent_workflow.analyze_research_papers(
    topic="quantum computing applications",
    max_results=20
)

# Synthesize findings from multiple research tasks
task = agent_workflow.synthesize_findings(
    query="AI trends summary",
    source_tasks=["task_id_1", "task_id_2", "task_id_3"]
)

# Set up continuous monitoring
task = agent_workflow.monitor_topic(
    query="cybersecurity vulnerabilities",
    interval="daily"
)
```

## Core Components

### ResearchFactory (Base Class)

Abstract base class that all research workflows inherit from. Provides:
- Task management (create, track, cancel)
- Parameter validation
- Result storage and retrieval
- Priority management
- Progress tracking

### ResearchTask

Dataclass representing a research task with:
- Unique task ID
- Research type
- Status and priority
- Parameters and configuration
- Progress indicator (0.0 to 1.0)
- Results and metadata
- Error tracking

### ResearchResult

Structured research result with:
- Summary and findings
- Recommendations
- Confidence score
- Data sources used
- Timestamp and metadata

### ResearchType Enum

Supported research types:
- `MARKET_ANALYSIS` - Market and competitive analysis
- `RESEARCH_AGENT` - Autonomous research agents
- `COMPETITIVE_ANALYSIS` - Focused competitive analysis
- `TREND_ANALYSIS` - Trend identification and analysis

### ResearchStatus Enum

Task status values:
- `PENDING` - Task created, awaiting execution
- `COLLECTING_DATA` - Gathering data from sources
- `ANALYZING` - Performing analysis
- `COMPLETED` - Task completed successfully
- `FAILED` - Task failed with error
- `CANCELLED` - Task cancelled by user

### ResearchPriority Enum

Priority levels:
- `LOW` - Background tasks, monitoring
- `NORMAL` - Standard research tasks
- `HIGH` - Important analysis, time-sensitive
- `CRITICAL` - Urgent research, decision support

## Integration Points

### Market Analysis Integration
- **Data Sources**: Market data APIs, financial databases, industry reports
- **Analysis Tools**: Competitive analysis, SWOT, trend identification
- **Output**: Structured insights, recommendations, benchmarks

### Research Agent Integration
- **Spy-Orchestration Service**: Integration with existing discovery pipeline
- **Sources**: GitHub, arXiv, research papers, technical blogs
- **Capabilities**: Autonomous discovery, deep research, continuous monitoring

## Agent Types

### Discovery Agent
- Searches for new technologies, papers, tools
- Uses multiple sources (GitHub, arXiv, blogs)
- Applies relevance filtering and scoring

### Analysis Agent
- Deep analysis of specific topics or papers
- Extracts key insights and methodologies
- Provides structured summaries

### Synthesis Agent
- Combines findings from multiple sources
- Identifies patterns and connections
- Generates comprehensive reports

### Monitoring Agent
- Continuous monitoring of topics
- Periodic updates and alerts
- Trend tracking over time

## Configuration

Each workflow accepts a configuration dictionary:

```python
config = {
    "data_sources": ["market-api", "financial-db"],
    "analysis_depth": "comprehensive",
    "max_depth": 3,
    "sources": ["github", "arxiv", "blogs"],
    "timeout": 600
}

workflow = MarketAnalysisWorkflow(config)
```

## Extension Guidelines

To add a new research workflow:

1. Create a new file in `factories/research/`
2. Inherit from `ResearchFactory` base class
3. Implement required abstract methods:
   - `_setup()` - Initialize resources
   - `validate_parameters()` - Validate inputs
   - `research()` - Main research logic
   - `_get_data_sources()` - List sources
   - `_get_features()` - List features
   - `_get_analysis_types()` - List analysis types

4. Register in `ResearchFactoryRegistry` if needed
5. Update `__init__.py` exports

## Analysis Types

### Market Analysis
- **Competitive Analysis**: Compare competitors on key metrics
- **Trend Analysis**: Identify market trends and patterns
- **Opportunity Assessment**: Evaluate market opportunities
- **Risk Analysis**: Assess market risks and threats
- **SWOT Analysis**: Strengths, weaknesses, opportunities, threats
- **PESTEL Analysis**: Political, economic, social, technological, environmental, legal
- **Five Forces**: Porter's five forces analysis
- **Value Chain**: Value chain analysis

### Research Agent Analysis
- **Technology Discovery**: Find new tools, libraries, frameworks
- **Paper Analysis**: Analyze academic and research papers
- **Code Analysis**: Analyze code repositories and projects
- **Trend Analysis**: Identify emerging trends
- **Comparative Analysis**: Compare similar technologies/approaches
- **Impact Assessment**: Assess impact and adoption

## Future Enhancements

- [ ] Real-time data streaming integration
- [ ] Advanced ML models for trend prediction
- [ ] Multi-agent collaboration workflows
- [ ] Automated report generation
- [ ] Interactive dashboards
- [ ] Historical analysis and benchmarking
- [ ] Custom agent deployment
- [ ] API integration with external research tools
