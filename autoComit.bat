git --version
git add .
git commit -m "initial comit "
git push origin main

:: === Tagging for GitHub Actions Release Build ===
git tag v1.5
git push origin v1.5
pause
