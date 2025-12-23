pub mod api;
pub mod pr_creator;
pub mod repo_scanner;

use octocrab::Octocrab;
use anyhow::Result;
use crate::optimizers::Optimization;

pub struct GitHubClient {
    client: Octocrab,
}

impl GitHubClient {
    pub fn new(token: String) -> Result<Self> {
        let client = Octocrab::builder()
            .personal_token(token)
            .build()?;
        
        Ok(Self { client })
    }
    
    pub async fn list_repos(&self, owner: &str) -> Result<Vec<String>> {
        // List all repositories for the owner
        let repos = self.client
            .repos(owner, "")
            .list()
            .send()
            .await?;
        
        Ok(repos.items.iter().map(|r| r.name.clone()).collect())
    }
    
    pub async fn create_optimization_pr(
        &self,
        owner: &str,
        repo: &str,
        optimizations: &[Optimization],
    ) -> Result<()> {
        pr_creator::create_pr(&self.client, owner, repo, optimizations).await
    }
}
