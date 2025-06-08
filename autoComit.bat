git --version
git add .
git commit -m " updted interface used CSS stiles "
git push origin main

:: === Tagging for GitHub Actions Release Build ===
git tag v2.0
git push origin v2.0
pause
