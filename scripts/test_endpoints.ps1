# test_endpoints.ps1
# This script tests the API Gateway and AI Orchestrator endpoints.
# It requires the infrastructure and services to be running (make up).

$ErrorActionPreference = "Stop"

Write-Host "========================================="
Write-Host " Testing PitWall AI Endpoints"
Write-Host "========================================="

# 1. Test Authentication (Login)
Write-Host "`n1. Testing Login (POST http://localhost:8000/api/auth/login)..."
$loginBody = @{
    username = "analyst"
    password = "pitwall2024"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login" -Method Post -ContentType "application/json" -Body $loginBody
    $token = $loginResponse.access_token
    Write-Host "Login successful! Token: $($token.Substring(0, 15))..." -ForegroundColor Green
} catch {
    Write-Host "Login failed! Is the API Gateway running? ($($_.Exception.Message))" -ForegroundColor Red
    exit
}

# 2. Test AI Orchestrator Chat (Stateless LLM Endpoint)
Write-Host "`n2. Testing AI Orchestrator Chat (POST http://localhost:8007/chat)..."
$chatBody = @{
    message = "What is the pit window for a Medium tyre stint?"
    session_id = "test-session-123"
} | ConvertTo-Json

try {
    $chatResponse = Invoke-RestMethod -Uri "http://localhost:8007/chat" -Method Post -ContentType "application/json" -Body $chatBody
    Write-Host "Chat Response:" -ForegroundColor Green
    Write-Host $chatResponse.response -ForegroundColor Cyan
} catch {
    Write-Host "Chat endpoint failed. Is the AI Orchestrator running? ($($_.Exception.Message))" -ForegroundColor Red
}

Write-Host "`n========================================="
Write-Host " Tests Completed."
Write-Host "========================================="
Write-Host "Note: For WebSocket testing, please use the Next.js frontend (http://localhost:3000)."
