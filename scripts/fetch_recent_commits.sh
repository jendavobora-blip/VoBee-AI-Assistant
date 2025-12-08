#!/bin/bash

################################################################################
# Script: fetch_recent_commits.sh
# Description: Fetches all commits from the last 2 hours across all accessible
#              repositories for the authenticated user.
# Requirements: 
#   - GitHub CLI (gh) installed and authenticated, OR
#   - GITHUB_TOKEN environment variable set with a valid GitHub personal access token
################################################################################

set -euo pipefail

# Configuration
HOURS_BACK=2
DEBUG=${DEBUG:-0}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored messages
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    if [ "$DEBUG" -eq 1 ]; then
        echo -e "${CYAN}[DEBUG]${NC} $1"
    fi
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check authentication method
check_authentication() {
    log_info "Checking authentication methods..."
    
    # Check if gh CLI is available and authenticated
    if command_exists gh; then
        if gh auth status >/dev/null 2>&1; then
            log_success "GitHub CLI (gh) is authenticated"
            USE_GH_CLI=1
            return 0
        else
            log_warning "GitHub CLI (gh) is installed but not authenticated"
        fi
    fi
    
    # Check if GITHUB_TOKEN is set
    if [ -n "${GITHUB_TOKEN:-}" ]; then
        log_success "GITHUB_TOKEN environment variable is set"
        USE_GH_CLI=0
        return 0
    fi
    
    log_error "No authentication method available!"
    log_error "Please either:"
    log_error "  1. Install and authenticate GitHub CLI: gh auth login"
    log_error "  2. Set GITHUB_TOKEN environment variable with a personal access token"
    exit 1
}

# Function to make GitHub API calls
github_api_call() {
    local endpoint="$1"
    local use_gh_cli="${USE_GH_CLI:-0}"
    
    if [ "$use_gh_cli" -eq 1 ]; then
        gh api "$endpoint" 2>/dev/null || echo "[]"
    else
        curl -s -H "Authorization: token ${GITHUB_TOKEN}" \
             -H "Accept: application/vnd.github.v3+json" \
             "https://api.github.com${endpoint}" 2>/dev/null || echo "[]"
    fi
}

# Function to get authenticated user
get_authenticated_user() {
    local response
    response=$(github_api_call "/user")
    echo "$response" | grep -o '"login"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4 | head -n1
}

# Function to fetch all accessible repositories
fetch_repositories() {
    local username="$1"
    local page=1
    local per_page=100
    local all_repos="[]"
    
    log_info "Fetching accessible repositories for user: $username"
    
    while true; do
        local repos
        repos=$(github_api_call "/user/repos?per_page=${per_page}&page=${page}&affiliation=owner,collaborator,organization_member")
        
        # Check if we got any repos
        if [ "$repos" = "[]" ] || [ -z "$repos" ]; then
            break
        fi
        
        # Merge repos into all_repos
        if [ "$all_repos" = "[]" ]; then
            all_repos="$repos"
        else
            all_repos=$(echo "$all_repos" "$repos" | jq -s '.[0] + .[1]')
        fi
        
        # Check if we got less than per_page results (last page)
        local count
        count=$(echo "$repos" | jq 'length')
        if [ "$count" -lt "$per_page" ]; then
            break
        fi
        
        ((page++))
    done
    
    echo "$all_repos"
}

# Function to calculate timestamp for N hours ago
get_timestamp_hours_ago() {
    local hours_back="$1"
    
    # Use date command (works on both Linux and macOS)
    if date --version >/dev/null 2>&1; then
        # GNU date (Linux)
        date -u -d "${hours_back} hours ago" +"%Y-%m-%dT%H:%M:%SZ"
    else
        # BSD date (macOS)
        date -u -v-"${hours_back}"H +"%Y-%m-%dT%H:%M:%SZ"
    fi
}

# Function to fetch commits for a repository since a given timestamp
fetch_commits_since() {
    local repo_full_name="$1"
    local since_timestamp="$2"
    
    log_debug "Fetching commits for $repo_full_name since $since_timestamp"
    
    local commits
    commits=$(github_api_call "/repos/${repo_full_name}/commits?since=${since_timestamp}&per_page=100")
    
    echo "$commits"
}

# Function to format and display commits
display_commits() {
    local repo_full_name="$1"
    local commits="$2"
    local commit_count
    
    commit_count=$(echo "$commits" | jq 'length')
    
    if [ "$commit_count" -eq 0 ]; then
        return 0
    fi
    
    echo ""
    echo -e "${GREEN}Repository: ${repo_full_name}${NC}"
    echo -e "${GREEN}Total commits: ${commit_count}${NC}"
    echo "$(printf '=%.0s' {1..80})"
    
    echo "$commits" | jq -r '.[] | 
        "  Commit: \(.sha[0:7])\n" +
        "  Author: \(.commit.author.name) <\(.commit.author.email)>\n" +
        "  Date:   \(.commit.author.date)\n" +
        "  Message: \(.commit.message | split("\n")[0])\n"'
    
    echo ""
}

# Main function
main() {
    log_info "Starting to fetch commits from the last ${HOURS_BACK} hours..."
    echo ""
    
    # Check required tools
    if ! command_exists jq; then
        log_error "jq is required but not installed. Please install jq:"
        log_error "  - On Ubuntu/Debian: apt-get install jq"
        log_error "  - On macOS: brew install jq"
        log_error "  - On CentOS/RHEL: yum install jq"
        exit 1
    fi
    
    if ! command_exists curl && [ "${USE_GH_CLI:-0}" -eq 0 ]; then
        log_error "curl is required but not installed."
        exit 1
    fi
    
    # Check authentication
    check_authentication
    
    # Get authenticated user
    local username
    username=$(get_authenticated_user)
    
    if [ -z "$username" ]; then
        log_error "Failed to get authenticated user. Please check your authentication."
        exit 1
    fi
    
    log_success "Authenticated as: $username"
    echo ""
    
    # Calculate timestamp for N hours ago
    local since_timestamp
    since_timestamp=$(get_timestamp_hours_ago "$HOURS_BACK")
    log_info "Fetching commits since: $since_timestamp"
    echo ""
    
    # Fetch all accessible repositories
    local repos
    repos=$(fetch_repositories "$username")
    
    local repo_count
    repo_count=$(echo "$repos" | jq 'length')
    
    if [ "$repo_count" -eq 0 ]; then
        log_warning "No repositories found for user: $username"
        exit 0
    fi
    
    log_success "Found ${repo_count} accessible repositories"
    echo ""
    
    # Counter for repositories with commits
    local repos_with_commits=0
    local total_commits=0
    
    # Iterate through repositories
    echo "$repos" | jq -r '.[] | .full_name' | while read -r repo_full_name; do
        log_debug "Processing repository: $repo_full_name"
        
        # Fetch commits for this repository
        local commits
        commits=$(fetch_commits_since "$repo_full_name" "$since_timestamp")
        
        local commit_count
        commit_count=$(echo "$commits" | jq 'length')
        
        if [ "$commit_count" -gt 0 ]; then
            ((repos_with_commits++)) || true
            ((total_commits+=commit_count)) || true
            display_commits "$repo_full_name" "$commits"
        fi
    done
    
    # Summary - note: the counters in the while loop don't propagate due to subshell
    # So we recalculate for the summary
    echo ""
    echo "$(printf '=%.0s' {1..80})"
    log_success "Scan complete!"
    
    # Count repos with commits and total commits
    local summary_repos=0
    local summary_commits=0
    echo "$repos" | jq -r '.[] | .full_name' | while read -r repo_full_name; do
        local commits
        commits=$(fetch_commits_since "$repo_full_name" "$since_timestamp")
        local commit_count
        commit_count=$(echo "$commits" | jq 'length')
        
        if [ "$commit_count" -gt 0 ]; then
            ((summary_repos++)) || true
            ((summary_commits+=commit_count)) || true
        fi
    done
    
    echo ""
}

# Run main function
main "$@"
