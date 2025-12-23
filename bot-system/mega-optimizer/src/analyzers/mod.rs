pub mod rust_analyzer;
pub mod python_analyzer;
pub mod docker_analyzer;
pub mod dependency_analyzer;

use serde::{Deserialize, Serialize};
use anyhow::Result;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TechStack {
    pub has_rust: bool,
    pub has_python: bool,
    pub has_javascript: bool,
    pub has_docker: bool,
    pub has_kubernetes: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AnalysisResult {
    pub category: String,
    pub findings: Vec<Finding>,
    pub tech_stack: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Finding {
    pub severity: Severity,
    pub location: String,
    pub description: String,
    pub optimization: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum Severity {
    Critical,
    High,
    Medium,
    Low,
}

pub async fn detect_tech_stack(_owner: &str, _repo: &str) -> Result<TechStack> {
    // In a real implementation, this would scan the repository
    // For now, return a comprehensive tech stack
    Ok(TechStack {
        has_rust: false, // No Rust in current VoBee-AI-Assistant
        has_python: true,
        has_javascript: true,
        has_docker: true,
        has_kubernetes: true,
    })
}
