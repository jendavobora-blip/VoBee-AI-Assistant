use anyhow::Result;
use clap::Parser;
use log::{info, error};

mod analyzers;
mod optimizers;
mod github;
mod ai;

use analyzers::{AnalysisResult, TechStack};
use github::GitHubClient;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// GitHub owner/organization
    #[arg(short, long)]
    owner: String,

    /// Repository name (optional, will scan all repos if not provided)
    #[arg(short, long)]
    repo: Option<String>,

    /// GitHub token for API access
    #[arg(short, long, env = "GITHUB_TOKEN")]
    token: String,

    /// Dry run mode (don't create PRs)
    #[arg(short, long, default_value = "false")]
    dry_run: bool,
}

#[tokio::main]
async fn main() -> Result<()> {
    env_logger::init();
    
    let args = Args::parse();
    
    info!("🚀 Starting Mega Optimizer Bot System");
    info!("Owner: {}", args.owner);
    
    let github_client = GitHubClient::new(args.token.clone())?;
    
    // Get repositories to analyze
    let repos = if let Some(repo_name) = args.repo {
        vec![repo_name]
    } else {
        info!("📡 Scanning all repositories for owner: {}", args.owner);
        github_client.list_repos(&args.owner).await?
    };
    
    info!("📊 Found {} repositories to analyze", repos.len());
    
    // Analyze each repository
    for repo_name in repos {
        info!("🔍 Analyzing repository: {}/{}", args.owner, repo_name);
        
        match analyze_and_optimize(&github_client, &args.owner, &repo_name, args.dry_run).await {
            Ok(()) => info!("✅ Successfully processed {}", repo_name),
            Err(e) => error!("❌ Failed to process {}: {}", repo_name, e),
        }
    }
    
    info!("🎉 Mega Optimizer Bot System completed!");
    Ok(())
}

async fn analyze_and_optimize(
    github: &GitHubClient,
    owner: &str,
    repo: &str,
    dry_run: bool,
) -> Result<()> {
    // Clone or download repository content
    info!("📥 Fetching repository content...");
    
    // Detect tech stack
    info!("🔬 Detecting technology stack...");
    let tech_stack = analyzers::detect_tech_stack(owner, repo).await?;
    
    info!("Detected technologies: {:?}", tech_stack);
    
    // Run analyzers
    let mut analysis_results = Vec::new();
    
    if tech_stack.has_rust {
        info!("🦀 Running Rust analyzer...");
        let result = analyzers::rust_analyzer::analyze(owner, repo).await?;
        analysis_results.push(result);
    }
    
    if tech_stack.has_python {
        info!("🐍 Running Python analyzer...");
        let result = analyzers::python_analyzer::analyze(owner, repo).await?;
        analysis_results.push(result);
    }
    
    if tech_stack.has_docker {
        info!("🐳 Running Docker analyzer...");
        let result = analyzers::docker_analyzer::analyze(owner, repo).await?;
        analysis_results.push(result);
    }
    
    // Generate optimizations
    info!("⚡ Generating optimizations...");
    let optimizations = optimizers::generate_optimizations(&analysis_results).await?;
    
    info!("Found {} optimization opportunities", optimizations.len());
    
    if !dry_run && !optimizations.is_empty() {
        info!("📝 Creating pull request with optimizations...");
        github.create_optimization_pr(owner, repo, &optimizations).await?;
    } else if dry_run {
        info!("🏃 Dry run mode - skipping PR creation");
        for opt in &optimizations {
            info!("  - {}: {}", opt.category, opt.description);
        }
    }
    
    Ok(())
}
