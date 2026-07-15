$modules = @(
    "Command Bus",
    "Communications",
    "Notifications",
    "Health",
    "Self Healing",
    "Maintenance",
    "Activity",
    "Briefs",
    "Asset Library",
    "Blueprints",
    "Creator",
    "N8N Studio"
)

Write-Host "=========================================="
Write-Host "   STARTING RRK MIGRATION SPRINT (WEEK 1)"
Write-Host "=========================================="

foreach ($module in $modules) {
    Write-Host "`n>>> Migrating $module <<<"
    py raphael_core\tests\builder\builder_migration_runner.py "$module"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Migration failed for $module. Halting sprint." -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n=========================================="
Write-Host "   RRK MIGRATION SPRINT COMPLETE!"
Write-Host "=========================================="
