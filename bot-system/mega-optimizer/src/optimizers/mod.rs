pub mod rust_optimizer;
pub mod python_optimizer;
pub mod gpu_optimizer;
pub mod cache_optimizer;

use crate::analyzers::AnalysisResult;
use serde::{Deserialize, Serialize};
use anyhow::Result;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Optimization {
    pub category: String,
    pub description: String,
    pub file_changes: Vec<FileChange>,
    pub impact: ImpactLevel,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FileChange {
    pub path: String,
    pub content: String,
    pub change_type: ChangeType,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ChangeType {
    Create,
    Modify,
    Delete,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ImpactLevel {
    High,    // 10x+ improvement
    Medium,  // 3-10x improvement
    Low,     // 1-3x improvement
}

pub async fn generate_optimizations(
    analysis_results: &[AnalysisResult],
) -> Result<Vec<Optimization>> {
    let mut optimizations = Vec::new();
    
    for result in analysis_results {
        match result.tech_stack.as_str() {
            "python" => {
                let opts = python_optimizer::generate_optimizations(result).await?;
                optimizations.extend(opts);
            }
            "rust" => {
                let opts = rust_optimizer::generate_optimizations(result).await?;
                optimizations.extend(opts);
            }
            _ => {}
        }
    }
    
    // Add infrastructure optimizations
    let cache_opts = cache_optimizer::generate_redis_caching().await?;
    optimizations.extend(cache_opts);
    
    Ok(optimizations)
}
