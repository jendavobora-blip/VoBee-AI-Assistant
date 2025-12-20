-- Database Schema for Invite-Only System
-- PostgreSQL Schema

-- Waitlist table
CREATE TABLE IF NOT EXISTS waitlist (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    use_case TEXT NOT NULL,
    persona VARCHAR(50) NOT NULL,
    priority_score INTEGER DEFAULT 0,
    position INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    invited_at TIMESTAMP
);

-- Create index on priority_score and created_at for efficient positioning
CREATE INDEX IF NOT EXISTS idx_waitlist_priority ON waitlist(priority_score DESC, created_at ASC);
CREATE INDEX IF NOT EXISTS idx_waitlist_email ON waitlist(email);

-- Invite codes table
CREATE TABLE IF NOT EXISTS invite_codes (
    code VARCHAR(20) PRIMARY KEY,
    issued_to VARCHAR(255),
    batch_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    used_by VARCHAR(255),
    used_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active'
);

-- Create indexes for efficient queries
CREATE INDEX IF NOT EXISTS idx_invite_codes_status ON invite_codes(status);
CREATE INDEX IF NOT EXISTS idx_invite_codes_batch ON invite_codes(batch_id);
CREATE INDEX IF NOT EXISTS idx_invite_codes_used_by ON invite_codes(used_by);

-- Referrals table
CREATE TABLE IF NOT EXISTS referrals (
    id UUID PRIMARY KEY,
    inviter_email VARCHAR(255) NOT NULL,
    invited_email VARCHAR(255) NOT NULL,
    invite_code VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (invite_code) REFERENCES invite_codes(code) ON DELETE SET NULL
);

-- Create indexes for efficient queries
CREATE INDEX IF NOT EXISTS idx_referrals_inviter ON referrals(inviter_email);
CREATE INDEX IF NOT EXISTS idx_referrals_invited ON referrals(invited_email);
CREATE INDEX IF NOT EXISTS idx_referrals_created_at ON referrals(created_at DESC);
